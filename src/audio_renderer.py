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

        # Volume bar renderer
        tk.Label(self.root, text = "Volume", anchor = "w", justify = "left").grid(row = 2, column = 0, sticky = "w", padx = 5,)
        self.canvas = tk.Canvas(root, width = 256, height = 30, bg = "white")
        self.canvas.grid(row = 3, column = 0, columnspan = 2, padx = 5, pady = 5)
        self.volume_bar = self.canvas.create_rectangle(0, 0, 0, 30, fill = "green")

        #### Column two UI

        # Performance Metrics
        tk.Label(self.root, text = f"""
        Samples Sniffed:   {0:5d}\n
        Model Inference:   {0:5d}\n
        Prediction Conf:    {0:5d}\n
        """, anchor = "w", justify = "left").grid(row = 1, column = 2, sticky = "w", columnspan = 2, padx = 15, pady = 5)

        self.confidence_slider_label = tk.Label(root, text = "RCS", font = ("Courier", 16))
        self.confidence_slider_label.grid(row = 2, column = 2, sticky = "w", padx = 5, )
        self.confidence_slider = tk.Scale(root, from_ = 0, to = 100, orient = "horizontal", showvalue = False, command = self.updateConfidenceThreshold)
        self.confidence_slider.set(80)
        self.confidence_slider.grid(row = 2, column = 3, sticky = "w", padx = 5, )

        self.downscale_slider_label = tk.Label(root, text = "DSF", font = ("Courier", 16))
        self.downscale_slider_label.grid(row = 3, column = 2, sticky = "w", padx = 5, )
        self.downscale_slider = tk.Scale(root, from_ = 0, to = 100, orient = "horizontal", showvalue = False, command = self.updateDownScaleThreshold)
        self.downscale_slider.set(45)
        self.downscale_slider.grid(row = 3, column = 3, sticky = "w", padx = 5, )

        # Start updating the volume bar with a faster refresh rate
        self.update_volume_bar()
        self.update_spectrogram()

    # Update RCS on slider adjustment
    def updateConfidenceThreshold(self, val):
        formatted_val = f"{int(val):4d}"
        self.confidence_slider_label.config(text = f"RCS: {formatted_val}")

    # Update DCF on slider adjustment
    def updateDownScaleThreshold(self, val):
        formatted_val = f"{int(val):4d}"
        self.downscale_slider_label.config(text = f"DSF: {formatted_val}")

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

    def update_volume_bar(self):
        # Run while stop event is not set
        if not self.stop_event.is_set():
            # Purge old samples
            latest_volume = None

            try:
                # Process all items in queue
                while True:
                    # Get latest samples
                    latest_volume = self.volume_queue.get(block = False)
            except Empty:
                pass

            # Run if there are samples to process
            if latest_volume is not None:
                # Compute bar width
                bar_width = int(latest_volume * 256)
                self.canvas.coords(self.volume_bar, 0, 0, bar_width, 30)

                # Adjust color based on volume
                if latest_volume > 0.7:
                    color = "red"
                elif latest_volume > 0.3:
                    color = "yellow"
                else:
                    color = "green"

                self.canvas.itemconfig(self.volume_bar, fill = color)

            # Dispatch after 1 second
            self.root.after(1, self.update_volume_bar)