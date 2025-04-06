import cv2

class DrawLine:
    def __init__(self, frame):
        self.drawing = False
        self.start_point = (0, 0)
        self.end_point = (0, 0)
        self.coordinates = []
        self.frame = frame

    def draw(self):
        def draw_line(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.drawing = True
                self.start_point = (x, y)

            elif event == cv2.EVENT_MOUSEMOVE:
                if self.drawing:
                    img_copy = self.frame.copy()
                    cv2.line(img_copy, self.start_point, (x, y), (0, 255, 0), 2)
                    cv2.imshow("Image", img_copy)

            elif event == cv2.EVENT_LBUTTONUP:
                self.drawing = False
                self.end_point = (x, y)
                cv2.line(self.frame, self.start_point, self.end_point, (0, 255, 0), 2)
                self.coordinates.append((self.start_point, self.end_point))
                cv2.imshow("Image", self.frame)

        cv2.namedWindow('Image')
        cv2.setMouseCallback('Image', draw_line)

        cv2.imshow('Image', self.frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print(self.coordinates)
        return self.coordinates