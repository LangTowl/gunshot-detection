import librosa
import matplotlib
import numpy as np
from PIL import Image
import librosa.display
from ultralytics import YOLO
from datetime import datetime
import matplotlib.pyplot as plt
from multiprocessing import Value

matplotlib.use('agg')

# Variables to be shared across threads
prediction_decimal = Value('f', 0.0)
samples_sniffed = Value('i', 0)
gunshots_detected = Value('i', 0)
model_inferences = Value('i', 0)
average_volume = Value('f', 0.0)
last_volume = Value('f', 0.0)

# Used directories
detections_directory = 'data/detections'

SAMPLE_RATE = 16000

def mel_spectrogram_generator(data, sr = 16000, n_fft = 2560, hop_length = 128, n_mels = 512, fmin = 4000, fmax = 8000, power = 2.0, figsize = (5,5)):
    # Compress into single mono channel
    if data.ndim > 1:
        data = data.squeeze()

    # Compute spectrogram
    spectrogram = librosa.feature.melspectrogram(
        y = data,
        sr = sr,
        n_fft = n_fft,
        hop_length = hop_length,
        n_mels = n_mels,
        fmin = fmin,
        fmax = fmax,
        power = power
    )

    # Convert to decibel
    spectrogram_decibel = librosa.power_to_db(spectrogram)

    # Open and configure plot
    fig, ax = plt.subplots(figsize=figsize, dpi=100)
    ax.set_position([0, 0, 1, 1])
    ax.set_frame_on(False)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    fig.patch.set_alpha(0)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.ioff()

    # Plot spectrogram
    librosa.display.specshow(
        spectrogram_decibel,
        sr = sr,
        hop_length = hop_length,
        x_axis = "time",
        y_axis = "mel",
        fmin = fmin,
        fmax = fmax,
        vmin = -20,
        vmax = 10,
        cmap = 'magma'
    )

    # Copy spectrogram graph to image, then delete graph
    fig.canvas.draw()
    image = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
    plt.close(fig)

    return image

def model_prediction(stop_event, spectrogram_queue, confidence_threshold = 0.75, volume_threshold = 3.0):
    global prediction_decimal
    global gunshots_detected
    global average_volume
    global last_volume
    global model_inferences
    global samples_sniffed

    # Time of last recorded gunshot
    time_of_last_gunshot = datetime.now()

    # Load model
    model = YOLO("/Users/langtowl/PycharmProjects/gunshot-detection/model/map50-97.pt", verbose = False)

    # Code to run while thread is alive
    while not stop_event.is_set():
        # Only execute when queue is !empty
        while not spectrogram_queue.empty():
            # Load next segment
            audio_segment = spectrogram_queue.get()
            samples_sniffed.value += 1

            # Update current and average volume
            current_volume = np.abs(np.max(audio_segment, axis = 0))
            last_volume.value = current_volume
            average_volume.value = (average_volume.value + (current_volume - average_volume.value) / samples_sniffed.value)

            # Determine if volume threshold met
            if current_volume >= average_volume.value * volume_threshold:

                # Generate spectrogram
                spectrogram = mel_spectrogram_generator(audio_segment)

                # Make prediction
                prediction = model.predict(spectrogram, verbose = False)
                model_inferences.value += 1

                # Check to see if there were any detections
                if prediction[0].boxes.shape[0] > 0:

                    # Update value of prediction
                    prediction_decimal.value = float(prediction[0].boxes.conf.max().item())

                    # Check to see if any of the detections exceed our threshold
                    if (prediction[0].boxes.conf > confidence_threshold).any():
                        # Determine time since last detection
                        now = datetime.now()
                        time_delta = (now - time_of_last_gunshot).total_seconds()

                        # Ignore redundant detections that occur within last 2 seconds
                        if time_delta > 2.0:
                            gunshots_detected.value += 1
                            time_of_last_gunshot = now