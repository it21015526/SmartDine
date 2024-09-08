import cv2
import time
from ultralytics import YOLO

class Task1Model:
    def __init__(self, video_path):
        self.model = YOLO('models/task1.pt')
        self.video_path = video_path
        self.detection_times = {}

    def detect_objects(self, frame):
        results = self.model.predict(frame)
        return results

    def is_waiter(self, frame, box):
        x1, y1, x2, y2 = map(int, box)
        person = frame[y1:y2, x1:x2]

        template = cv2.imread("template/template.jpeg")
        if person.shape[0] < template.shape[0] or person.shape[1] < template.shape[1]:
            template = cv2.resize(template, (person.shape[1], person.shape[0]))

        result = cv2.matchTemplate(person, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        return max_val >= 0.5

    def process_frame(self, frame):
        results = self.detect_objects(frame)

        if 'seated' in results and 'order_start' not in self.detection_times:
            self.detection_times['order_start'] = time.time()

        if 'ordering' in results and 'order_start' in self.detection_times and 'order_end' not in self.detection_times:
            self.detection_times['order_end'] = time.time()

        if 'food_arrived' in results and 'order_end' in self.detection_times and 'food_arrival' not in self.detection_times:
            self.detection_times['food_arrival'] = time.time()

    def get_seating_time(self):
        if 'order_start' in self.detection_times:
            return round(self.detection_times['order_start'], 2)
        else:
            return 'N/A'

    def get_order_receive_time(self):
        if 'order_end' in self.detection_times:
            return round(self.detection_times['order_end'], 2)
        else:
            return 'N/A'

    def calculate_total_dining_time(self):
        total_dining_time = (
            self.detection_times.get('food_arrival', 0) - self.detection_times.get('order_start', 0)
        )
        return total_dining_time if total_dining_time > 0 else 'N/A'

    def process_video(self):
        cap = cv2.VideoCapture(self.video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            self.process_frame(frame)

        cap.release()
        if 'order_start' in self.detection_times and 'order_end' in self.detection_times:
            wait_time = self.detection_times['order_end'] - self.detection_times['order_start']
            print(f"Time to Place an Order: {wait_time:.2f} seconds")

        if 'bill_request' in self.detection_times and 'bill_delivered_time' in self.detection_times:
            bill_time = self.detection_times['bill_delivered_time'] - self.detection_times['bill_request']
            print(f"Time to Receive the Bill: {bill_time:.2f} seconds")

        if 'order_end' in self.detection_times and 'food_arrival' in self.detection_times:
            receive_order_time = self.detection_times['food_arrival'] - self.detection_times['order_end']
            print(f"Time to Receive the Order: {receive_order_time:.2f} seconds")

        self.calculate_total_dining_time()
