import numpy as np
import cv2
from tensorflow_files.predictor import predict_drawing


class DrawingCamera:
	def __init__(self):
		self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
		width, height = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		size_diff = (width - height) // 2
		self.y1, self.y2, self.x1, self.x2 = 0, height, size_diff, width - size_diff

		self.prediction = None
		self.frame = None

	def update(self):
		ret, frame = self.cap.read()

		crop_frame = frame[self.y1:self.y2, self.x1:self.x2]
		gray_frame = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
		kernel = np.ones((8, 8), np.uint8)
		dilated_frame = cv2.erode(gray_frame, kernel)
		resized_frame = cv2.resize(dilated_frame, (28, 28), cv2.INTER_NEAREST)
		preview_frame = cv2.resize(resized_frame, (200, 200), cv2.INTER_NEAREST)

		self.prediction = predict_drawing(resized_frame)
		self.prediction = " "
		self.frame = crop_frame
		cv2.imshow("input preview", preview_frame)

	def get_frame(self):
		return self.frame

	def get_prediction(self):
		print(self.prediction)
		return self.prediction

	def release(self):
		self.cap.release()
		cv2.destroyAllWindows()
