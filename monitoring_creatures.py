import os
import cv2
import hashlib
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Configure Vultr S3
vultr_access_key = '3H2HAUNH39DJP1W0DHUN'  # Replace with  actual access key
vultr_secret_key = 'n6APq7ecPADQbAKXhPoMtTpEkeq6XktRSXV2obiU'  # Replace with vultr actual secret key
vultr_bucket_name = 'images'  # Replace with  Vultr bucket name
vultr_endpoint = 'https://del1.vultrobjects.com/'  # Vultr Object Storage endpoint

# Create a session and S3 resource
session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    aws_access_key_id=vultr_access_key,
    aws_secret_access_key=vultr_secret_key,
    endpoint_url=vultr_endpoint
)



# Function to upload files to Vultr
def upload_to_vultr(file_name, object_name=None):
    if object_name is None:
        object_name = file_name

    
    # Check if the file exists
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



# Function to capture image from the drone (or webcam)
def capture_image_from_drone():
    # Use the appropriate video source (0 is the default webcam)
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("animal_image.jpg", frame)  # Save the captured image
        print("Image captured: animal_image.jpg")
    else:
        print("Error: Failed to capture image.")
    cap.release()


# Load face recognition model (OpenCV's pre-trained model)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


# Function to recognize animal face in the image
def recognize_animal_face(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        print("Animal face detected.")
        return True
    else:
        print("No animal face detected.")
        return False


# Set to store unique face hashes
stored_faces = set()


# Function to detect if the captured image is a duplicate
def detect_duplicate_face(image_path):
    img = cv2.imread(image_path)
    img_hash = hashlib.md5(img).hexdigest()  # Create a hash of the image

    if img_hash in stored_faces:
        print("Duplicate animal face detected.")
        return True
    else:
        print("New animal face detected, storing in the database.")
        stored_faces.add(img_hash)
        return False


# Main function to execute the complete process
def main():
    # Step 1: Capture Image
    capture_image_from_drone()

    # Step 2: Upload the image to Vultr
    # Step 3: Recognize Animal Face
    if recognize_animal_face("animal_image.jpg"):
        # Step 4: Check for Duplicates
        if not detect_duplicate_face("animal_image.jpg"):
            # Step 5: Upload to Vultr Cloud if not a duplicate
            upload_to_vultr("animal_image.jpg")



# Run the main program
if __name__ == "__main__":
    main()
