import cv2
import os
import numpy as np

# Directory containing the extracted frames
frames_directory = "./extracted_frames"
# Directory to save the cropped object images
objects_directory = "./objects"
# Subdirectories for each object type
person_directory = os.path.join(objects_directory, "person")
chair_directory = os.path.join(objects_directory, "chair")
table_directory = os.path.join(objects_directory, "table")

# Ensure the directories exist
os.makedirs(person_directory, exist_ok=True)
os.makedirs(chair_directory, exist_ok=True)
os.makedirs(table_directory, exist_ok=True)

def save_cropped_object(frame, box, label, output_dir):
    x1, y1, x2, y2 = map(int, box)
    cropped_image = frame[y1:y2, x1:x2]
    output_path = os.path.join(output_dir, f"{label}_{x1}_{y1}_{x2}_{y2}.jpg")
    cv2.imwrite(output_path, cropped_image)

def detect_objects(frame):
    boxes = []
    labels = []

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color ranges and masks for detection
    # Example color ranges for detection (These need to be tuned for your specific case)
    # Person detection (assuming skin color range for simplicity)
    lower_skin = np.array([0, 48, 80], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    mask_skin = cv2.inRange(hsv, lower_skin, upper_skin)

    # Chair detection (assuming a color range for chairs)
    lower_chair = np.array([0, 0, 0], dtype=np.uint8)
    upper_chair = np.array([180, 255, 30], dtype=np.uint8)
    mask_chair = cv2.inRange(hsv, lower_chair, upper_chair)

    # Table detection (assuming white color range for tables)
    lower_table = np.array([0, 0, 200], dtype=np.uint8)
    upper_table = np.array([180, 20, 255], dtype=np.uint8)
    mask_table = cv2.inRange(hsv, lower_table, upper_table)

    # Find contours and bounding boxes
    contours_skin, _ = cv2.findContours(mask_skin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_skin:
        x, y, w, h = cv2.boundingRect(contour)
        boxes.append((x, y, x+w, y+h))
        labels.append('person')

    contours_chair, _ = cv2.findContours(mask_chair, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_chair:
        x, y, w, h = cv2.boundingRect(contour)
        boxes.append((x, y, x+w, y+h))
        labels.append('chair')

    contours_table, _ = cv2.findContours(mask_table, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_table:
        x, y, w, h = cv2.boundingRect(contour)
        boxes.append((x, y, x+w, y+h))
        labels.append('table')

    return boxes, labels

# Loop through all directories in the frames directory
for video_name in os.listdir(frames_directory):
    video_path = os.path.join(frames_directory, video_name)
    if os.path.isdir(video_path):
        for frame_filename in sorted(os.listdir(video_path)):
            frame_path = os.path.join(video_path, frame_filename)
            frame = cv2.imread(frame_path)

            # Detect objects in the frame
            boxes, labels = detect_objects(frame)

            # Save cropped images for each detected object
            for box, label in zip(boxes, labels):
                if label == 'person':
                    save_cropped_object(frame, box, label, person_directory)
                elif label == 'chair':
                    save_cropped_object(frame, box, label, chair_directory)
                elif label == 'table':
                    save_cropped_object(frame, box, label, table_directory)

print("Cropped object images saved successfully.")
