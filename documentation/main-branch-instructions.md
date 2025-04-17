# Main Branch Setup
---
The main branch consists of 3 important folders:
- model: where the current best model is housed.
- notebooks: where all the Jupyter Notebooks used in model generation and training are housed.
- src: where the .py files used to execute the program are housed.

## Model
---
Currently, this model stored in this folder is the best model our team was able to achieve. Its performance metrics can be found in the following folder:

```text
./notebooks/runs
```

## Notebooks
---
There are 4 notebooks in this folder, each is responsible for a different portion of the model development pipeline.

### Step 1: Audio Preprocessing 
---
The audio_preprocessor notebook is used to take in any audio file and convert it into a standardized format: 2 seconds long with a sample rate of $16,000Hz$

### Step 2: Spectrogram Generation
---
Once all the samples have been standardized, the spectrogram_generator notebook can be used to convert these sound samples into $256\times256$ RGB spectrogram images. This new medium is what the model will be trained and inferenced with. 

### Steps 3-4: Model Generation and Model Training
---
Refer to the following instructions to construct the dataset and generate/train the model. 

[Training Instructions]()
