# Automated Traffic Violation Detection System

An AI-powered computer vision system designed to automatically detect and record selected traffic violations from video footage using **YOLOv8, PyTorch, OpenCV, and ByteTrack**.

## Overview

The **Automated Traffic Violation Detection System** uses deep learning and computer vision techniques to analyze traffic video footage and automatically identify specific road violations with minimal manual intervention.

The system focuses on four core functionalities:

* Helmet violation detection
* License plate detection and recognition
* Traffic signal violation detection
* Triple-riding detection

Detected violations can be recorded along with relevant vehicle, timestamp, confidence, and evidence information for further analysis.

## Key Features

### 1. Helmet Violation Detection

Detects two-wheeler riders and determines whether they are wearing a helmet.

* Helmet and no-helmet detection using YOLOv8
* Identification of riders without helmets
* Violation event generation
* Evidence frame capture

### 2. License Plate Detection and Recognition

Detects and extracts the license plate associated with a vehicle.

* License plate localization
* Number plate extraction
* License plate recognition
* Association of plate information with detected violations

### 3. Traffic Signal Violation Detection

Identifies vehicles that cross a predefined stop line while the traffic signal is red.

* Traffic signal state identification
* Vehicle detection using YOLOv8
* Vehicle tracking using ByteTrack
* Stop-line based violation detection
* Automatic violation logging

### 4. Triple-Riding Detection

Detects cases where three or more individuals are travelling on a two-wheeler.

* Person detection using YOLOv8
* Rider-to-vehicle association
* Identification of three or more riders
* Automatic violation logging

## Technology Stack

### Programming Language

* Python 3

### Deep Learning Frameworks

* PyTorch
* Ultralytics YOLOv8

### Computer Vision and Data Processing

* OpenCV
* NumPy
* Pandas
* Matplotlib

### Object Tracking

* ByteTrack

### Dataset Annotation

* LabelImg
* Roboflow

### Core Concepts

* Object Detection
* Object Tracking
* Computer Vision
* Deep Learning
* Video Analytics
* Traffic Violation Detection

## System Architecture

```text
Traffic Video / CCTV Footage
            |
            v
      Video Processing
          (OpenCV)
            |
            v
       YOLOv8 Detection
            |
            v
       ByteTrack Tracking
            |
            v
     Violation Detection
            |
     +------+------+------+
     |      |      |      |
     v      v      v      v
  Helmet  Signal  Triple  License
Violation Violation Riding  Plate
     |      |      |      |
     +------+------+------+
            |
            v
    Violation Verification
            |
            v
    Evidence & Violation Log
```

## How the System Works

1. Traffic video footage is provided as the system input.
2. OpenCV reads and processes the video frame by frame.
3. YOLOv8 detects relevant objects such as vehicles, motorcycles, helmets, and persons.
4. ByteTrack assigns and maintains unique tracking IDs across consecutive frames.
5. Detection results are processed using predefined traffic-violation rules.
6. The system identifies applicable violations:

   * No helmet
   * Red-light violation
   * Triple riding
7. The license plate of the associated vehicle is detected and extracted when visible.
8. The detected violation is associated with the corresponding vehicle or tracking ID.
9. Violation information and evidence frames are recorded for further analysis.

## Project Structure

```text
TRAFFIC-MANAGEMENT-SYSTEM/
│
├── backend/
│   ├── models/
│   ├── app.py
│   ├── database.py
│   ├── detection.py
│   ├── number_plate.py
│   └── violation.py
│
├── frontend/
│   ├── assets/
│   ├── components/
│   └── app.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/snehala24/Traffic-Management-System.git

cd Traffic-Management-System
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Model Setup

Place the required YOLOv8 model weights inside:

```text
backend/models/
```

Ensure that the model paths used in the application correspond to the actual model files.

### 5. Run the Application

```bash
python backend/app.py
```

If the frontend is implemented as a separate application, run it using its corresponding entry point.

## Model Training

Custom traffic datasets can be used to train and fine-tune the YOLOv8 detection models.

The general workflow is:

```text
Dataset Collection
        |
        v
Image Annotation
(LabelImg / Roboflow)
        |
        v
Dataset Preparation
        |
        v
YOLOv8 Model Training
        |
        v
Model Validation
        |
        v
Traffic Video Testing
```

## Performance Evaluation

The system can be evaluated using standard object-detection and video-processing metrics, including:

* Precision
* Recall
* F1-score
* Mean Average Precision (mAP)
* Processing speed (FPS)
* False-positive rate

Performance depends on factors such as the training dataset, model configuration, hardware, video resolution, lighting, camera angle, and traffic density.

## Output

For each detected violation, the system can record information such as:

```text
Violation Type
Vehicle / Tracking ID
License Plate
Timestamp
Confidence Score
Evidence Frame
```

Example:

```text
Violation Type : No Helmet
Vehicle ID     : 27
License Plate  : TN XX XXXX
Timestamp      : 00:02:31
Confidence     : 0.91
Evidence       : violation_27.jpg
```

## Applications

The system can serve as a prototype for:

* Automated traffic surveillance
* Smart-city traffic monitoring
* Road-safety monitoring
* Traffic violation analysis
* CCTV-based vehicle monitoring
* AI-assisted traffic monitoring systems

## Future Enhancements

Potential improvements include:

* Integration with live CCTV cameras
* Improved license plate recognition
* Additional traffic violation categories
* Real-time monitoring dashboard
* Cloud deployment
* Mobile application integration
* Improved detection under low-light conditions
* Improved performance in crowded traffic scenarios
* Integration with additional traffic management systems

## Limitations

Detection performance may vary depending on:

* Camera angle
* Video quality
* Lighting conditions
* Vehicle density
* Occlusion
* License plate visibility
* Weather conditions
* Quality and diversity of training data

The system is intended as an AI-based traffic monitoring prototype and should be thoroughly validated before deployment in real-world traffic enforcement environments.

## License

This project is intended for **academic and educational purposes**.
