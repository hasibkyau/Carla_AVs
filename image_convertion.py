# import pandas as pd
# from sklearn.model_selection import train_test_split

from sklearn.model_selection import train_test_split
import matplotlib.image as mpimg
from PIL import Image
# import the modules
import os
import cv2
import time
from os import listdir

# get the path/directory
folder_dir = "E:/CARLA_0.9.5/PythonAPI/MyProject/carla_dataset/_IMG/"
folder_dir2 = "E:/CARLA_0.9.5/PythonAPI/MyProject/carla_dataset/"

def imgPreProcess(img):

    img = cv2.resize(img, (640, 480))
    # img2 = np.uint8(img)
    img = img[200:440, :, :]
    # img = img[250:480, :, :]

    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    # img = cv2.GaussianBlur(img, (3, 3), 0)

    # img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # yuv_img = cv2.GaussianBlur(yuv_img, (3, 3), 0)
    # hsv_img = cv2.GaussianBlur(hsv_img, (3, 3), 0)
    # img = cv2.GaussianBlur(img, (3, 3), 0)


    img = cv2.resize(img, (200, 66))
    # img = img[..., np.newaxis]
    # img = img/255
    # print(img)
    return img



for images in os.listdir(folder_dir):

    # check if the image ends with png
    if (images.endswith(".png")):

        path = folder_dir + images
        print(images)
        img = mpimg.imread(path)
        img = imgPreProcess(img)
        # mpimg.imsave(folder_dir2+"training_img/" + "1" + images, img)
        cv2.imshow("", img)
        cv2.waitKey(1)
        # time.sleep(2)
        # print(img.shape)