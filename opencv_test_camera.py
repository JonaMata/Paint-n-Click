import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
	ret, frame = cap.read()
	frame_hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
	frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	frame_grey_blur = cv2.GaussianBlur(frame_grey, (5, 5), 0)

	edges = cv2.Canny(frame_grey, 50, 150)
	rho = 1  # distance resolution in pixels of the Hough grid
	theta = np.pi / 180  # angular resolution in radians of the Hough grid
	threshold = 15  # minimum number of votes (intersections in Hough grid cell)
	min_line_length = 50  # minimum number of pixels making up a line
	max_line_gap = 20  # maximum gap in pixels between connectable line segments
	line_image = np.copy(frame) * 0  # creating a blank to draw lines on

	lines = cv2.HoughLinesP(
		edges, rho, theta, threshold, np.array([]),
		min_line_length, max_line_gap
	)

	print(lines)

	# White Mask
	lower = np.uint8([0, 200, 0])
	upper = np.uint8([255, 255, 255])
	white_mask = cv2.inRange(frame_hls, lower, upper)

	# Grey Mask
	lower = np.uint8([0, 0, 0])
	upper = np.uint8([255, 100, 255])
	grey_mask = cv2.inRange(frame_hls, lower, upper)

	# Combine Masks
	mask = cv2.bitwise_or(white_mask, grey_mask)

	cv2.imshow("mask", mask)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
