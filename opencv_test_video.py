import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	resized = cv2.resize(gray, (28, 28), cv2.INTER_CUBIC)

	cv2.imshow('compressed', resized)
	cv2.imshow('input', frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()