import cv2
import numpy as np
import math
import Main
import random

import Preprocess
import DetectChars
import PossiblePlate
import PossibleChar

def detectPlatesInScene(input_image):
    Possible_Plates = []

    height, width, Channels = input_image.shape

    threshold_image = np.zeros((height, width, 1), np.uint8)
    grayscale_image, threshold_image = Preprocess.preprocess(input_image)    
    # cv2.imshow("grayscale", grayscale_image)
    # cv2.imshow("threshold", threshold_image)

    #finds all contours, then only includes contours that could be chars (without comparison to other chars yet)
    Possible_Chars = get_Possible_Chars_in_input_image(threshold_image)

    # given a list of all possible chars, find groups of matching chars
    Matching_Chars = DetectChars.findListOfListsOfMatchingChars(Possible_Chars)
    for listOfMatchingChars in Matching_Chars:                 
        possiblePlate = extractPlate(input_image, listOfMatchingChars)         
        if possiblePlate.imgPlate is not None:                          
            Possible_Plates.append(possiblePlate)                  

    return Possible_Plates

def get_Possible_Chars_in_input_image(threshold_image):
    Possible_Chars = []  
    Possible_Chars_Count = 0

    threshold_image_copy = threshold_image.copy()
    contours, npaHierarchy = cv2.findContours(threshold_image_copy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(0, len(contours)):
        possibleChar = PossibleChar.PossibleChar(contours[i])
        if DetectChars.checkIfPossibleChar(possibleChar):                   
            Possible_Chars_Count = Possible_Chars_Count + 1           
            Possible_Chars.append(possibleChar)                        

    return Possible_Chars

def extractPlate(input_image, listOfMatchingChars):
    possiblePlate = PossiblePlate.PossiblePlate()
    
    listOfMatchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)        # sort chars from left to right based on x position

    plate_center_X = (listOfMatchingChars[0].intCenterX + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterX) / 2.0
    plate_center_Y = (listOfMatchingChars[0].intCenterY + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY) / 2.0
    plate_center = plate_center_X, plate_center_Y

    plate_width = int((listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectX + listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectWidth - listOfMatchingChars[0].intBoundingRectX) * 1.3)

    total_char_heights = 0
    for matchingChar in listOfMatchingChars:
        total_char_heights = total_char_heights + matchingChar.intBoundingRectHeight

    average_char_height = total_char_heights / len(listOfMatchingChars)
    plate_height = int(average_char_height * 1.5)

    opposite = listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY - listOfMatchingChars[0].intCenterY
    hypotenuse = DetectChars.distanceBetweenChars(listOfMatchingChars[0], listOfMatchingChars[len(listOfMatchingChars) - 1])
    correction_angle_radian = math.asin(opposite / hypotenuse)
    correction_angle_degree = correction_angle_radian * (180.0 / math.pi)
    possiblePlate.rrLocationOfPlateInScene = ( tuple(plate_center), (plate_width, plate_height), correction_angle_degree )

    rotationMatrix = cv2.getRotationMatrix2D(tuple(plate_center), correction_angle_degree, 1.0)
    height, width, Channels = input_image.shape

    rotated_image = cv2.warpAffine(input_image, rotationMatrix, (width, height))  
    cropped_image = cv2.getRectSubPix(rotated_image, (plate_width, plate_height), tuple(plate_center))
    possiblePlate.imgPlate = cropped_image         

    return possiblePlate