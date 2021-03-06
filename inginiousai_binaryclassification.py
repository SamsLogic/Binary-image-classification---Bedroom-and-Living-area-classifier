# -*- coding: utf-8 -*-
"""InginiousAI binaryclassification

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IkAP_4_vy06D8GkomEHRIzeQA-7S_gll

# Import Libraries and load data
"""

import os
import numpy as np
import pandas as pd

import cv2

import tensorflow as tf
import tensorflow.keras.models as M
import tensorflow.keras.layers as L
import tensorflow.keras.optimizers as O
import tensorflow.keras.metrics as ME
import tensorflow.keras.losses as LO

from tqdm.notebook import tqdm

import matplotlib.pyplot as plt

from sklearn.model_selection import KFold

# Getting image file paths

bed_files = os.listdir('/content/drive/MyDrive/inGiniousAI/Images/bedroom')
liv_files = os.listdir('/content/drive/MyDrive/inGiniousAI/Images/livingroom')
bed_files = [os.path.join('/content/drive/MyDrive/inGiniousAI/Images/bedroom', i) for i in bed_files]
liv_files = [os.path.join('/content/drive/MyDrive/inGiniousAI/Images/livingroom', i) for i in liv_files]

# preparing pandas dataframe of image paths

data = dict()
data['images'] = bed_files + liv_files
data['labels'] = [1]*(len(bed_files)) + [0]*(len(liv_files))
data = pd.DataFrame(data)
data = data.sample(frac=1, random_state=45).reset_index(drop=True)

data

"""# A glance into the data"""

data.labels.value_counts()

print('Class count: ')

fig, ax = plt.subplots(2,5, figsize=(10,10))

for i in range(10):
    image = cv2.imread(data.images[i])
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image,(256,256), cv2.INTER_NEAREST)
    ax[i//5,i%5].imshow(image)
    ax[i//5,i%5].axis("off")
    ax[i//5,i%5].set_title(data.labels[i])

plt.subplots_adjust(hspace=0)
fig.tight_layout()
plt.show()

"""# Image preprocessing"""

def preprocessor(image: np.ndarray) -> np.ndarray:
    '''
    Image Preprocessor to preprocess the image for training and prediction

    input: np.ndarray
    output: np.ndarray
    '''

    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    image = cv2.bilateralFilter(image,15, 70, 70)
    # image = cv2.GaussianBlur(image,(3,3),2)
    image = cv2.Canny(image,120,120)
    # ret, image = cv2.threshold(image,150,255,0)
    # image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, (15,15))
    # contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # image = cv2.drawContours(image, contours, -1, (0,255,0), 3)
    image = cv2.dilate(image, (7,7), 5)
    image = cv2.resize(image, (128,128), cv2.INTER_NEAREST)
    return image

image1 = preprocessor(cv2.imread(data.images[11]))
plt.imshow(image1,cmap='gray')
plt.title(data.labels[1])
plt.show()

!mkdir /content/drive/MyDrive/inGiniousAI/Images/preprocesed
!mkdir /content/drive/MyDrive/inGiniousAI/Images/preprocesed/0
!mkdir /content/drive/MyDrive/inGiniousAI/Images/preprocesed/1

file_path = '/content/drive/MyDrive/inGiniousAI/Images/preprocesed'

preprocessed_data = dict()
image_paths = []
label = []
error_img = []
for i in tqdm(range(len(data))):
    image = cv2.imread(data.images[i])
    if type(image) == type(None):
        error_img.append(data.images[i])
        continue
    image = preprocessor(image)
    cv2.imwrite(os.path.join(file_path,str(data.labels[i])+'/'+str(i)+'.jpeg'),image)
    image_paths.append(os.path.join(file_path,str(data.labels[i])+'/'+str(i)+'.jpeg'))
    label.append(data.labels[i])

preprocessed_data['images'] = image_paths
preprocessed_data['labels'] = label
preprocessed_data = pd.DataFrame(preprocessed_data)

preprocessed_data

fig, ax = plt.subplots(3,5, figsize=(10,10))

for i in range(15):
    image = preprocessor(cv2.imread(data.images[i]))
    ax[i//5,i%5].imshow(image,cmap='gray')
    ax[i//5,i%5].axis("off")
    ax[i//5,i%5].set_title(data.labels[i])

fig.tight_layout()
plt.show()

"""# Training

## Global variables
"""

BATCH_SIZE = 16
EPOCHS = 15

"""## Model Architecture"""

def build_model():
    '''
    Model architecure for the classification task

    input:  None
    output: tf.Keras.Model
    '''

    inp = L.Input(shape=(128,128,1,))
    x = L.Conv2D(16,(15,15),padding='same',activation='relu')(inp)
    x = L.MaxPooling2D()(x)
    x = L.BatchNormalization()(x)
    x = L.Conv2D(32,(13,13),padding='same',activation='relu')(x)
    x = L.MaxPooling2D()(x)
    x = L.Dropout(0.3)(x)
    x = L.Add()([x, tf.image.resize(inp, (32,32))])
    x = L.Conv2D(64,(7,7),padding='same',activation='relu')(x)
    x = L.MaxPooling2D()(x)
    x = L.Dropout(0.3)(x)
    x = L.Add()([x, tf.image.resize(inp, (16,16))])
    x = L.Conv2D(128,(5,5),padding='same',activation='relu')(x)
    x = L.MaxPooling2D()(x)
    x = L.Dropout(0.5)(x)
    x = L.BatchNormalization()(x)
    x = L.Conv2D(256,(3,3),padding='same',activation='relu')(x)
    x = L.MaxPooling2D()(x)
    x = L.Dropout(0.5)(x)
    x = L.BatchNormalization()(x)
    x = L.Flatten()(x)
    x = L.Dense(64,activation='relu')(x)
    x = L.Dense(32,activation='relu')(x)
    x = L.Dense(16,activation='relu')(x)
    out = L.Dense(1,activation='sigmoid',kernel_initializer='glorot_uniform')(x)

    model = M.Model(inputs=inp, outputs=out)
    adam = O.Adam(learning_rate=0.001)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=[ME.AUC()])
    return model

model = build_model()
model.summary()

"""## Training with cross validation"""

def load_data(path, labels=None):
    '''
    Function to load data into the system. it is used for dynamic loading of the data incase the data size is more than the available memory

    input: path string, class label
    output: image tensor, class label
    '''

    image = tf.io.decode_jpeg(tf.io.read_file(path), channels=1)
    if labels == None:
        return image
    return image, labels

# KFold cross validation

kf = KFold(n_splits=5)

for ix, (tr_ix,val_ix) in enumerate(kf.split(preprocessed_data.values)):
    print(f"################### FOLD {ix+1} ###################")

    model = build_model()

    tr_dataset = tf.data.Dataset.from_tensor_slices((preprocessed_data.iloc[tr_ix].images.values, preprocessed_data.iloc[tr_ix].labels.values)).map(load_data, num_parallel_calls=tf.data.AUTOTUNE).cache().batch(BATCH_SIZE,drop_remainder=True).repeat().prefetch(tf.data.AUTOTUNE)
    val_dataset = tf.data.Dataset.from_tensor_slices((preprocessed_data.iloc[val_ix].images.values, preprocessed_data.iloc[val_ix].labels.values)).map(load_data, num_parallel_calls=tf.data.AUTOTUNE).cache().batch(BATCH_SIZE,drop_remainder=True).repeat().prefetch(tf.data.AUTOTUNE)

    history = model.fit(tr_dataset,
                        steps_per_epoch=len(tr_ix)//BATCH_SIZE,
                        epochs=EPOCHS,
                        validation_data=val_dataset,
                        validation_batch_size=BATCH_SIZE,
                        validation_steps=len(val_ix)//BATCH_SIZE)
    
    print('Validation data AUC score:', model.evaluate(val_dataset,verbose=0,steps=len(val_ix)//BATCH_SIZE)[1])

"""## Save model"""

model.save('/content/drive/MyDrive/inGiniousAI/model.h5')

"""# Inference

## Load Test Data

The images used for testing are images from captured from my own phone
"""

test_files = os.listdir('/content/drive/MyDrive/inGiniousAI/Images/Test/')

test_files = [os.path.join('/content/drive/MyDrive/inGiniousAI/Images/Test', i) for i in test_files]

"""## Preprocess data"""

test_images = np.zeros((len(test_files),128,128,1))

for i in range(len(test_files)):
    image = cv2.imread(test_files[i])
    image = cv2.resize(image, (256,256))
    test_images[i] = np.expand_dims(preprocessor(image),axis=-1)

fig, ax = plt.subplots(1,len(test_files), figsize=(20,5))

for i in range(len(test_files)):
    ax[i].imshow(np.squeeze(test_images[i],axis=-1))
    ax[i].axis('off')

fig.tight_layout()
plt.show()

"""## Prediction"""

pred = model.predict(test_images)

pred[pred >= 0.5] = 1
pred[pred < 0.5] = 0

"""## Result"""

fig, ax = plt.subplots(1,len(test_files), figsize=(20,5))

for i in range(len(test_files)):
    ax[i].imshow(cv2.cvtColor(cv2.imread(test_files[i]), cv2.COLOR_BGR2RGB))
    ax[i].set_title(f"Predicted: {'Bedroom'*(pred[i][0] == 1) + 'Living room'*(pred[i][0] == 0)}")
    ax[i].axis('off')

fig.tight_layout()
plt.show()