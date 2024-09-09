from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import cv2
import time
import os
import json
import numpy as np
from t1 import Task1Model
from t2 import Task2Model
from t3 import Task3Model

from customerinfo import save_customer_info,get_customer_info
from tableInfo import save_table_info,get_table_info
from interactionInfo import save_interaction_info,get_interaction_info

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
    spf = 1 / fps

    rearrangingTime = 0
    cleaningTime = 0

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

        person_count = 0
        seting_exceed = 0
        order_exceed = 0
        food_exceed = 0
        customer_count = 0
        table_turnover = 0
        nonEmpty  = 0
        waitingTime = 0
        nonEating = 0

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
                                customer_count +=1

                                seating_time = task_model.get_seating_time()
                                order_receive_time = task_model.get_order_receive_time()

                                if (seating_time != 'N/A' and seating_time > 600): #10 minutes
                                            seting_exceed +=1
                                if (order_receive_time != 'N/A' and order_receive_time > 1800): # 30 minutes
                                            food_exceed +=1

                                label = str(f"Customer: {task_model.get_activity(frame, box).capitalize()}, Time: {round(frame_num / fps, 2)}").capitalize()
                                frame = cv2.putText(frame, f"Seating time: {seating_time}", (box[0], box[1] + 30), font, fontScale, color, thickness, cv2.LINE_AA)
                                frame = cv2.putText(frame, f"Order receive time: {order_receive_time}", (box[0], box[1] + 60), font, fontScale, color, thickness, cv2.LINE_AA)
                    
                    elif isinstance(task_model, Task2Model):
                        label = f"{classes[cls].replace('_', ' ')}".capitalize()
                        frame = cv2.rectangle(frame, tuple(box[:2]), tuple(box[2:]), (0, 0, 255), 2)
                        frame = cv2.putText(frame, str(label), tuple(box[:2]), font, fontScale, color, thickness, cv2.LINE_AA)

                        non_eating_duration = task_model.engagement_times.get('non_eating', time.time()) - task_model.engagement_times.get('non_eating_start', time.time())
                        waiting_time_duration = task_model.engagement_times.get('looking_for_assistance', time.time()) - task_model.engagement_times.get('looking_for_assistance_start', time.time())

                        non_eating_text = f"Non-Eating time: {non_eating_duration:.2f} sec" if 'non_eating_start' in task_model.engagement_times else "Non-Eating time: N/A"
                        frame = cv2.putText(frame, non_eating_text, (box[0], box[1] + 30), font, fontScale, color, thickness, cv2.LINE_AA)

                        waiting_text = f"Waiting time: {waiting_time_duration:.2f} sec" if 'looking_for_assistance_start' in task_model.engagement_times else "Waiting time: N/A"
                        frame = cv2.putText(frame, waiting_text, (box[0], box[1] + 60), font, fontScale, color, thickness, cv2.LINE_AA)
                        
                        if (non_eating_duration > 0) :
                            nonEating = non_eating_duration
                        else : 
                            nonEating = 0
                        
                        if (waiting_time_duration > 0):
                            waitingTime = waiting_time_duration
                        else : 
                            waitingTime = 0 

                        if (label == 'Empty' and task_model.engagement_times.get('is_Finish_eating')):
                            nonEmpty +=1

                    elif isinstance(task_model, Task3Model):
                        if classes[cls] == 'person' and not task_model.is_waiter(frame, box):
                            person_count = person_count + 1
                    
                    else:
                        label = "not supported"
                           
        if isinstance(task_model, (Task3Model)):
            print(f"Processing frame {frame_num}")

            if not task_model.check_layout(frame, frame_num):
                rearrangingTime = round(rearrangingTime + spf, 2)
                # cleaningTime = time_cleaning

            table_unclean, bbox = task_model.check_unclean(frame)
            if table_unclean:
                frame = cv2.rectangle(frame, tuple(bbox[:2]), tuple(bbox[2:]), (0, 255, 0), 2)
                frame = cv2.putText(frame, str(f"Not Clean"), tuple(bbox[:2]), font, fontScale, (255, 0, 0), thickness, cv2.LINE_AA)
                cleaningTime = round(cleaningTime + spf, 2)
            
            table_turnover = round(person_count/15, 0)
            frame = cv2.putText(frame, str(f"Table rearranging time: {rearrangingTime} seconds"), (100, 150), font, fontScale, (255, 0, 0), thickness, cv2.LINE_AA)
            frame = cv2.putText(frame, str(f"Table Cleaning time: {cleaningTime}"), (100, 180), font, fontScale, (255, 0, 0), thickness, cv2.LINE_AA)
            frame = cv2.putText(frame, str(f"Table Turnover: {table_turnover}"), (100, 210), font, fontScale, (255, 0, 0), thickness, cv2.LINE_AA)

            with open("C:/Users/Kanishka/Desktop/Smart Dine PP2/SmartDine/Server/Tasks/template/0_1.json", "r") as reader:
                polys = json.load(reader)["shapes"]

            for table, poly in polys.items():
                frame = cv2.putText(frame, table, (int(poly[0][0]), int(poly[0][1])), font, fontScale, (0, 255, 255), thickness, cv2.LINE_AA)
                frame = cv2.polylines(frame, [np.array(poly, dtype=np.int32)], True, (0, 0, 255), 1)

        save_table_info(rearrangingTime, cleaningTime, table_turnover)
        save_interaction_info(nonEmpty, waitingTime, nonEating)
        save_customer_info(customer_count, seting_exceed, order_exceed, food_exceed)
        
        frame_num = frame_num + 1
        video.write(frame)

    cap.release()
    video.release()

    with open(task_model.video_path.replace("original", "processed"), 'rb') as f:
        yield f.read()

        
@app.route('/process_video', methods=['POST'])
def process_video():
    task_type = request.form.get('task_type')
    video_file = request.files.get('video')

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


@app.route('/currentCustomer', methods=['GET'])
def current_customer_count():
    latest_info = get_customer_info()
    
    if latest_info:
        datetime, customer_count, seting_exceed, order_exceed, food_exceed = latest_info
        return jsonify({
            'datetime': datetime,
            'customer_count': customer_count,
            'seting_exceed': seting_exceed,
            'order_exceed': order_exceed,
            'food_exceed': food_exceed
        })
    else:
        return jsonify({'error': 'No data available'}), 404
    
@app.route('/tableInfo', methods=['GET'])
def current_table_turnover():
    latest_info = get_table_info()
    
    if latest_info:
        avg_rearrangingTime, sum_rearrangingTime, avg_cleaningTime, sum_cleaningTime, ttrate,datetime = latest_info
        return jsonify({
            'avg_rearrangingTime': avg_rearrangingTime,
            'sum_rearrangingTime': sum_rearrangingTime,
            'avg_cleaningTime': avg_cleaningTime,
            'sum_cleaningTime': sum_cleaningTime,
            'ttrate': ttrate,
            'datetime' : datetime
        })
    else:
        return jsonify({'error': 'No data available'}), 404

@app.route('/interactionInfo', methods=['GET'])
def current_interaction_info():
    latest_info = get_interaction_info()
    
    if latest_info:
        datetime, nonEmpty, waitingTime, nonEating = latest_info
        return jsonify({
            'datetime': datetime,
            'nonEmpty': nonEmpty,
            'waitingTime': waitingTime,
            'nonEating': nonEating
        })
    else:
        return jsonify({'error': 'No data available'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
