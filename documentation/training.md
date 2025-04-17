
# Training a new YOLO Model with Roboflow

## Prerequisites

- Roboflow account
- Labeled image dataset
- Local GPU setup

## Create a Project

1. Log in to [Roboflow](https://app.roboflow.com/).
2. Click **"Create New Project"**.
3. Select:
   - **Project Type**: Object Detection
   - **Project Name**: (e.g., `Gunshot Detection`)
   - **Annotation Type**: Bounding Box

## Upload Images

1. Click **Upload Images** or **Drag-and-Drop** your dataset files.
2. Select your dataset images.
3. If images are not annotated:
   - Use Roboflow’s annotation tool to draw bounding boxes and label each object.

## Generate a Dataset Version

1. After uploading and annotating, click **"Generate New Dataset"**.
2. Click **"Generate"** to create a dataset version

## Train the YOLO Model

### Export Dataset to Train Locally

1. Go to your **Dataset Version**.
2. Click **"Download Dataset"**.
3. Choose:
   - **Format**: YOLOv*
   - **Download Code**: Roboflow provides a Python script snippet to download the dataset with an API key.
   - **Download Zip**: Instead of the code download the dataset as a zip. (This can be a large amount depending on dataset size)
4. Use the command:
   ```bash
   pip install roboflow
   ```
## Clone GitHub Repository

1. Clone the project repository from GitHub
   ```bash
   git clone https://github.com/LangTowl/gunshot-detection.git
   cd gunshot-detection
   ```
## Configure the Dataset

1. Unzip it into the **datasets/** directory within the repository
2. Your file structure once unzipped should appear similar to:

![File Structure](https://i.postimg.cc/qvFpYjhs/File-Structure.png)

## Train the Model

1. Install the needed libraries using:
```bash
pip install -r requirements.txt
```
If you didn't already.

2. Run the **model_generator.ipynb** notebook
3. This will create a new **runs/detect/train** folder with training logs, metrics, and model checkpoints.
