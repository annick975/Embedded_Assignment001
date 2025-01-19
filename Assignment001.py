import os
import time
import shutil
import subprocess

# Configuration
MONITOR_FOLDER = "./captured_pictures"  # Folder where the camera saves pictures
UPLOADED_FOLDER = "./uploaded"           # Folder to move uploaded pictures
UPLOAD_URL = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"
UPLOAD_INTERVAL = 30                     # Time in seconds before uploading

# Ensure folders exist
os.makedirs(MONITOR_FOLDER, exist_ok=True)
os.makedirs(UPLOADED_FOLDER, exist_ok=True)

def upload_image(file_path):
    try:
        # Use the curl command to upload the image
        response = subprocess.run(
            [
                "curl", "-X", "POST", "-F", f"imageFile=@{file_path}", UPLOAD_URL
            ],
            capture_output=True, text=True
        )
        # Check if the upload was successful (check for specific success message)
        if response.returncode == 0 and "successfully uploaded" in response.stdout:
            print(f"[SUCCESS] Uploaded: {file_path}")
            return True
        else:
            print(f"[FAILURE] Upload failed for: {file_path}\nResponse: {response.stdout}")
            return False
    except Exception as e:
        print(f"[ERROR] An error occurred while uploading {file_path}: {e}")
        return False

def monitor_and_upload():
    print("[INFO] Monitoring folder for new pictures...")
    while True:
        # Get a list of files in the monitor folder
        files = [f for f in os.listdir(MONITOR_FOLDER) if os.path.isfile(os.path.join(MONITOR_FOLDER, f))]
        
        for file_name in files:
            file_path = os.path.join(MONITOR_FOLDER, file_name)
            uploaded_path = os.path.join(UPLOADED_FOLDER, file_name)

            # Skip if the file is already uploaded
            if os.path.exists(uploaded_path):
                print(f"[INFO] File already uploaded: {file_name}")
                continue

            # Wait before uploading the file
            print(f"[INFO] Waiting {UPLOAD_INTERVAL} seconds before uploading {file_name}...")
            time.sleep(UPLOAD_INTERVAL)

            # Upload the file
            if upload_image(file_path):
                # Move the file to the uploaded folder
                shutil.move(file_path, uploaded_path)
                print(f"[INFO] Moved {file_name} to {UPLOADED_FOLDER}")
            else:
                print(f"[WARNING] Skipping moving {file_name} due to upload failure.")

        # Sleep for a while before scanning the folder again
        time.sleep(5)

if __name__ == "__main__":
    monitor_and_upload()
