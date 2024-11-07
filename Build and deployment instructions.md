Summary of Build and Deployment Instructions
Set Up Project

Create and activate a virtual environment.
Install dependencies: opencv-python-headless and boto3.
Download YOLO Model Files

Download yolov3.weights, yolov3.cfg, and coco.names and place them in your project directory.
Set Environment Variables

Store Vultr credentials in environment variables (VULTR_ACCESS_KEY, VULTR_SECRET_KEY) for security.
Configure Vultr S3 Bucket in Code

Replace vultr_bucket_name and vultr_endpoint with your bucket’s details in the code.
Run Locally

Run the script locally to capture images, recognize animal faces, and upload non-duplicates to Vultr.
Deploy to Vultr Server (Optional)

Set up a Vultr server, install Python, clone the project, install dependencies, and run the script.
Verify Output

Check console logs and Vultr bucket to ensure functionality and non-duplicate uploads.
This summarizes setting up, running, and optionally deploying the project to a Vultr server.
