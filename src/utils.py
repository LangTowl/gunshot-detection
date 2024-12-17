import sys
import time
from queue import Empty

def volume_animation_bar(stop_event, audio_queue, chunk_duration = 0.1, max_length = 40):
    # While thread is active
    while not stop_event.is_set():
        try:
            volume_level = audio_queue.get(timeout = chunk_duration)        # Volume level is assigned to queue's data, if queue is empty, raise Empty flag
            filled_length = int(volume_level * max_length)                  # Determine number of bars to fill bar
            bar = "█" * filled_length + " " * (max_length - filled_length)  # Determines number of █ and " " to fill bar
            sys.stdout.write(f"\r|{bar}| {int(volume_level * 100)}% ")      # Write to screen
            sys.stdout.flush()                                              # Flush screen
        except Empty:
            pass