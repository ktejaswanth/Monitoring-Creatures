import os
import cv2
import hashlib
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Vultr S3 Configuration (Directly Set Access Keys - Only for Development Purposes)
vultr_access_key = '3H2HAUNH39DJP1W0DHUN'  # Replace with your Vultr access key
vultr_secret_key = 'n6APq7ecPADQbAKXhPoMtTpEkeq6XktRSXV2obiU'  # Replace with your Vultr secret key
vultr_bucket_name = 'images'  # Replace with your Vultr bucket name
vultr_endpoint = 'https://del1.vultrobjects.com/'  # Vultr Object Storage endpoint

# Create a session and S3 resource
session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    aws_access_key_id=vultr_access_key,
    aws_secret_access_key=vultr_secret_key,
    endpoint_url=vultr_endpoint
)

# YOLO Model Paths - update these paths if necessary
yolo_weights = "yolov3.weights"  # Path to YOLO weights file
yolo_config = "yolov3.cfg"  # Path to YOLO config file
labels_file = "coco.names"  # Path to labels file

# Load class labels
with open(labels_file, 'r') as f:
    labels = f.read().strip().split("\n")

# Initialize YOLO model
net = cv2.dnn.readNetFromDarknet(yolo_config, yolo_weights)
output_layers = net.getUnconnectedOutLayersNames()


# Function to upload files to Vultr S3
def upload_to_vultr(file_name, object_name=None):
    if object_name is None:
        object_name = file_name

    if not os.path.exists(file_name):
        print(f"Error: The file '{file_name}' does not exist.")
        return

    try:
        s3.upload_file(file_name, vultr_bucket_name, object_name)
        print(f"{file_name} has been uploaded to {vultr_bucket_name}.")
    except FileNotFoundError:
        print("Error: The file was not found.")
    except NoCredentialsError:
        print("Error: Credentials not available.")
    except PartialCredentialsError:
        print("Error: Partial credentials provided.")
    except Exception as e:
        print(f"An unexpected error occurred during upload: {e}")


# Function to capture image from the webcam
def capture_image_from_drone():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return False

    ret, frame = cap.read()
    cap.release()

    if ret:
        cv2.imwrite("animal_image.jpg", frame)
        print("Image captured: animal_image.jpg")
        return True
    else:
        print("Error: Failed to capture image.")
        return False


# Function to recognize animal face in the image using YOLO
def recognize_animal_face_yolo(image_path):
    img = cv2.imread(image_path)
    height, width = img.shape[:2]

    # Prepare the image for YOLO
    blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(output_layers)

    # Analyze the output
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = int(scores.argmax())
            confidence = scores[class_id]

            # Filter for high-confidence animal detections
            if confidence > 0.5 and labels[class_id] in ["cat", "dog", "bird", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "loin", "tiger"]:  # Add other animals as needed
                print(f"Animal face detected: {labels[class_id]} with confidence {confidence}")
                return True

    print("No animal face detected.")
    return False


# Set to store unique face hashes
stored_faces = set()


# Function to detect if the captured image is a duplicate
def detect_duplicate_face(image_path):
    img = cv2.imread(image_path)
    img_hash = hashlib.md5(img).hexdigest()

    if img_hash in stored_faces:
        print("Duplicate animal face detected.")
        return True
    else:
        print("New animal face detected, storing in the database.")
        stored_faces.add(img_hash)
        return False


# Main function to execute the complete process
def main():
    print("Starting the animal face recognition and upload process...")

    if capture_image_from_drone():
        image_path = "animal_image.jpg"


        if recognize_animal_face_yolo(image_path):
            if not detect_duplicate_face(image_path):
                upload_to_vultr(image_path)


if __name__ == "__main__":
    main()
