import numpy as np
from queue import Queue
import sounddevice as sd
from multiprocessing import Value

volume_queue = Queue()          # Queue is accessed by volume rendered
spectrogram_queue = Queue()     # Queue is used to generate spectrogram

def record_audio(stop_event, chunk_duration = 0.01, sample_rate = 16000, channels = 1):

    # Determine sample
    num_samples = int(sample_rate * chunk_duration)

    # Buffer setup
    segment_duration = 2.0
    number_of_segments = int(segment_duration / chunk_duration)

    # Audio buffers
    audio_buffer_1 = []
    audio_buffer_2 = []

    # Setup offset buffer
    silent_chunks = int(sample_rate * 1.0 / num_samples)
    silent_audio = np.zeros((num_samples, channels), dtype=np.float32)
    audio_buffer_1 = [silent_audio] * silent_chunks


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
            audio_buffer_1.append(audio_segment)
            if len(audio_buffer_1) == number_of_segments:
                full_segment_1 = np.concatenate(audio_buffer_1[:number_of_segments], axis=0)
                spectrogram_queue.put(full_segment_1)
                audio_buffer_1 = audio_buffer_1[number_of_segments:]

            # Append audio buffer to spectrogram queue once it accumulates 2 seconds of audio
            audio_buffer_2.append(audio_segment)
            if len(audio_buffer_2) == number_of_segments:
                full_segment_1 = np.concatenate(audio_buffer_2[:number_of_segments], axis=0)
                spectrogram_queue.put(full_segment_1)
                audio_buffer_2 = audio_buffer_2[number_of_segments:]
