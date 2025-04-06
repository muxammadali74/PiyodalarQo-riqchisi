import os
import time

class Logger:
    def __init__(self, log_dir = 'resources/logs/'):
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f"log_{time.strftime('%Y%m%d')}.txt")
    def log_events(self, event=None):
        with open(self.log_file, 'a') as file:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            if event:
                file.write(f"[{timestamp}] {event}\n")

# import cv2
# mat = cv2.cuda_GpuMat()
# print(type(mat))



