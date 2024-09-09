import cv2
import os

# Directory containing the MP4 files (relative to the script's location)
video_directory = "./"
# Directory to save the frames (relative to the script's location)
output_directory = "./extracted_frames"
# Number of frames to extract from each video
num_frames_to_extract = 10000

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Loop through all files in the video directory
for filename in os.listdir(video_directory):
    if filename.endswith(".mp4"):
        video_path = os.path.join(video_directory, filename)
        video_name = os.path.splitext(filename)[0]
        
        # Create a directory for each video's frames
        video_output_dir = os.path.join(output_directory, video_name)
        if not os.path.exists(video_output_dir):
            os.makedirs(video_output_dir)
        
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        
        while frame_count < num_frames_to_extract:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Save each frame as a JPEG file
            frame_filename = f"{video_name}_frame_{frame_count:04d}.jpg"
            frame_path = os.path.join(video_output_dir, frame_filename)
            cv2.imwrite(frame_path, frame)
            frame_count += 1
        
        cap.release()

print("Frames extracted successfully.")
