import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import matplotlib.image as mpimg
from imgaug import augmenters as iaa
import cv2
import random
import time
from PIL import Image

from keras.models import Sequential
from keras.layers import Convolution2D,Flatten,Dense
from keras.optimizers import Adam

# def getName(filePath):
#     return filePath.split('\\')[-1]


def importDataInfo(path):
    columns = ['Center', 'Throttle', 'Steering', 'Brake', 'Gear']
    data = pd.read_csv(os.path.join(path, 'driving_log.csv'), names=columns)
    #### REMOVE FILE PATH AND GET ONLY FILE NAME
    # print(getName(data['center'][0]))
    data['Center'] = data['Center']
    # print(data.head())
    print('Total Images Imported', data.shape[0])
    return data


def balanceData(data,display=True):
    nBin = 31
    samplesPerBin = 2000
    hist, bins = np.histogram(data['Steering'], nBin)
    if display:
        center = (bins[:-1] + bins[1:]) * 0.5
        plt.bar(center, hist, width=0.06)
        plt.plot((np.min(data['Steering']), np.max(data['Steering'])), (samplesPerBin, samplesPerBin))
        plt.show()
    removeindexList = []
    for j in range(nBin):
        binDataList = []
        for i in range(len(data['Steering'])):
            if data['Steering'][i] >= bins[j] and data['Steering'][i] <= bins[j + 1]:
                binDataList.append(i)
        binDataList = shuffle(binDataList)
        binDataList = binDataList[samplesPerBin:]
        removeindexList.extend(binDataList)

    print('Removed Images:', len(removeindexList))
    # print(type(removeindexList))
    # print(removeindexList)
    data.drop(data.index[removeindexList], inplace=True)
    print('Remaining Images:', len(data))
    # print(type(data))

    if display:
        hist, _ = np.histogram(data['Steering'], (nBin))
        plt.bar(center, hist, width=0.06)
        plt.plot((np.min(data['Steering']), np.max(data['Steering'])), (samplesPerBin, samplesPerBin))
        plt.show()
    return data


def loadData(path, data):
  imagesPath = []
  steering = []
  throttle = []
  for i in range(len(data)):
    img_name = int(data['Center'][i])
    steer = float(data['Steering'][i])
    throt = float(data['Throttle'][i])

    imagesPath.append( path + 'training_img/' + str(img_name) + ".png")
    steering.append(steer)
    throttle.append(throt)

  imagesPath = np.asarray(imagesPath)
  steering = np.asarray(steering)
  throttle = np.asarray(throttle)

  return imagesPath, steering, throttle

def augmentImage(imgPath,steering):
    img = mpimg.imread(imgPath)
    if np.random.rand() < 0.5:
        pan = iaa.Affine(translate_percent={"x": (-0.1, 0.1), "y": (-0.1, 0.1)})
        img = pan.augment_image(img)
    if np.random.rand() < 0.5:
        zoom = iaa.Affine(scale=(1, 1.2))
        img = zoom.augment_image(img)
    if np.random.rand() < 0.5:
        brightness = iaa.Multiply((0.2, 1.2))
        img = brightness.augment_image(img)
    if np.random.rand() < 0.5:
        img = cv2.flip(img, 1)
        steering = -steering
    return img, steering



def preProcess(img):
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # img = cv2.GaussianBlur(img, (3, 3), 0)

    # cv2.imshow("", img)
    # cv2.waitKey(1)
    # time.sleep(1)
    # img = img[..., np.newaxis]
    img = img/255
    return img


def batchGenerator(imagesPath, steeringList, batchSize, trainFlag):
    print("hello")
    while True:
        imgBatch = []
        steeringBatch = []


        for i in range(batchSize):
            index = random.randint(0, len(imagesPath) - 1)
            if trainFlag:
                img, steering = augmentImage(imagesPath[index], steeringList[index])
            else:
                img = mpimg.imread(imagesPath[index])
                steering = steeringList[index]
            img = preProcess(img)
            imgBatch.append(img)
            steeringBatch.append(steering)
        yield (np.asarray(imgBatch), np.asarray(steeringBatch))


def createModel():
    model = Sequential()

    # # The inputs are 66x200x3(RGB) images with `channels_last` and the batch size is 24.
    # For CNNs that are trained on images, for example, say your dataset is RGB (3-channel) images that are 256x256
    # pixels. A single image can be represented by a 3 x 256 x 256 matrix.If you set your batch size to be 10, that
    # means you’re concatenating 10 images together into a 10 x 3 x 256 x 256 matrix.

    # model.add(Convolution2D(24, (5, 5), (2, 2), input_shape=(66, 200, 3), activation='elu'))
    model.add(Convolution2D(24, (5, 5), (2, 2), input_shape=(66, 200, 4), activation='elu'))
    model.add(Convolution2D(36, (5, 5), (2, 2), activation='elu'))
    model.add(Convolution2D(48, (5, 5), (2, 2), activation='elu'))
    model.add(Convolution2D(64, (3, 3), activation='elu'))
    model.add(Convolution2D(64, (3, 3), activation='elu'))

    model.add(Flatten())

    model.add(Dense(100, activation='elu'))
    model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='elu'))
    model.add(Dense(1))

    model.compile(Adam(lr=0.0001), loss='mse')
    return model

