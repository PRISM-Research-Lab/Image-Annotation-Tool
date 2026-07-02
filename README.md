# Image-Annotation-Tool
A lightweight Python/OpenCV annotation tool for creating image classification datasets from high-resolution images. Supports manual ROI selection, custom labels, automatic dataset organization, and fixed-size crop generation for deep learning.


# 🍅 Tomato Image Annotation Tool

A lightweight Python-based image annotation tool for creating image classification datasets from high-resolution tomato plant images.

This tool was developed for agricultural AI projects and educational research. It allows users to manually crop regions of interest (ROIs) from RGB images and automatically organize them into labeled folders for deep learning model training.

---

## Features

- Automatically loads all images from a folder
- Displays large images scaled to fit the screen
- Crops from the **original high-resolution image**
- Saves all crops at a fixed size (default: **224 × 224**)
- Supports multiple user-defined classes
- Automatically creates class folders
- Simple mouse-based annotation
- Keyboard shortcuts for fast labeling
- Perfect for building image classification datasets

---

## Example Workflow

```
Raw Images
      │
      ▼
Open Image Annotation Tool
      │
      ▼
Draw ROI using mouse
      │
      ▼
Press keyboard shortcut
(H = Healthy, D = Disease, ...)
      │
      ▼
Crop saved automatically
      │
      ▼
Dataset/
    Healthy/
    Disease/
    ...
```

---

# Installation

## Step 1. Install Python

Download Python (3.10 or newer)

https://www.python.org/downloads/

During installation, make sure to check:

```
☑ Add Python to PATH
```

---

## Step 2. Clone Repository

```bash
git clone https://github.com/yourusername/TomatoImageAnnotationTool.git

cd TomatoImageAnnotationTool
```

or simply download the ZIP file and extract it.

---

## Step 3. Install Dependencies

Open Command Prompt or PowerShell and run

```bash
python -m pip install opencv-python
```

---

## Folder Structure

```
Project/

│
├── ImageAnnotationTool.py
│
├── raw_images/
│     image1.jpg
│     image2.jpg
│     image3.jpg
│
└── labeled_dataset/
```

---

## Configure Paths

Open **ImageAnnotationTool.py**

Modify

```python
INPUT_IMAGE_FOLDER = "path_to_your_images"

OUTPUT_DATASET_FOLDER = "path_to_save_dataset"
```

Example

```python
INPUT_IMAGE_FOLDER = "D:/TomatoImages"

OUTPUT_DATASET_FOLDER = "D:/Dataset"
```

---

# Running the Tool

Run

```bash
python ImageAnnotationTool.py
```

---

# Mouse Controls

| Action | Description |
|---------|-------------|
| Left Mouse Button | Draw a rectangle around the region of interest |

---

# Keyboard Shortcuts

| Key | Function |
|-----|----------|
| **H** | Save crop as Healthy |
| **D** | Save crop as Disease |
| **A** | Add a new class |
| **R** | Reset current selection |
| **N** | Load next image |
| **Q** | Quit the program |

---

# Adding New Classes

Press

```
A
```

Example

```
Keyboard Shortcut:
m

Class Name:
Magnesium_Deficiency
```

The tool automatically creates

```
Dataset/

Healthy/

Disease/

Magnesium_Deficiency/
```

---

# Output Dataset

Example

```
Dataset/

Healthy/
    IMG001_Healthy_1.jpg
    IMG003_Healthy_2.jpg

Disease/
    IMG001_Disease_3.jpg

Magnesium_Deficiency/
    IMG005_Magnesium_Deficiency_4.jpg
```

---

# Image Quality

The displayed image is resized only for easier viewing.

**Important**

The crop is extracted from the original high-resolution image before being resized.

This preserves maximum image quality.

---

# Crop Size

By default all crops are resized to

```
224 × 224 pixels
```

Change this in

```python
SAVE_CROP_SIZE = (224,224)
```

Examples

```python
SAVE_CROP_SIZE = (256,256)

SAVE_CROP_SIZE = (512,512)

SAVE_CROP_SIZE = (299,299)
```

---

# Recommended Crop Sizes

| Model | Input Size |
|---------|-----------|
| ResNet18 | 224×224 |
| ResNet50 | 224×224 |
| MobileNetV3 | 224×224 |
| EfficientNet-B0 | 224×224 |
| EfficientNet-B3 | 300×300 |
| InceptionV3 | 299×299 |

---

# Tips for Good Dataset Creation

✔ Draw tightly around the leaf or plant region.

✔ Avoid excessive background.

✔ Keep crops consistent.

✔ Balance the number of images in each class.

✔ Verify labels before training AI models.

---

# Dependencies

- Python 3.10+
- OpenCV

Install

```bash
python -m pip install opencv-python
```

---

# Example Applications

This tool can be used for creating datasets for

- Plant disease classification
- Drought stress detection
- Nutrient deficiency classification
- Pest damage detection
- Leaf image datasets
- Greenhouse monitoring
- General image classification projects

---

# Citation

If you use this tool in your research, please cite the corresponding GitHub repository.

---

# License

MIT License

---

Developed for agricultural AI research and educational projects.
