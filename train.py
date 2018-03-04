"""
    File name: train.py
    Function Des:

    ~~~~~~~~~~

    author: Skyduy <cuteuy@gmail.com> <http://skyduy.me>

"""
import os
import numpy as np
from keras import layers
from keras.callbacks import Callback, ModelCheckpoint
from keras.models import Model
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from utils import load_data, APPEARED_LETTERS


def prepare_data(folder):
    print('... loading data')
    letter_num = len(APPEARED_LETTERS)
    data, label = load_data(folder)
    data_train, data_test, label_train, label_test = \
        train_test_split(data, label, test_size=0.1, random_state=0)
    label_categories_train = to_categorical(label_train, letter_num)
    label_categories_test = to_categorical(label_test, letter_num)
    label_categories_train = label_categories_train.reshape((4,-1,letter_num))
    label_categories_test = label_categories_test.reshape((4,-1,letter_num))
    return (data_train, label_categories_train,
            data_test, label_categories_test)


def build_model():
    print('... construct network')
    inputs = layers.Input((60, 120, 3))
    x = layers.Conv2D(32, 9, activation='relu')(inputs)
    x = layers.Conv2D(32, 9, activation='relu')(x)
    x = layers.MaxPool2D((2, 2))(x)
    x = layers.Dropout(0.25)(x)
    x = layers.Flatten()(x)
    x = layers.Dense(640)(x)
    x = layers.Dropout(0.5)(x)
    out1 = layers.Dense(len(APPEARED_LETTERS), activation='softmax')(x)
    out2 = layers.Dense(len(APPEARED_LETTERS), activation='softmax')(x)
    out3 = layers.Dense(len(APPEARED_LETTERS), activation='softmax')(x)
    out4 = layers.Dense(len(APPEARED_LETTERS), activation='softmax')(x)

    return Model(inputs=inputs, outputs=[out1, out2, out3, out4])


def train(pic_folder, weight_folder):
    if not os.path.exists(weight_folder):
        os.makedirs(weight_folder)
    x_train, y_train, x_test, y_test = prepare_data(pic_folder)
    model = build_model()

    print('... compile models')
    model.compile(
        optimizer='adadelta',
        loss=['categorical_crossentropy', 'categorical_crossentropy', 'categorical_crossentropy', 'categorical_crossentropy'],
        metrics=['accuracy'],
    )

    print('... begin train')

    check_point = ModelCheckpoint(
        os.path.join(weight_folder, '{epoch:02d}.hdf5'))
    print(y_train.shape)
    model.fit(
        x_train, [y_train[0], y_train[1], y_train[2], y_train[3]], batch_size=64, epochs=100,
        validation_split=0.1, callbacks=[check_point],
    )


if __name__ == '__main__':
    train(
        pic_folder='images',
        weight_folder='models'
    )
