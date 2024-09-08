from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import cv2
import time
import os
import json
from ultralytics import YOLO
from t1 import Task1Model
from t2 import Task2Model
from t3 import Task3Model

from ultralytics.engine.results import Results

app = Flask(__name__)
CORS(app)

# Example task models
TASK_MODELS = {
    'task1': Task1Model,
    'task2': Task2Model,
    'task3': Task3Model
}

def generate_frames_and_detections(task_model):
    cap = cv2.VideoCapture(task_model.video_path)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    video = cv2.VideoWriter(task_model.video_path.replace("original", "processed"), fourcc, fps, (width, height))
    
    # font
    font = cv2.FONT_HERSHEY_SIMPLEX

    # fontScale
    fontScale = 1
    
    # Blue color in BGR
    color = (255, 0, 0)

    # Line thickness of 2 px
    thickness = 2

    frame_num = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if isinstance(task_model, (Task1Model, Task2Model)):
            # Detect objects in the frame
            results = task_model.detect_objects(frame)

            classes = task_model.model.names

            for result in results:
                for i, (box, cls, conf) in enumerate(zip(result.boxes.xyxy.int().cpu().tolist(), result.boxes.cls.int().cpu().tolist(), result.boxes.conf.cpu().tolist())):
                    if isinstance(task_model, Task1Model):
                        if classes[cls] == 'person':
                            if task_model.is_waiter(frame, box):
                                label = "waiter".capitalize()
                            else:
                                label = str(f"Customer: Eating, Time: {round(frame_num / fps, 2)}").capitalize()
                                frame = cv2.putText(frame, "Seating time: N/A", (box[0], box[1] + 30), font, fontScale, color, thickness, cv2.LINE_AA)
                                frame = cv2.putText(frame, "Order receive time: N/A", (box[0], box[1] + 60), font, fontScale, color, thickness, cv2.LINE_AA)
                        else:    
                            label = classes[cls].capitalize()
                    
                    elif isinstance(task_model, Task2Model):
                        label = f"{classes[cls].replace('_', ' ')}".capitalize()
                        frame = cv2.putText(frame, "Non-Eating time: N/A", (box[0], box[1] + 30), font, fontScale, color, thickness, cv2.LINE_AA)
                        frame = cv2.putText(frame, "Waiting time: N/A", (box[0], box[1] + 60), font, fontScale, color, thickness, cv2.LINE_AA)
                    
                    else:
                        label = "not supported"
                        
                    frame = cv2.rectangle(frame, tuple(box[:2]), tuple(box[2:]), (0, 0, 255), 2)
                    frame = cv2.putText(frame, str(label), tuple(box[:2]), font, fontScale, color, thickness, cv2.LINE_AA)

        else:
            print(f"Processing frame {frame_num}")

            if not task_model.check_layout(frame, frame_num):
                time_cleaning = round(frame_num / fps, 2)
            
            # time_cleaning = task_model.calculate_time()
            frame = cv2.putText(frame, str(f"Table rearranging time: {time_cleaning} seconds"), (100, 150), font, fontScale, (0, 0, 255), thickness, cv2.LINE_AA)
            frame = cv2.putText(frame, str(f"Table Turnover time: N/A"), (100, 180), font, fontScale, (0, 0, 255), thickness, cv2.LINE_AA)


        frame_num = frame_num + 1
        video.write(frame)
        
    cap.release()
    video.release()

    with open(task_model.video_path.replace("original", "processed"), 'rb') as f:
        yield f.read()


@app.route('/process_video', methods=['POST'])
def process_video():
    # task_type = request.form.get('task_type')
    # video_file = request.files.get('video')
    # model_path = request.form.get('model_path')
    task_type = 'taks1'
    video_file = request.files.get('video')
    model_path = request.form.get('model_path')

    if task_type not in TASK_MODELS:
        return jsonify({'error': 'Invalid task type'}), 400

    if not video_file:
        return jsonify({'error': 'No video file provided'}), 400

    # Save video file temporarily
    video_path = f'tmp/{task_type}/original/{time.time()}_{video_file.filename}'
    # video_path = "tmp/original/VID-20240901-WA0003.mp4"
    os.makedirs(f"tmp/{task_type}/original/", exist_ok=True)
    os.makedirs(f"tmp/{task_type}/processed/", exist_ok=True)
    video_file.save(video_path)

    # Initialize the selected task model
    task_model_class = TASK_MODELS[task_type]
    task_model = task_model_class(video_path)

    # Stream video frame by frame with detection results
    return Response(generate_frames_and_detections(task_model), 
                    mimetype='video/mp4',
                    content_type='video/mp4',
                    direct_passthrough=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
