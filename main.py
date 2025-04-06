# main.py
import sys
import threading
import cv2
import numpy as np
from config import Config
from coordinatesPedestrianCrossing import DrawLine
from gui_handler import GUIHAndler
from object_detection import ObjectDetector
from video_reader import VideoReader
from collections import deque

def main():
    config = Config()

    video_reader = VideoReader(config.video_path)
    object_detector = ObjectDetector(config.model_path)
    gui_handler = GUIHAndler(width=config.width, height=config.height)

    frame = video_reader.read_frame()
    if frame is not None:
        frame = cv2.resize(frame, (config.width, config.height))
        draw = DrawLine(frame)
        # saved_coordinates = draw.draw()
        saved_coordinates = [((826, 469), (1175, 460)), ((1175, 460), (1276, 470)), ((1276, 470), (924, 484)), ((924, 484), (828, 470)), ((800, 470), (870, 486)), ((869, 484), (155, 541)), ((155, 541), (113, 510)), ((113, 510), (801, 468))]
        pedestrian_zone = np.array([pt for line in saved_coordinates for pt in line], dtype=np.int32)
    else:
        print("Ошибка: не удалось загрузить кадр для отметки зоны.")
        return

    direction1_zone = pedestrian_zone[:len(pedestrian_zone) // 2]
    direction2_zone = pedestrian_zone[len(pedestrian_zone) // 2:]

    logged_vehicles = set()
    logged_pedestrians = set()

    stop_threads = threading.Event()

    def calculate_fps(prev_time):
        new_time = cv2.getTickCount() / cv2.getTickFrequency()
        fps = 1 / (new_time - prev_time)
        return fps, new_time

    def detection_loop():
        prev_time = cv2.getTickCount() / cv2.getTickFrequency()
        buffer_size = 300  # 10 секунд при 30 FPS
        frame_buffer = deque(maxlen=buffer_size)

        recording_violation = False
        violation_frames_remaining = 0
        violation_clip_buffer = []

        last_violation_time = 0
        cooldown_seconds = 5  # чтобы избежать частого срабатывания

        while video_reader.is_opened():
            frame = video_reader.read_frame()
            if frame is None:
                print("Видео закончилось или кадр не удалось считать.")
                stop_threads.set()
                break
            frame = cv2.resize(frame, (config.width, config.height))
            # frame_buffer.append(frame)

            # Нарисовать зону
            if pedestrian_zone.size > 0:
                frame = gui_handler.draw_fill_polygon(frame, direction1_zone, direction2_zone, 0.2, (0, 255, 0))

            pedestrian_in_dir1 = pedestrian_in_dir2 = car_in_dir1 = car_in_dir2 = False

            results = object_detector.detect(frame, classes=[0, 2])

            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                    cls = int(box.cls[0].item())

                    if cls == 0:  # Пешеход
                        is_in_dir1 = gui_handler.check_point_inside_zone(x1, y2, direction1_zone)
                        is_in_dir2 = gui_handler.check_point_inside_zone(x1, y2, direction2_zone)
                        pedestrian_in_dir1 |= is_in_dir1
                        pedestrian_in_dir2 |= is_in_dir2
                        color = (0, 0, 255) if is_in_dir1 or is_in_dir2 else (255, 0, 0)
                        gui_handler.draw_rectangle(frame, (x1, y1, x2, y2), True, color, (0, 0, 255))
                    elif cls == 2:  # Машина
                        is_in_dir1 = gui_handler.check_point_inside_zone(x1, y2, direction1_zone)
                        is_in_dir2 = gui_handler.check_point_inside_zone(x1, y2, direction2_zone)
                        car_in_dir1 |= is_in_dir1
                        car_in_dir2 |= is_in_dir2
                        color = (0, 0, 255) if is_in_dir1 or is_in_dir2 else (255, 0, 0)
                        gui_handler.draw_rectangle(frame, (x1, y1, x2, y2), True, color, (0, 0, 255))

            current_time = cv2.getTickCount() / cv2.getTickFrequency()

            violation_detected = (
                    (pedestrian_in_dir1 and car_in_dir1) or
                    (pedestrian_in_dir2 and car_in_dir2)
            )
            frame_buffer.append(frame.copy())

            if violation_detected and not recording_violation and (
                    current_time - last_violation_time > cooldown_seconds):
                gui_handler.show_violation(frame)
                gui_handler.save_screenshot(frame, "violation_detected")
                recording_violation = True
                violation_frames_remaining = 300  # 10 секунд после
                violation_clip_buffer = list(frame_buffer)
                last_violation_time = current_time

            if recording_violation:
                violation_clip_buffer.append(frame)
                violation_frames_remaining -= 1
                if violation_frames_remaining <= 0:
                    gui_handler.save_violation_clip(violation_clip_buffer)
                    print("Клип нарушения сохранён.")
                    recording_violation = False
                    violation_clip_buffer = []

            # FPS
            fps, prev_time = calculate_fps(prev_time)
            gui_handler.draw_fps(frame, fps)

            # Показ
            gui_handler.update_frame(frame, results)



    detection_thread = threading.Thread(target=detection_loop)

    detection_thread.start()

    detection_thread.join()

    video_reader.release()

    gui_handler.close()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        cv2.setUseOptimized(True)
        main()
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    else:
        sys.exit(0)
