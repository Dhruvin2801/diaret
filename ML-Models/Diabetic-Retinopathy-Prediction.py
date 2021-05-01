# -*- coding: utf-8 -*-
"""Diabetic-Retinopathy-Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sp3mSZuW4a8wiIM0qbhLy4peMLLMv93z
"""

#Imports
# pip install kaggle
from zipfile import ZipFile as z
from google.colab import files

#Kaggle Data Import
files.upload()

# mkdir -p ~/.kaggle
# cp kaggle.json ~/.kaggle/

# chmod 600 ~/.kaggle/kaggle.json

# kaggle datasets download --force -d tanlikesmath/diabetic-retinopathy-resized

file_name = "diabetic-retinopathy-resized.zip"

with z(file_name, 'r') as zi:
  zi.extractall()
  print('done')

from google.colab import drive
drive.mount('/content/drive')

import os
import pandas as pd 
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from glob import glob
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout, Conv2D, MaxPooling2D, Dense, Flatten, BatchNormalization
from sklearn.model_selection import train_test_split

path = "/content/resized_train_cropped/resized_train_cropped"
data = "/content/resized_train_cropped/resized_train_cropped"
print('number of images in total - ',len(os.listdir(data)))

data = pd.read_csv("/content/trainLabels.csv") 
data.head()

data['image_name'] = [i+".jpeg" for i in data['image'].values]
data.head()

train, val = train_test_split(data, test_size=0.15)

train.shape, val.shape

import cv2
def load_color(image):
    image_size = 224
    sigma_X=10
    image = cv2.resize(image, (image_size, image_size))
    image=cv2.addWeighted ( image,4, cv2.GaussianBlur( image , (0,0) , sigma_X) ,-8 ,128)
    return image

data_gen = ImageDataGenerator(rescale=1/255.,
                              zoom_range=0.15,
                              fill_mode='constant',
                              cval=0.,
                              horizontal_flip=True,
                              vertical_flip=True,
                              preprocessing_function=load_color)

# batch size
bs = 128

train_gen = data_gen.flow_from_dataframe(train, 
                                        path,
                                         x_col="image_name", y_col="level", class_mode="raw",
                                         batch_size=bs,
                                         target_size=(224, 224))
val_gen = data_gen.flow_from_dataframe(val,
                                       path,
                                       x_col="image_name", y_col="level", class_mode="raw",
                                       batch_size=bs,
                                       target_size=(224, 224))

from keras.applications.resnet50 import ResNet50
import keras.layers as L
from keras.models import Model

base_model = ResNet50(weights='imagenet',
                   include_top=False,
                   input_shape=(224, 224, 3))

x = base_model.output
x = L.GlobalMaxPooling2D()(x)
x = L.BatchNormalization()(x)
x = L.Dropout(0.2)(x)
x = L.Dense(1024, activation="relu")(x)
x = L.Dropout(0.1)(x)
x = L.Dense(64, activation="relu")(x)
predictions = L.Dense(5, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

for layer in base_model.layers[:-20]: layer.trainable = False

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.summary()

from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau

model_history = model.fit(train_gen, steps_per_epoch=int(29842/128), epochs=2,  validation_data=val_gen, validation_steps=int(5266/128))

#SAVING WEIGHTS

model.save('dr_weights.h5')

#MODEL

accuracyNT = model_history.history['accuracy']
validation_accuracyNT = model_history.history['val_accuracy']
loss_NT = model_history.history['loss']
validation_loss_NT = model_history.history['val_loss']
epochsNT = range(len(accuracyNT))

plt.plot(epochsNT, accuracyNT, 'r', label='Training accuracy')
plt.plot(epochsNT, validation_accuracyNT, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend(loc=0)
plt.figure()

plt.show()

plt.plot(epochsNT, loss_NT, 'r', label='Training loss')
plt.plot(epochsNT, validation_loss_NT, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend(loc=0)
plt.figure()

plt.show()