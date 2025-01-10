# Gunshot Detection Using Digital Signal Processing

### Buidling w/ Docker
---
docker build -t my-python-app .
docker run -it --rm --privileged --device /dev/snd my-python-app 

1. Download gunshot and non gunshot .wav (duration and sample rate do not matter)
2. Store these into their respective folders: data/raw/gunshot and data/raw/not-gunshot
	- Make sure to remove delete_me.txt from reach folder in data
3. Run the audio_preprocessor notebook, make sure to update source and destination path so that raw gunshots go into preprocessed gunshots and raw not-gunshots go into preprocessed not-gunshots
4. Run the generate spectrogram notebook, make sure to update source and destination path
5. Run the generate_model notebook, make sure to name exported model to the following standard: 'trained_model_{model number}_ {date}.h5'
