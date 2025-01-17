import os
from PIL import Image
import numpy as np
from multiprocessing import Value
import librosa
from keras import models
from keras import preprocessing

# Variables to be shared across threads
prediction = Value('d', 0)
gunshots_detected = Value('i', 0)

# Spectrogram generation constants
SAMPLE_RATE = 16000
FRAME_SIZE = 2048
HOP_SIZE = 128
SEGMENT_LENGTH = SAMPLE_RATE * 2
SEGMENT_HOP = SEGMENT_LENGTH // 2

model_path = 'models/trained_model_1_Jan_12_2025.h5'

def generate_spectrogram(audio_segment, model_input_dims = (128, 128)):
    # Compute the STFT
    stft = librosa.stft(audio_segment, n_fft = FRAME_SIZE, hop_length = HOP_SIZE)
    stft_magnitude = np.abs(stft) ** 2

    # Convert to log-amplitude scale
    stft_db = librosa.amplitude_to_db(stft_magnitude, ref=np.max)

    # Normalize the spectrogram
    stft_db_normalized = (stft_db - stft_db.min()) / (stft_db.max() - stft_db.min())

    # Convert to a PIL image for resizing and RGB conversion
    stft_image = Image.fromarray(np.uint8(stft_db_normalized * 255), mode="L")
    stft_image = stft_image.resize(model_input_dims).convert("RGB")

    # Convert to numpy array and normalize to [0, 1]
    spectrogram_array = preprocessing.image.img_to_array(stft_image) / 255.0

    return spectrogram_array

def model_prediction(stop_event, spectrogram_queue):
    model = models.load_model(model_path, compile = False)

    while not spectrogram_queue.empty():
        audio_segment = spectrogram_queue.get()

        spectrogram = generate_spectrogram(audio_segment)
        processed_spectrogram = np.array(spectrogram)

        prediction = model.predict(processed_spectrogram)
