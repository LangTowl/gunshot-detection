import os
import librosa
import numpy as np
from keras import models
from datetime import datetime
from multiprocessing import Value
from scipy.io.wavfile import write
from skimage.transform import resize

# Variables to be shared across threads
prediction_decimal = Value('d', 0.0)
samples_sniffed = Value('i', 0)
gunshots_detected = Value('i', 0)

# Used directories
detections_directory = 'data/detections'
model_path = 'models/trained_model_3_Jan_29_2025.h5'

# Spectrogram generation constants
SAMPLE_RATE = 16000
FRAME_SIZE = 2048
HOP_SIZE = 128
TARGET_SHAPE = (128, 128)

def generate_spectrogram_array(audio_data):
    # Compress channels if necessary
    if audio_data.ndim > 1:
        audio_data = audio_data.squeeze()

    # Ensure audio data is a NumPy array
    audio = np.array(audio_data)

    # Check if the audio length is sufficient for STFT
    if len(audio) < FRAME_SIZE:
        audio = np.pad(audio, (0, FRAME_SIZE - len(audio)), mode='constant')

    # Short-time Fourier transform to magnitude
    stft = librosa.stft(audio, n_fft=FRAME_SIZE, hop_length=HOP_SIZE)
    magnitude = np.abs(stft)

    # Convert amplitude to dB
    db_scale = librosa.amplitude_to_db(magnitude, ref=np.max)

    # Resize
    db_resized = resize(db_scale, TARGET_SHAPE, mode='constant', preserve_range=True)

    # Normalize
    db_min, db_max = db_resized.min(), db_resized.max()
    db_resized = (db_resized - db_min) / (db_max - db_min + 1e-8)

    # Convert to float32 for memory saving
    db_resized = db_resized.astype(np.float32)

    # Expand to 3 channels for input
    db_resized = np.stack([db_resized, db_resized, db_resized], axis=-1)

    return db_resized


def model_prediction(stop_event, spectrogram_queue):
    global prediction_decimal
    global gunshots_detected

    # Load trained model
    model = models.load_model(model_path, compile=False)

    # Time of last recorded gunshot
    time_of_last_gunshot = datetime.now()

    # Code to run while thread is alive
    while not stop_event.is_set():
        # Only execute when queue is !empty
        while not spectrogram_queue.empty():
            # Load next segment
            audio_segment = spectrogram_queue.get()

            # Generate spectrogram
            spectrogram = generate_spectrogram_array(audio_segment)

            # Prepare batch for prediction
            spectrogram = np.squeeze(spectrogram)  # Remove any unintended extra dimensions
            spectrogram_batch = np.expand_dims(spectrogram, axis=0)

            # Make prediction
            prediction = model.predict(spectrogram_batch, verbose=0)
            prediction_decimal.value = prediction[0][0]

            # Gunshot if confidence is > ##%
            if prediction_decimal.value > 0.95:
                # Determine time since last detection
                now = datetime.now()
                time_delta = (now - time_of_last_gunshot).total_seconds()

                if time_delta > 1.0:

                    gunshots_detected.value += 1
                    time_of_last_gunshot = now

                    # Save file to disk if gunshot is detected
                    formatted_date_time = now.strftime("%m_%d_%H_%M")
                    filename = os.path.join(detections_directory, f"gs_{samples_sniffed.value}_conf_{prediction_decimal.value:.3f}_date_{formatted_date_time}.wav")
                    audio_segment_int16 = (audio_segment * 32767).astype(np.int16)
                    write(filename, SAMPLE_RATE, audio_segment_int16)

            samples_sniffed.value += 1
