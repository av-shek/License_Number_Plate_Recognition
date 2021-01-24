import cv2
import numpy as np
import math

def preprocess(input_image):
    grayscale_image = extractValue(input_image)
    grayscale_image_with_maximum_contrast = maximizeContrast(grayscale_image)
    height, width = grayscale_image.shape
    
    blurred_image = np.zeros((height, width, 1), np.uint8)
    GAUSSIAN_SMOOTH_FILTER_SIZE = (5, 5)
    blurred_image = cv2.GaussianBlur(grayscale_image_with_maximum_contrast, GAUSSIAN_SMOOTH_FILTER_SIZE, 0)

    ADAPTIVE_THRESH_BLOCK_SIZE = 19
    ADAPTIVE_THRESH_WEIGHT = 9
    threshold_image = cv2.adaptiveThreshold(blurred_image, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)
    return grayscale_image, threshold_image

def extractValue(input_image):
    height, width, Channel = input_image.shape
    HSV_image = np.zeros((height, width, 3), np.uint8)
    HSV_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)
    Hue, Saturation, Value = cv2.split(HSV_image)
    return Value

def maximizeContrast(grayscale_image):
    height, width = grayscale_image.shape

    Top_hat_transform = np.zeros((height, width, 1), np.uint8)      #enhance bright objects in dark background
    Black_hat_transform = np.zeros((height, width, 1), np.uint8)    #enhance dark objects in bright background

    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    Top_hat_transform = cv2.morphologyEx(grayscale_image, cv2.MORPH_TOPHAT, structuringElement)
    Black_hat_transform = cv2.morphologyEx(grayscale_image, cv2.MORPH_BLACKHAT, structuringElement)

    grayscale_image_Plus_TopHat = cv2.add(grayscale_image, Top_hat_transform)
    grayscale_image_Plus_TopHat_Minus_BlackHat = cv2.subtract(grayscale_image_Plus_TopHat, Black_hat_transform)

    return grayscale_image_Plus_TopHat_Minus_BlackHat