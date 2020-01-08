import cv2
import numpy as np

frame = cv2.imread('images/road.jpg', cv2.IMREAD_UNCHANGED)
# Resize image if it is too large
if frame.shape[0] > 720 and frame.shape[1] > 960:
	frame = cv2.resize(frame, (1080, 720), cv2.INTER_LANCZOS4)

frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
kernel = np.ones((5, 5), np.uint8)
frame_grey_dilated = cv2.dilate(frame_grey, kernel, iterations=1)
frame_grey_blur = cv2.GaussianBlur(frame_grey_dilated, (5, 5), 0)

# Generate Houghlines
edges = cv2.Canny(frame_grey_dilated, 50, 150)
rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 10  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 10  # minimum number of pixels making up a line
max_line_gap = 10  # maximum gap in pixels between connectable line segments
line_image = np.copy(frame) * 0  # creating a blank to draw lines on

lines = cv2.HoughLinesP(
	edges, rho, theta, threshold, np.array([]),
	min_line_length, max_line_gap
)

print(lines)
points = []
for line in lines:
	for x1, y1, x2, y2 in line:
		points.append(((x1 + 0.0, y1 + 0.0), (x2 + 0.0, y2 + 0.0)))
		cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 2)

lines_edges = cv2.addWeighted(frame, 1, line_image, 1, 0)

cv2.imshow("eroded", frame_grey_dilated)
cv2.imshow("lines", lines_edges)

cv2.waitKey(0)
cv2.destroyAllWindows()