import numpy as np
import cv2
from predictor import predict_drawing

cap = cv2.VideoCapture(0)

while True:
	ret, frame = cap.read()

	width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	size_diff = int((width - height)/2)
	y1, y2, x1, x2 = 0, height, size_diff, width-size_diff

	crop_frame = frame[y1:y2, x1:x2]
	gray_frame = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
	kernel = np.ones((8, 8), np.uint8)
	dilated_frame = cv2.erode(gray_frame, kernel)
	resized_frame = cv2.resize(dilated_frame, (28, 28), cv2.INTER_NEAREST)
	preview_frame = cv2.resize(resized_frame, (200, 200), cv2.INTER_NEAREST)
	prediction = predict_drawing(resized_frame)

	cv2.putText(crop_frame, 'Prediction: '+', '.join(np.flip(prediction)),
				(0, 20),
				cv2.FONT_HERSHEY_SIMPLEX,
				0.5,
				(255, 255, 255),
				1)
	cv2.imshow('cropped', crop_frame)
	cv2.imshow('compressed', preview_frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()