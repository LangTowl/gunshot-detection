import sys
from queue import Empty

def volume_animation_bar(stop_event, volume_queue, prediction, samples_sniffed, gunshots_detected, average_volume, last_volume, model_inferences, chunk_duration = 0.01, max_length = 40):
    # Debug
    print("Initializing volume bar renderer...\n")

    # While thread is active
    while not stop_event.is_set():
        try:
            volume_level = volume_queue.get(timeout = chunk_duration)        # Volume level is assigned to queue's data, if queue is empty, raise Empty flag
            filled_length = int(volume_level * max_length)                   # Determine number of bars to fill bar
            bar = "█" * filled_length + " " * (max_length - filled_length)   # Determines number of █ and " " to fill bar
            percentage = f"{int(volume_level * 100):3d}%"                    # Format percentage to always be 3 digits wide
            sys.stdout.write(f"\r|{bar}| {percentage} [Last Volume: {last_volume.value:7.3f}] [Avg. Volume: {average_volume.value:7.3f}] [Samples Sniffed: {samples_sniffed.value:5d}] [Model Inferences: {model_inferences.value:5d}] [Prediction: {prediction.value:.5f}]  [Gunshots Detected: {gunshots_detected.value:5d}]")
            sys.stdout.flush()  # Clear screen
        except Empty:
            pass