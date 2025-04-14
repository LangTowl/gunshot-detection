import tkinter as tk
from queue import Empty
from PIL import Image, ImageTk
from model_utils import mel_spectrogram_generator

class AudioRenderer:
    def __init__(self, root, stop_event, volume_queue, spectrogram_queue):
        # Initialize window and config
        self.root = root
        self.root.title("GDS Audio Renderer")
        self.stop_event = stop_event
        self.volume_queue = volume_queue
        self.spectrogram_queue = spectrogram_queue

        ### Column one UI

        # Spectrogram setup
        tk.Label(self.root, text="Spectrogram").grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
        self.spec_space_holder = tk.Canvas(root, width = 256, height = 256, bg = "white")
        self.spec_space_holder.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)

        # Refresh spectrogram
        self.update_spectrogram()

    def update_spectrogram(self):
        if not self.stop_event.is_set():

            try:
                # Get next segment
                audio_segment = self.spectrogram_queue.get(block = False)

                # Generate spectrogram
                spectrogram = mel_spectrogram_generator(audio_segment)

                # Convert to TK
                spectrogram_tk = ImageTk.PhotoImage(spectrogram)

                # Update the spectrogram on the UI
                self.spec_space_holder.create_image(0, 0, anchor = "nw", image = spectrogram_tk)

                # Bum ah garbage collection
                self.spec_space_holder.image = spectrogram_tk
            except Empty:
                pass

            # Dispatch after 1 second
            self.root.after(10, self.update_spectrogram)