"""
Author: Amr Elsersy
email: amrelsersay@gmail.com
-----------------------------------------------------------------------------------
Description: utils functions
"""
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
import pandas as pd
import cv2

def tensor_to_numpy(image):
    if type(image) != np.ndarray:
        return image.cpu().squeeze().numpy()
    return image


def histogram_equalization(face):
    # return face with hight contrast (bright & dark histograms are distibuted equally)
    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    return cv2.equalizeHist(face)
    

def normalization(face):
    # normalize input face (face - mean)/std
    face = tensor_to_numpy(face)
    # [-1,1] range
    mean = np.mean(face)
    std = np.std(face)

    # if black_image
    if int(mean) == 0 and int(std) == 0:
        return face

    face = (face - mean) / std  
    face = face.astype(np.float32)

    # normalization will change mean/std but will have overflow in max/min values
    face = np.clip(face, -1, 1)
    # convert from [-1,1] range to [0,1]
    face = (face + 1) / 2
    # face = (face * 255).astype(np.uint8)
    return face.astype(np.float32)

def standerlization(image):
    # simple normalization (change ranges)
    image = tensor_to_numpy(image)    
    # standerlization .. convert it to 0-1 range
    min_img = np.min(image)
    max_img = np.max(image)
    image = (image - min_img) / (max_img - min_img)
    return image.astype(np.float32)
