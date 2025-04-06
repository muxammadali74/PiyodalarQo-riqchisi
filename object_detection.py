import torch
from ultralytics import YOLO



class ObjectDetector:
    def __init__(self, model_path):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = YOLO(model_path)
        self.model.to(self.device)
        print("Модель запущена на устройстве:", self.model.device)

    def detect(self, frame, classes=[0, 2]):
        results = self.model.predict(frame, classes=classes)
        return results
