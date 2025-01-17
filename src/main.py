import threading
from audio_input import volume_queue, spectrogram_queue, samples_sniffed, record_audio
from volume_bar_renderer import volume_animation_bar
from model_utils import prediction, model_prediction

if __name__ == "__main__":
    # Stop event to kill executions across threads
    stop_event = threading.Event()

    # Initiate thread for volume bar rendering
    animation_thread = threading.Thread(target = volume_animation_bar, args = (stop_event, volume_queue, prediction))
    animation_thread.start()

    # Initialize thread for spectrogram generation and model predictions
    prediction_thread = threading.Thread(target = model_prediction, args = (stop_event, spectrogram_queue))
    prediction_thread.start()

    try:
        print("Initializing audio input...\n")
        record_audio(stop_event)
    except KeyboardInterrupt:
        print("\n\nStopping audio input pipeline...\n")
        stop_event.set()
    finally:
        animation_thread.join()  # Wait for thread to finish task, then terminate
        print("Exiting program...")