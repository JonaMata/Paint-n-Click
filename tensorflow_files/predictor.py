from tensorflow import keras
import numpy as np

used_labels = [
        'axe',
        'cat',
        'car',
        'bicycle',
        'feather',
        'cloud',
        'tree',
        'peanut',
        'mountain',
        'stop_sign',
        'smiley_face',
        'castle',
        'crown',
        'key',
        'pencil',
        'fireplace',
        'fish',
        'hand',
        'saw',
        'snorkel',
        'star'
    ]

model = keras.models.load_model('tensorflow_files/quickdraw_model.h5')


def predict_drawing(image):
    processed = image.reshape(28, 28, 1)
    input = np.array([processed])
    prediction = model.predict_classes(input)
    extra_prediction = model.predict(input)[0]
    top_values_index = sorted(range(len(extra_prediction)), key=lambda i: extra_prediction[i])[-1:]
    predicted_classes = [used_labels[i] for i in np.flip(top_values_index)]
    return predicted_classes
