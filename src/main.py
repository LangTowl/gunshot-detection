import os
import threading
from volume_bar_renderer import volume_animation_bar
from audio_input import volume_queue, spectrogram_queue, record_audio
from model_utils import prediction_decimal, samples_sniffed, model_prediction, gunshots_detected, average_volume, last_volume, model_inferences

if __name__ == "__main__":

    # Shut up warning
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    # Stop event to kill executions across threads
    stop_event = threading.Event()

    # Initiate thread for volume bar rendering
    animation_thread = threading.Thread(target = volume_animation_bar, args = (stop_event, volume_queue, prediction_decimal, samples_sniffed, gunshots_detected, average_volume, last_volume, model_inferences))
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
        animation_thread.join()
        prediction_thread.join()
        print("Exiting program...")