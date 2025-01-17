import numpy as np
from queue import Queue
import sounddevice as sd
from multiprocessing import Value

volume_queue = Queue()          # Queue is accessed by volume rendered
spectrogram_queue = Queue()     # Queue is used to generate spectrogram

def record_audio(stop_event, chunk_duration = 0.01, sample_rate = 16000, channels = 1):

    # Determine sample
    num_samples = int(sample_rate * chunk_duration)

    # Buffer to accumulate 2-second audio
    segment_duration = 2.0
    number_of_segments = int(segment_duration / chunk_duration)
    audio_buffer = []

    # Initialize audio stream
    with sd.InputStream(samplerate = sample_rate, channels = channels, dtype = 'float32') as stream:

        # While thread is active
        while not stop_event.is_set():
            # Record audio segment based on computed sample duration
            audio_segment, _ = stream.read(num_samples)

            # Compute volume and pass to volume queue
            rms = np.sqrt(np.mean(np.square(audio_segment)))
            volume_level = min(1.0, rms * 10)
            volume_queue.put(volume_level)

            # Append audio buffer to spectrogram queue once it accumulates 2 seconds of audio
            audio_buffer.append(audio_segment)
            if len(audio_buffer) == number_of_segments:
                full_segment = np.concatenate(audio_buffer[:number_of_segments], axis=0)
                spectrogram_queue.put(full_segment)
                audio_buffer = audio_buffer[number_of_segments:]
