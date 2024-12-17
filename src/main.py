import threading
from audio_input import audio_input_pipeline, audio_queue
from utils import volume_animation_bar

def main():
    # Stop event used to kill threads
    stop_event = threading.Event()

    # Initiate thread for volume bar rendering
    animation_thread = threading.Thread(target = volume_animation_bar, args = (stop_event, audio_queue))
    animation_thread.start()

    try:
        print("Initiating audio input pipeline...")
        audio_input_pipeline(stop_event, callback = None) # TODO: Implement callback function in audio_input
    except KeyboardInterrupt:
        print("\nStopping audio input pipeline...")
        stop_event.set()
    finally:
        animation_thread.join()      # Wait for thread to finish task, then terminate
        print("Exiting program...")

if __name__ == "__main__":
    main()