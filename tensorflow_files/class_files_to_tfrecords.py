import tensorflow as tf
import numpy as np

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


def write_tfrecord(images, labels, label):
    print('Finished importing dataset '+label)
    print('Start flatten creation '+label)
    image_flatten = images.flatten()
    label_flatten = labels.flatten()
    print('Finished flatten creation '+label)
    print('Start feature creation '+label)
    feature = {
        'image': tf.train.Feature(bytes_list=tf.train.BytesList(value=images)),
        'label': tf.train.Feature(int64_list=tf.train.Int64List(value=label_flatten))
    }
    print('Finished Feature creation '+label)
    print('Start train.Example creation '+label)
    example = tf.train.Example(features=tf.train.Features(feature=feature))
    print('Finished train.Example creation '+label)
    print('Start serialization '+label)
    serialized = example.SerializeToString()
    print('Finished Serialization '+label)
    print('Start writing tfrecord '+label)
    writer = tf.io.TFRecordWriter('.\custom_dataset\custom_'+label+'.tfrecord')
    writer.write(serialized)
    writer.close()
    print('Finished writing '+label)


for i in range(len(used_labels)):
    print('Start '+used_labels[i])
    file = join(data_path, [s for s in data_files if used_labels[i] in s][0])
    file_data = np.load(file)
    file_data = np.reshape(file_data, (file_data.shape[0], 28, 28))
    print(file_data.shape)
    image_set = file_data
    label_set = np.array([i] * len(file_data))
    write_tfrecord(image_set, label_set, used_labels[i])
    print('Finished: '+used_labels[i])


