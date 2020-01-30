import tensorflow as tf
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D

from os import listdir
from os.path import isfile, join

data_path = '../dataset/downloads'
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

image_set = []
label_set = []

for i in range(len(used_labels)):
    print('Start '+used_labels[i])
    file = join(data_path, [s for s in data_files if used_labels[i] in s][0])
    file_data = np.load(file)
    file_data = np.reshape(file_data, (file_data.shape[0], 28, 28, 1))
    image_set.extend(file_data)
    label_set.extend([i] * len(file_data))
    print('Finished: '+used_labels[i])


num_examples = 2820365
SPLIT_WEIGHTS = (9.5, 0.5)
num_train, num_val = (num_examples * weight/10 for weight in SPLIT_WEIGHTS)

print('Creating dataset')
dataset = tf.data.Dataset.from_tensor_slices((image_set, label_set)).shuffle(num_examples)
print(dataset)

print('Splitting dataset')
train_dataset = dataset.take(int(num_train))
val_dataset = dataset.skip(int(num_train))
print(train_dataset)
print(val_dataset)

shuffle_batch_size = 128
batch_size = 128
epochs = 5
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
    Dense(len(used_labels), activation='softmax')
])

print('Compiling model')
model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss=tf.keras.losses.sparse_categorical_crossentropy,
              metrics=['accuracy'])

model.summary()

print('Training model')
history = model.fit(
    train_dataset.batch(batch_size),
    epochs=epochs,
    steps_per_epoch=num_train//batch_size//epochs,
    validation_data=val_dataset.batch(batch_size),
    validation_steps=num_val//batch_size
)

print('Saving model')
model.save('quickdraw_model.h5')
