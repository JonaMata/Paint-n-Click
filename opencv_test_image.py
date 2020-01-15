import cv2
import numpy as np

frame = cv2.imread('test_images/heart_whiteboard.jpg', cv2.IMREAD_UNCHANGED)
# Resize image if it is too large
if frame.shape[0] > 720 and frame.shape[1] > 960:
	frame = cv2.resize(frame, (1080, 720), cv2.INTER_LANCZOS4)

frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
kernel = np.ones((5, 5), np.uint8)
frame_grey_dilated = cv2.dilate(frame_grey, kernel, iterations=1)
frame_grey_blur = cv2.GaussianBlur(frame_grey_dilated, (5, 5), 0)

cv2.imshow("eroded", frame_grey_dilated)

cv2.waitKey(0)
cv2.destroyAllWindows()