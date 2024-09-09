import os

# Directory containing the extracted frames
frames_directory = "./extracted_frames"

# Loop through all directories in the frames directory
for video_name in os.listdir(frames_directory):
    video_path = os.path.join(frames_directory, video_name)
    if os.path.isdir(video_path):
        frame_count = len([name for name in os.listdir(video_path) if os.path.isfile(os.path.join(video_path, name))])
        print(f"{video_name}: {frame_count} frames")
