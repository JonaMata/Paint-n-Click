import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
	ret, frame = cap.read()
	width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	size_diff = int((width - height)/2)
	y1, y2, x1, x2 = 0, height, size_diff, width-size_diff
	crop_frame = frame[y1:y2, x1:x2]
	gray_frame = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
	resized_frame = cv2.resize(gray_frame, (28, 28), cv2.INTER_CUBIC)

	cv2.imshow('cropped', crop_frame)
	cv2.imshow('compressed', resized_frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()