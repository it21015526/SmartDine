import cv2
import os
from ultralytics import YOLO

# Directory containing the extracted frames
frames_directory = "./extracted_frames"
# Directory to save the annotated frames
annotated_frames_directory = "./annotated_frames"
# Initialize YOLOv8 model
model = YOLO('yolov8n.pt')

# Ensure the output directory exists
if not os.path.exists(annotated_frames_directory):
    os.makedirs(annotated_frames_directory)

def is_waiter(frame, box):
    x1, y1, x2, y2 = map(int, box)
    person = frame[y1:y2, x1:x2]

    # Define regions for shirt and trousers
    shirt_region = person[:int((y2-y1)/2), :]
    trousers_region = person[int((y2-y1)/2):, :]

    # Calculate average colors in the regions
    shirt_color = cv2.mean(shirt_region)[:3]
    trousers_color = cv2.mean(trousers_region)[:3]

    # Check if shirt is blue and trousers are black
    is_shirt_blue = shirt_color[0] > 150 and shirt_color[1] < 100 and shirt_color[2] < 100
    is_trousers_black = trousers_color[0] < 50 and trousers_color[1] < 50 and trousers_color[2] < 50

    return is_shirt_blue and is_trousers_black

def annotate_frame(frame, results):
    detected_tables = []
    detected_chairs = []

    for result in results:
        for i, box in enumerate(result.boxes.xyxy):
            x1, y1, x2, y2 = map(int, box[:4])
            label = result.names[int(result.boxes.cls[i])]

            if label == 'person':
                if is_waiter(frame, (x1, y1, x2, y2)):
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.putText(frame, "Waiter", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(frame, "Customer", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            elif label == 'chair':
                detected_chairs.append((x1, y1, x2, y2))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
                cv2.putText(frame, "Chair", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
            elif label == 'table' or label == 'dining table':
                detected_tables.append((x1, y1, x2, y2))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, "Table", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Ensure tables are detected if they have chairs nearby
    for (tx1, ty1, tx2, ty2) in detected_tables:
        chairs_nearby = [chair for chair in detected_chairs if tx1 < chair[0] < tx2 and ty1 < chair[1] < ty2]
        if chairs_nearby:
            cv2.rectangle(frame, (tx1, ty1), (tx2, ty2), (0, 255, 0), 2)
            cv2.putText(frame, "Table with Chairs", (tx1, ty1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Loop through all directories in the frames directory
for video_name in os.listdir(frames_directory):
    video_path = os.path.join(frames_directory, video_name)
    if os.path.isdir(video_path):
        video_output_dir = os.path.join(annotated_frames_directory, video_name)
        if not os.path.exists(video_output_dir):
            os.makedirs(video_output_dir)

        for frame_filename in sorted(os.listdir(video_path)):
            frame_path = os.path.join(video_path, frame_filename)
            frame = cv2.imread(frame_path)

            # Detect objects in the frame
            results = model(frame)

            # Annotate the frame
            annotate_frame(frame, results)

            # Save the annotated frame in the annotated_frames_directory
            output_frame_path = os.path.join(video_output_dir, frame_filename)
            cv2.imwrite(output_frame_path, frame)

print("Frames annotated and saved successfully.")
