import tkinter as tk
from queue import Empty

class AudioRenderer:
    def __init__(self, root, stop_event, volume_queue, spectrogram_queue):
        # Initialize window config
        self.root = root
        self.root.title("GDS Audio Renderer")
        self.stop_event = stop_event
        self.volume_queue = volume_queue

        # Column one UI
        tk.Label(self.root, text="Spectrogram").grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)

        self.spec_space_holder = tk.Canvas(root, width = 256, height = 256, bg = "white")
        self.spec_space_holder.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)

        tk.Label(self.root, text = "Volume", anchor = "w", justify = "left").grid(row = 2, column = 0, sticky = "w", padx = 5,)

        self.canvas = tk.Canvas(root, width = 256, height = 30, bg = "white")
        self.canvas.grid(row = 3, column = 0, columnspan = 2, padx = 5, pady = 5)
        self.volume_bar = self.canvas.create_rectangle(0, 0, 0, 30, fill = "green")

        # Column two UI
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

    def updateConfidenceThreshold(self, val):
        formatted_val = f"{int(val):4d}"
        self.confidence_slider_label.config(text = f"RCS: {formatted_val}")

    def updateDownScaleThreshold(self, val):
        formatted_val = f"{int(val):4d}"
        self.downscale_slider_label.config(text = f"DSF: {formatted_val}")


    def update_volume_bar(self):
        if not self.stop_event.is_set():
            # Clear the queue by processing all available items
            latest_volume = None
            try:
                # Process all items in queue, keeping only the latest
                while True:
                    latest_volume = self.volume_queue.get(block = False)
            except Empty:
                pass

            # If we got at least one volume reading, update the bar
            if latest_volume is not None:
                # Update the width of the bar based on volume level
                bar_width = int(latest_volume * 256)
                self.canvas.coords(self.volume_bar, 0, 0, bar_width, 30)

                # Update color based on volume
                if latest_volume > 0.7:
                    color = "red"
                elif latest_volume > 0.3:
                    color = "yellow"
                else:
                    color = "green"
                self.canvas.itemconfig(self.volume_bar, fill = color)

            self.root.after(1, self.update_volume_bar)