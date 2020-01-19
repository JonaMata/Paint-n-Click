from tensorflow import keras
import tensorflow_datasets as tfds
import cv2
import numpy as np

SPLIT_WEIGHTS = (8, 1, 1)
splits = tfds.Split.TRAIN.subsplit(weighted=SPLIT_WEIGHTS)

(raw_train, raw_val, raw_test), metadata = tfds.load('quickdraw_bitmap',
                                                     split=list(splits),
                                                     data_dir=".\dataset",
                                                     as_supervised=True,
                                                     with_info=True)

classes = metadata.features['label'].names

model = keras.models.load_model('quickdraw_model.h5')

image = cv2.imread('test_image.bmp')
grayscale = np.array([cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)])

grayscale = grayscale.reshape(grayscale.shape[0], 28, 28, 1)

prediction = model.predict_classes(grayscale)

print(classes[prediction[0]])
