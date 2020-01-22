# Paint-n-Click
A point 'n click like game involving physically drawing the key objects to get them into the game to solve the puzzles.

Using Quick Draw bitmaps dataset to identify doodles with Tensorflow: https://www.tensorflow.org/datasets/catalog/quickdraw_bitmap  

We used the following tutorial for the TensorFlow model: https://github.com/tensorflow/docs/blob/master/site/en/r1/tutorials/sequences/recurrent_quickdraw.md  

For the input of the model we use OpenCV to resize a webcam input to 28x28 grayscale.
as you can see in [drawing_camera.py](drawing_camera.py)
```
crop_frame = frame[self.y1:self.y2, self.x1:self.x2]
gray_frame = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
kernel = np.ones((8, 8), np.uint8)
dilated_frame = cv2.erode(gray_frame, kernel)
resized_frame = cv2.resize(dilated_frame, (28, 28), cv2.INTER_NEAREST)
```
![](assets/gif/capture_cat.gif)

The objective of the game is to answer the questions or riddles to be able to continue to the next level  
![](assets/gif/capture_intro.gif)