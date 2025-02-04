import sys
from queue import Empty

def volume_animation_bar(stop_event, volume_queue, prediction, samples_sniffed, gunshots_detected, chunk_duration = 0.01, max_length=40):
    # While thread is active
    while not stop_event.is_set():
        try:
            volume_level = volume_queue.get(timeout = chunk_duration)        # Volume level is assigned to queue's data, if queue is empty, raise Empty flag
            filled_length = int(volume_level * max_length)                  # Determine number of bars to fill bar
            bar = "█" * filled_length + " " * (max_length - filled_length)  # Determines number of █ and " " to fill bar
            percentage = f"{int(volume_level * 100):3d}%"                   # Format percentage to always be 3 digits wide
            sys.stdout.write(f"\r|{bar}| {percentage} [Prediction: {prediction.value:.5f}] [Samples Sniffed: {samples_sniffed.value:5d}] [Gunshots Detected: {gunshots_detected.value}]")
            sys.stdout.flush()  # Flush screen
        except Empty:
            pass