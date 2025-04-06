import datetime
import cv2
import time
import numpy as np
from config import Config

class GUIHAndler:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window_name = 'Violation Detection'
        self.config = Config()

    def update_frame(self, frame, results):
        cv2.imshow(self.window_name, frame)
        cv2.waitKey(1)

    def close(self):
        cv2.destroyAllWindows()

    def check_point_inside_zone(self, x, y, zone, invert=False):
        point = (x, y)
        rect = np.array(zone, dtype=np.int32)
        return cv2.pointPolygonTest(rect, point, False) >= 0 if not invert else False

    def draw_rectangle(self, frame, coords, is_violation, violation_color, normal_color):
        color = violation_color if is_violation else normal_color
        x1, y1, x2, y2 = coords
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    def show_violation(self, frame):
        # pass
        cv2.putText(frame, "Qoyda buzarlik qayd etildi", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    def save_violation_clip(self, buffer, fps=30):
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.config.output_video}/violation_clip_{now}.avi"
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        height, width, _ = buffer[0].shape
        out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
        for frame in buffer:
            out.write(frame)
        out.release()
        print(f"Клип сохранён: {filename}")

    def save_screenshot(self, frame, violation_type):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"{self.config.output_images}/{violation_type}_{timestamp}.png"
        cv2.imwrite(filename, frame)

    def draw_fps(self, frame, fps):
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    def draw_fill_polygon(self, frame, polygon1, polygon2, alpha, color):
        overlay = frame.copy()
        mask = np.zeros_like(frame, dtype=np.uint8)

        cv2.fillPoly(mask, [polygon1], color)
        cv2.fillPoly(mask, [polygon2], color)


        frame = cv2.addWeighted(mask, alpha, frame, 1 - alpha, 0)

        return frame