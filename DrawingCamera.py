import numpy as np
import cv2
from predictor import predict_drawing

class DrawingCamera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        width, height = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        size_diff = (width - height) // 2
        self.y1, self.y2, self.x1, self.x2 = 0, height, size_diff, width - size_diff

    def update(self):
        ret, frame = self.cap.read()

        crop_frame = frame[self.y1:self.y2, self.x1:self.x2]
        gray_frame = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((8, 8), np.uint8)
        dilated_frame = cv2.erode(gray_frame, kernel)
        resized_frame = cv2.resize(dilated_frame, (28, 28), cv2.INTER_NEAREST)

        self.prediction = predict_drawing(resized_frame)
        self.frame = crop_frame

    def getFrame(self):
        return self.frame

    def getPrediction(self):
        return self.prediction