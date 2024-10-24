# Project Title: Animal Face Recognition and Image Storage System

## Overview
Animal Face Recognition and Image Storage System is a Python-based application that captures images of animals through the usage of a drone or webcam. It reads faces from the captured images and identifies duplicates to subsequently upload images securely to a Vultr S3 bucket.

## Building and Deploying

### Prerequisites
- **Python 3.6 or above**
- **Pip** (package installer for Python)

Installation Steps
1. Clone the repository 
    ```bash
    git clone https://github.com/yourusername/animal-face-recognition.git
    cd animal-face-recognition


2.python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


3.pip install opencv-python boto3


Download the Haar Cascade Model Download haarcascade_frontalface_default.xml from the OpenCV repository and place it in the project directory.

Configure Vultr S3 Credentials Update the vultr_access_key, vultr_secret_key, and vultr_bucket_name variables in the main.py file with your Vultr S3 credentials.

