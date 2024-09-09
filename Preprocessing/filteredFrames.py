import cv2
import os
from ultralytics import YOLO
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim

# Directory containing the extracted frames
frames_directory = "./extracted_frames"
# Threshold for duplicate frame detection
duplicate_threshold = 0.95

# Initialize YOLOv8 model
model = YOLO('yolov8n.pt')

def is_duplicate(frame1, frame2, threshold=duplicate_threshold):
    # Convert frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    # Compute Structural Similarity Index (SSI)
    score, _ = compare_ssim(gray1, gray2, full=True)
    return score > threshold

def has_movement(frame, model):
    results = model(frame)
    for result in results:
        if len(result.boxes) > 0:
            return True
    return False

# Loop through all directories in the frames directory
for video_name in os.listdir(frames_directory):
    video_path = os.path.join(frames_directory, video_name)
    if os.path.isdir(video_path):
        previous_frame = None

        for frame_filename in sorted(os.listdir(video_path)):
            frame_path = os.path.join(video_path, frame_filename)
            frame = cv2.imread(frame_path)

            if previous_frame is not None and is_duplicate(previous_frame, frame):
                os.remove(frame_path)
                continue

            if not has_movement(frame, model):
                os.remove(frame_path)
                continue

            previous_frame = frame

print("Outlier frames removed successfully.")
