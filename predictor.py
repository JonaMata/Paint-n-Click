from tensorflow import keras
import tensorflow_datasets as tfds
import cv2
import numpy as np

raw_data, metadata = tfds.load('quickdraw_bitmap',
                               data_dir=".\dataset",
                               as_supervised=True,
                               with_info=True)

classes = metadata.features['label'].names

print(classes)

model = keras.models.load_model('quickdraw_model.h5')


def predict_drawing(image):
    processed = image.reshape(28, 28, 1)
    input = np.array([processed])
    prediction = model.predict_classes(input)
    extra_prediction = model.predict(input)[0]
    top_values_index = sorted(range(len(extra_prediction)), key=lambda i: extra_prediction[i])[-5:]
    predicted_classes = [classes[i] for i in np.flip(top_values_index)]
    return predicted_classes
