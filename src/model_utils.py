import io
from PIL import Image
import numpy as np
from multiprocessing import Value
import librosa
from keras import models
import matplotlib.pyplot as plt

# Variables to be shared across threads
prediction = Value('d', 0)
samples_sniffed = Value('i', 0)
gunshots_detected = Value('i', 0)

# Spectrogram generation constants
SAMPLE_RATE = 16000
FRAME_SIZE = 2048
HOP_SIZE = 128
SEGMENT_LENGTH = SAMPLE_RATE * 2
SEGMENT_HOP = SEGMENT_LENGTH // 2

model_path = 'models/trained_model_1_Jan_12_2025.h5'

def generate_spectrogram(audio_segment, model_input_dims = (128, 128)):
    # Compress channels
    if audio_segment.ndim > 1:
        audio_segment = audio_segment.squeeze()

    # Compute the STFT
    stft = librosa.stft(audio_segment, n_fft = FRAME_SIZE, hop_length = HOP_SIZE)
    stft_magnitude = np.abs(stft) ** 2

    # Convert to log-amplitude scale
    stft_db = librosa.amplitude_to_db(stft_magnitude)

    # Create the spectrogram plot
    plt.figure(figsize=(10, 4))
    plt.axis('off')
    librosa.display.specshow(
        stft_db,
        sr=SAMPLE_RATE,
        hop_length=HOP_SIZE,
        x_axis='time',
        y_axis='log',
        cmap='magma'
    )

    # Save the figure into a memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, transparent=True)
    buf.seek(0)

    # Load the image from the buffer and convert it to RGB
    spectrogram_image = Image.open(buf).convert("RGB")
    spectrogram_image = spectrogram_image.resize((128, 128))  # Resize to (128, 128)

    # Convert to numpy array and normalize the pixel values
    spectrogram_image = np.array(spectrogram_image) / 255.0

    # Close the plot to release memory
    plt.close()

    return np.expand_dims(spectrogram_image, axis = 0)

def model_prediction(stop_event, spectrogram_queue):
    model = models.load_model(model_path, compile = False)

    while not stop_event.is_set():
        while not spectrogram_queue.empty():
            audio_segment = spectrogram_queue.get()

            spectrogram = generate_spectrogram(audio_segment)
            processed_spectrogram = np.expand_dims(spectrogram, axis = 0)

            # print(f"Confidence: {model.predict(processed_spectrogram, verbose=0)[0]} Samples Sniffed: {samples_sniffed.value}")

            samples_sniffed.value += 1