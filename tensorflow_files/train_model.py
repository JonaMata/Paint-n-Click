from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
tf.compat.v1.enable_eager_execution()
import tensorflow_datasets as tfds

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D

from os import listdir
from os.path import isfile, join

data_path = '../custom_dataset'
data_files = [f for f in listdir(data_path) if isfile(join(data_path, f))]

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

num_examples = 2820365

SPLIT_WEIGHTS = (8, 2)

num_train, num_val = (num_examples * weight/10 for weight in SPLIT_WEIGHTS)

raw_dataset = tf.data.TFRecordDataset(data_files)
feature_description = {
    'image': tf.io.FixedLenFeature([], tf.int64, default_value=0),
    'label': tf.io.FixedLenFeature([], tf.int64, default_value=0)
}

def _parse_function(example_proto):
    return tf.io.parse_single_example(example_proto, feature_description)

dataset = raw_dataset.map(_parse_function)


print(dataset)
raw_train = dataset.take(num_train)
raw_val = dataset.take(num_val)

shuffle_batch_size = 32
batch_size = 8
epochs = 100
input_shape = (28, 28, 1)
num_classes = 345

model = Sequential([
    Conv2D(batch_size//4, kernel_size=(3, 3), activation='relu', input_shape=input_shape),
    Conv2D(batch_size//2, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Flatten(),
    Dense(batch_size, activation='relu'),
    Dropout(0.5),
    Dense(num_classes, activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss=tf.keras.losses.sparse_categorical_crossentropy,
              metrics=['accuracy'])

model.summary()

print(raw_train.element_spec[0].shape)

history = model.fit(
    raw_train.shuffle(shuffle_batch_size).batch(batch_size),
    epochs=epochs,
    steps_per_epoch=num_train//batch_size//epochs,
    validation_data=raw_val.shuffle(shuffle_batch_size).batch(batch_size),
    validation_steps=num_val//batch_size
)

model.save('quickdraw_model_new.h5')

