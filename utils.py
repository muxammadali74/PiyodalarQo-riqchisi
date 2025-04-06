import time

import cv2
import numpy as np


def calculate_fps(prev_time):
    new_time = time.time()
    fps = int(1 / (new_time - prev_time))
    return fps, new_time

def draw_polygon(frame, points, color=(0, 255, 0), thickness=2):
    points = [tuple(pt) for pt in points]
    cv2.polylines(frame, [np.array(points)], isClosed=True, color=color, thickness=thickness)
