import sounddevice as sd
import numpy as np
from queue import Queue

# Generate thread-safe queue for use across threads: volume bar & data processing
audio_queue = Queue()

def audio_input_pipeline(stop_event, callback = None, chunk_duration = 0.1):
    # System parameters
    samplerate = 16000
    channels = 1

    # Initiate audio input stream
    with sd.InputStream(samplerate = samplerate, channels = channels, dtype = 'float32') as stream:
        # While thread is active...
        while not stop_event.is_set():
            num_samples = int(samplerate * chunk_duration)  # Determine number of samples to fetch
            audio_chunk, _ = stream.read(num_samples)       # Fetch audio chunk
            rms = np.sqrt(np.mean(np.square(audio_chunk)))  # Compute RMS:
            volume_level = min(1.0, rms * 10)               # Normalize to RMS for display

            audio_queue.put(volume_level)  # Pass RMS (volume) to volume bar

            if callback:
                callback(audio_chunk)  # TODO: Implement preprocessing subroutine