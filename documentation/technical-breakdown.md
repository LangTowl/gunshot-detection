# Technical Breakdown
<img width="1274" alt="image" src="https://github.com/user-attachments/assets/41f71b02-91c5-4d32-8051-b3ae197f2614" />


## System Input
The Gunshot Detection System (GDS) begins with collecting two overlapping audio queues. The second queue has a one second offset from the first, creating a sliding window effect. Each sample is standardized to seconds long with a sampler rate of $16,000 Hz$. There is an optional parameter in the `audio_input.py` which can be used to add a downscaling factor to reduce the volume of the incoming audio. 

## Pre-Processing
Once the incoming audio has been standardized, it is passed through a Short Time Fourier Transform. 

$$S(m,k)=\sum_{n=0}^{N-1}x(n+mH)\cdot w(n)\cdot e^{-i2\pi n\frac{k}{N}}$$

- $k=$ proxy for frequency *(also measured in # of frequency bins)*
- $m=$ proxy for time *(also measures frame number or # of frames)*
- $N=$ all samples contained in frame size, otherwise the frame size
- $x(n+mH)=$ all samples contained in current frame
	- $mH=$ starting sample of current frame
- $w(n)=$ windowing function
- $e^{-j2\pi n \frac{k}{N}}=$ is a pure tone whose frequency is given by $\dfrac{k}{N}$
	- essentially projects our windowed sample onto pure tone

From this new frequency representation of the input signal, a Mel-Spectrogram is generated.

## Training
The spectrograms generated in the previous stage are the actual datum that the model is trained on. Since the YOLO models require labels and bounding box coordinates. Use of an online platform like RoboFlow for data labeling is necessary. 

The process for training the model is outlined [here](). 

## Model Inference Pipeline
During application runtime, a rolling average of the ambient volume is aggregated. Only when the ambient volume increases $x$ times louder than the average, is the model inference. 

>[!note] This volume threshold is defined inside of model_utils.py

In the event this volume threshold is exceeded, that sample is used to generate a spectrogram. This spectrogram is used to inference the model to look for gunshots. In the event of a detection, the confidence must exceed the confidence threshold in order for it to be flagged as a gunshot. 

>[!note] This confidence threshold is defined inside of model_utils.py

This detection can be used to trigger or query and external API which can react to the detection. At this time, this application is only capable of the actual detection, and does to connect to any external APIs. 
