from ultralytics import YOLO
from PIL import Image
import numpy as np

class FoodDetector:
    def __init__(self):
        self.model = YOLO('yolov8n')
    
    def detect_food(self, image):
        results = self.model(image)
        return Image.fromarray(results[0].plot()), results[0]
