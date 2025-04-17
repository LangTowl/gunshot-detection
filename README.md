# Patrol Vehicle Alert System: Gunshot Detection System
---
The Patrol Vehicle Alert System (PVAS) is a suite of AI powered features aimed at improving the safety and operational efficiency for the Polk County Sheriff's Office and their Deputies. This system specifically, aims to detect and classify gunshots from ambient audio. Upon detection, this system can be connected to an external API which can trigger a myriad of fast-response actions. 

# Built With
---
This application is built in *Python* and *Jupyter Notebooks* for AI model development and training. 

# Requirements
---
## Development / Training (`main`)

>[!note] Using python 3.12

[For main specific requirements.]()

## Production (`prod`)

>[!note] Using python 3.8

[For prod(uction) specific requirements.]()

## Installation

Can be installed with:

```terminal
pip install -r requirements.txt
```

# Branch Breakdown
---
## `main`

The main branch is used for testing and model development. It contains a series of Jupyter Notebooks used for pre-processing, spectrogram generation, and model training. Currently, this system uses a YOLO type architecture which requires bounding box and class labels for training. If additional models are desired, using a RoboFlow or a similar application is recommended to define bounding boxes and labels. 

- [Complete instructions on how to use this branch.]()
- [Technical Breakdown]()

## `prod`

The prod(uction) branch is a much more performant and lightweight version of main. All non-essential components and modules are removed, and model inference frequency is reduce to lower computation complexity. 

- [Technical Breakdown]()

# How To Run (Both `main` and `prod`)
--- 
Inside `src`:
```terminal
python3 main.py
```
