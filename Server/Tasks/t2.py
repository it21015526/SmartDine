import cv2
import time
import numpy as np
from ultralytics import YOLO

class Task2Model:
    def __init__(self, video_path):
        self.model = YOLO('models/task2.pt')
        self.video_path = video_path
        self.detection_times = {}
        self.initial_food_areas = []
        self.engagement_times = {
            'non_eating_duration': 0,
            'waiting_duration': 0
        }

    def detect_objects(self, frame):
        results = self.model.predict(frame)
        return results

    def estimate_food_area(self, frame, plate_bbox):
        x, y, w, h = plate_bbox
        roi = frame[y:y+h, x:x+w]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        food_area = cv2.countNonZero(thresh)
        return food_area

    def update_durations(self):
        """ Updates non-eating and waiting time based on the engagement times. """
        current_time = time.time()

        # Non-eating time (using phone)
        if 'non_eating_start' in self.engagement_times:
            non_eating_time = current_time - self.engagement_times['non_eating_start']
            self.engagement_times['non_eating_duration'] = non_eating_time
        
        # Waiting time (looking for assistance)
        if 'looking_for_assistance_start' in self.engagement_times:
            waiting_time = current_time - self.engagement_times['looking_for_assistance_start']
            self.engagement_times['waiting_duration'] = waiting_time

    def process_frame(self, frame):
        # Detect objects in the frame
        results = self.detect_objects(frame)

        # Process food waste estimation
        for result in results:
            if result['label'] == 'plate':
                plate_bbox = result['bbox']
                food_area = self.estimate_food_area(frame, plate_bbox)
                timestamp = time.time()

                if 'initial_food_area' not in self.detection_times:
                    self.detection_times['initial_food_area'] = food_area
                    self.detection_times['initial_timestamp'] = timestamp
                    print(f"Initial Food Area detected at {timestamp}: {food_area}")
                else:
                    self.initial_food_areas.append((timestamp, food_area))
                    print(f"Food Area at {timestamp}: {food_area}")

        # Process engagement detection
        for result in results:
            if result['label'] == 'eating':
                if 'eating_start' not in self.engagement_times:
                    self.engagement_times['eating_start'] = time.time()
                    print(f"Eating started at: {self.engagement_times['eating_start']}")
                self.engagement_times['eating'] = time.time()

            elif result['label'] == 'phone':
                if 'non_eating_start' not in self.engagement_times:
                    self.engagement_times['non_eating_start'] = time.time()
                    print(f"Phone usage started at: {self.engagement_times['non_eating_start']}")
                self.engagement_times['non_eating'] = time.time()

            elif result['label'] == 'looking_around':
                if 'looking_for_assistance_start' not in self.engagement_times:
                    self.engagement_times['looking_for_assistance_start'] = time.time()
                    print(f"Looking for assistance started at: {self.engagement_times['looking_for_assistance_start']}")
                self.engagement_times['looking_for_assistance'] = time.time()

        # Update non-eating and waiting durations after processing the frame
        self.update_durations()

    def process_video(self):
        cap = cv2.VideoCapture(self.video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            self.process_frame(frame)

        cap.release()

    def calculate_food_waste(self):
        initial_area = self.detection_times.get('initial_food_area', 0)
        final_area = self.initial_food_areas[-1][1] if self.initial_food_areas else 0
        leftover_area = initial_area - final_area
        print(f"Initial Food Area: {initial_area}, Final Food Area: {final_area}, Leftover Area: {leftover_area}")

    def calculate_engagement_durations(self):
        eating_duration = self.engagement_times.get('eating', 0) - self.engagement_times.get('eating_start', 0)
        non_eating_duration = self.engagement_times.get('non_eating_duration', 0)
        waiting_duration = self.engagement_times.get('waiting_duration', 0)

        print(f"Eating Duration: {eating_duration:.2f} seconds")
        print(f"Non-Eating (Phone) Duration: {non_eating_duration:.2f} seconds")
        print(f"Waiting for Assistance Duration: {waiting_duration:.2f} seconds")


