import os
import shutil
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from ultralytics import YOLO
import sys

# Increase the recursion limit
sys.setrecursionlimit(3000)

# Set directories
base_dir = './objects'
dataset_dir = './dataset'
train_images_dir = os.path.join(dataset_dir, 'images', 'train')
val_images_dir = os.path.join(dataset_dir, 'images', 'val')
train_labels_dir = os.path.join(dataset_dir, 'labels', 'train')
val_labels_dir = os.path.join(dataset_dir, 'labels', 'val')

# Create required directories
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)

# Define the classes you want to detect
classes = ['table', 'plate', 'food_arrived', 'bill_requested', 'bill_delivered', 'seated', 'ordering', 'phone', 'looking_around']

# Dummy bounding box generator (replace with actual labeling logic)
def generate_dummy_bounding_box(image):
    height, width, _ = image.shape
    print(f"Image shape: {image.shape}")
    x_center = width / 2
    y_center = height / 2
    box_width = width / 4
    box_height = height / 4
    bbox = [x_center / width, y_center / height, box_width / width, box_height / height]
    print(f"Generated bbox: {bbox}")
    return bbox

# Prepare dataset
def prepare_dataset(class_name, files, images_dir, labels_dir):
    class_dir = os.path.join(base_dir, class_name)
    for file in files:
        image_path = os.path.join(class_dir, file)
        image = cv2.imread(image_path)

        if image is None:
            raise ValueError(f"Could not load image: {image_path}")

        # Save image
        shutil.copy(image_path, os.path.join(images_dir, file))

        # Generate dummy label file
        bbox = generate_dummy_bounding_box(image)
        label_file = file.replace('.jpg', '.txt').replace('.jpeg', '.txt').replace('.png', '.txt')
        label_path = os.path.join(labels_dir, label_file)
        with open(label_path, 'w') as f:
            class_index = classes.index(class_name)
            f.write(f"{class_index} {' '.join(map(str, bbox))}\n")

# Iterate over each class and prepare the dataset
for class_name in classes:
    class_dir = os.path.join(base_dir, class_name)
    if not os.path.exists(class_dir):
        print(f"Class directory {class_dir} does not exist, skipping class {class_name}")
        continue

    class_images = [f for f in os.listdir(class_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    if not class_images:
        print(f"No images found for class {class_name}, skipping.")
        continue

    train_files, val_files = train_test_split(class_images, test_size=0.2, random_state=42)
    prepare_dataset(class_name, train_files, train_images_dir, train_labels_dir)
    prepare_dataset(class_name, val_files, val_images_dir, val_labels_dir)

# Create YAML configuration file
yaml_content = f"""
train: {os.path.abspath(train_images_dir)}
val: {os.path.abspath(val_images_dir)}

nc: {len(classes)}
names: {classes}
"""
with open('custom_dataset.yaml', 'w') as f:
    f.write(yaml_content)

# Train the YOLOv8 model
model = YOLO('yolov8n.pt')
model.train(data='custom_dataset.yaml', epochs=50, imgsz=640)

print("Training complete.")
