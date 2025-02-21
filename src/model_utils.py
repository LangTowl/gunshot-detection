import librosa
from PIL import Image
import librosa.display
from ultralytics import YOLO
from datetime import datetime
import matplotlib.pyplot as plt
from multiprocessing import Value

# Variables to be shared across threads
prediction_decimal = Value('d', 0.0)
samples_sniffed = Value('i', 0)
gunshots_detected = Value('i', 0)

# Used directories
detections_directory = 'data/detections'

SAMPLE_RATE = 16000

def mel_spectrogram_generator(data, sr = 16000, duration = 2.0, n_fft = 2560, hop_length = 128, n_mels = 512, fmin = 4000, fmax = 8000, power = 2.0, figsize = (5,5), target_shape = (256, 256), show = False, save = False):
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

def model_prediction(stop_event, spectrogram_queue):
    global prediction_decimal
    global gunshots_detected

    # Time of last recorded gunshot
    time_of_last_gunshot = datetime.now()

    # Load model
    model = YOLO("/Users/langtowl/PycharmProjects/gunshot-detection/src/best.pt")

    # Code to run while thread is alive
    while not stop_event.is_set():
        # Only execute when queue is !empty
        while not spectrogram_queue.empty():
            # Load next segment
            audio_segment = spectrogram_queue.get()

            # Generate spectrogram
            spectrogram = mel_spectrogram_generator(audio_segment)

            # Make prediction
            prediction = model.predict(spectrogram, verbose = False)

            # Extract bounding boxes
            bounding_boxes = prediction[0].boxes.xyxy.cpu().numpy()

            if len(bounding_boxes) > 0:
                # Determine time since last detection
                now = datetime.now()
                time_delta = (now - time_of_last_gunshot).total_seconds()

                if time_delta > 1.0:
                    gunshots_detected.value += 1
                    time_of_last_gunshot = now


            samples_sniffed.value += 1

"""
formatted_date_time = now.strftime("%m_%d_%H_%M")
                    filename = os.path.join(detections_directory, f"gs_{samples_sniffed.value}_conf_{prediction_decimal.value:.3f}_date_{formatted_date_time}.wav")
                    audio_segment_int16 = (audio_segment * 32767).astype(np.int16)
                    write(filename, SAMPLE_RATE, audio_segment_int16)
"""