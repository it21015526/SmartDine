import time
import cv2
import numpy as np
from ultralytics import YOLO

class Task3Model:
    def __init__(self, video_path):
        self.model = None
        self.video_path = video_path
        self.turnover_times = {}
        self.rearrangement_times = {}

    def detect_objects(self, frame):
        results = self.model.predict(frame)
        return results
    
    def check_layout(self, frame, frame_num):
        template = cv2.imread("template/99_1.jpeg")

        if frame.shape[0] < template.shape[0] or frame.shape[1] < template.shape[1]:
            template = cv2.resize(template, (frame.shape[1], frame.shape[0]))

        ##Matching each channel
        result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        return max_val >= 0.77
    
    def set_time(self, time):
        if "start" in self.turnover_times:
            self.turnover_times["stop"] = time
        else:
            self.turnover_times["start"] = time

    def calculate_time(self):
        if "stop" in self.turnover_times and "start" in self.turnover_times:
            return self.turnover_times["stop"] - self.turnover_times["start"]
        else:
            return 0

    def process_frame_for_table_turnover(self, frame):
        results = self.detect_objects(frame)

        if 'table_vacated' in results and 'table_vacated' not in self.turnover_times:
            self.turnover_times['table_vacated'] = time.time()
            print(f"Table vacated at: {self.turnover_times['table_vacated']}")
        elif 'table_occupied' in results and 'table_vacated' in self.turnover_times and 'table_occupied' not in self.turnover_times:
            self.turnover_times['table_occupied'] = time.time()
            print(f"Table occupied at: {self.turnover_times['table_occupied']}")

    def process_frame_for_table_rearrangement(self, frame):
        results = self.detect_objects(frame)

        if 'table_vacated' in results and 'table_vacated' not in self.rearrangement_times:
            self.rearrangement_times['table_vacated'] = time.time()
            print(f"Table vacated for rearrangement at: {self.rearrangement_times['table_vacated']}")
        elif 'table_rearranged' in results and 'table_vacated' in self.rearrangement_times and 'table_rearranged' not in self.rearrangement_times:
            self.rearrangement_times['table_rearranged'] = time.time()
            print(f"Table rearranged at: {self.rearrangement_times['table_rearranged']}")

    def process_video(self):
        cap = cv2.VideoCapture(self.video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Process for table turnover and rearrangement in a single pass
            self.process_frame_for_table_turnover(frame)
            self.process_frame_for_table_rearrangement(frame)

        cap.release()

    def calculate_table_turnover_time(self):
        if 'table_vacated' in self.turnover_times and 'table_occupied' in self.turnover_times:
            table_turnover_time = self.turnover_times['table_occupied'] - self.turnover_times['table_vacated']
            print(f"Table Turnover Time: {table_turnover_time:.2f} seconds")
        else:
            print("Insufficient data to calculate table turnover time.")

    def calculate_table_rearrangement_time(self):
        if 'table_vacated' in self.rearrangement_times and 'table_rearranged' in self.rearrangement_times:
            table_rearrangement_time = self.rearrangement_times['table_rearranged'] - self.rearrangement_times['table_vacated']
            print(f"Table Rearrangement Time: {table_rearrangement_time:.2f} seconds")
        else:
            print("Insufficient data to calculate table rearrangement time.")
