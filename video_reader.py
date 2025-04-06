import cv2


class VideoReader:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path)


    def is_opened(self):
        if not self.cap.isOpened():
            print("Ошибка: не удалось открыть видео.")

        return self.cap.isOpened()

    def read_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Ошибка: не удалось считать кадр.")
        return frame

    def release(self):
        self.cap.release()

