import os
import cv2
import numpy as np
import math
import random
import Main
import Preprocess
import PossibleChar

kNearest = cv2.ml.KNearest_create()

def KNN_data_loading_and_training():
    try:
        Classifications = np.loadtxt("KNN_Dataset/classifications.txt", np.float32)                  
    except:                                                                                 
        print("Unable to open classifications.txt\n")  
        return False                                                                   

    try:
        FlattenedImages = np.loadtxt("KNN_Dataset/flattened_images.txt", np.float32)                 
    except:                                                                                 
        print("Unable to open flattened_images.txt\n")  
        os.system("pause")
        return False                                                                        

    Classifications = Classifications.reshape((Classifications.size, 1))       
    kNearest.setDefaultK(1)                                                             
    kNearest.train(FlattenedImages, cv2.ml.ROW_SAMPLE, Classifications)           
    return True                             

MIN_PIXEL_WIDTH = 2
MIN_PIXEL_HEIGHT = 8
MIN_ASPECT_RATIO = 0.25
MAX_ASPECT_RATIO = 1.0
MIN_PIXEL_AREA = 80
MIN_DIAG_SIZE_MULTIPLE_AWAY = 0.3
MAX_DIAG_SIZE_MULTIPLE_AWAY = 5.0
MAX_CHANGE_IN_AREA = 0.5
MAX_CHANGE_IN_WIDTH = 0.8
MAX_CHANGE_IN_HEIGHT = 0.2
MAX_ANGLE_BETWEEN_CHARS = 12.0
MIN_NUMBER_OF_MATCHING_CHARS = 3
RESIZED_CHAR_IMAGE_WIDTH = 20
RESIZED_CHAR_IMAGE_HEIGHT = 30
MIN_CONTOUR_AREA = 100

def detectCharsInPlates(Possible_plates_list):
    plate_counter = 0
    imgContours = None
    contours = []

    if len(Possible_plates_list) == 0:         
        return Possible_plates_list            

    for possiblePlate in Possible_plates_list:          
        possiblePlate.imgGrayscale, possiblePlate.imgThresh = Preprocess.preprocess(possiblePlate.imgPlate)     
        
        # increase size of plate image for easier viewing and char detection
        possiblePlate.imgThresh = cv2.resize(possiblePlate.imgThresh, (0, 0), fx = 1.6, fy = 1.6)
        threshold_Value, possiblePlate.imgThresh = cv2.threshold(possiblePlate.imgThresh, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        Possible_chars = get_Possible_chars(possiblePlate.imgGrayscale, possiblePlate.imgThresh)
        Matching_chars = findListOfListsOfMatchingChars(Possible_chars)

        if (len(Matching_chars) == 0):
            possiblePlate.strChars = ""
            continue				

        for i in range(0, len(Matching_chars)):                              
            Matching_chars[i].sort(key = lambda matchingChar: matchingChar.intCenterX)        
            Matching_chars[i] = remove_innerOverlapping_chars(Matching_chars[i])              

        length_of_max_chars = 0
        index_of_max_chars = 0
        for i in range(0, len(Matching_chars)):
            if len(Matching_chars[i]) > length_of_max_chars:
                length_of_max_chars = len(Matching_chars[i])
                index_of_max_chars = i

        longest_list_matching_chars = Matching_chars[index_of_max_chars]
        possiblePlate.strChars, possiblePlate.imgThresh = recognizeCharsInPlate(possiblePlate.imgThresh, longest_list_matching_chars)
    return Possible_plates_list

def get_Possible_chars(grayscale_image, threshold_image):
    Possible_Chars = []                       
    contours = []
    threshold_image_copy = threshold_image.copy()

    contours, npaHierarchy = cv2.findContours(threshold_image_copy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:                        
        possibleChar = PossibleChar.PossibleChar(contour)

        if checkIfPossibleChar(possibleChar):              
            Possible_Chars.append(possibleChar)       
    return Possible_Chars


def checkIfPossibleChar(possibleChar):
    if (possibleChar.intBoundingRectArea > MIN_PIXEL_AREA and
        possibleChar.intBoundingRectWidth > MIN_PIXEL_WIDTH and possibleChar.intBoundingRectHeight > MIN_PIXEL_HEIGHT and
        MIN_ASPECT_RATIO < possibleChar.fltAspectRatio and possibleChar.fltAspectRatio < MAX_ASPECT_RATIO):
        return True
    else:
        return False


def findListOfListsOfMatchingChars(listOfPossibleChars):
    listOfListsOfMatchingChars = []                  

    for possibleChar in listOfPossibleChars:                        
        listOfMatchingChars = findListOfMatchingChars(possibleChar, listOfPossibleChars)        
        listOfMatchingChars.append(possibleChar)                

        if len(listOfMatchingChars) < MIN_NUMBER_OF_MATCHING_CHARS:     
            continue                            

        listOfListsOfMatchingChars.append(listOfMatchingChars)

        listOfPossibleCharsWithCurrentMatchesRemoved = []
        listOfPossibleCharsWithCurrentMatchesRemoved = list(set(listOfPossibleChars) - set(listOfMatchingChars))

        recursiveListOfListsOfMatchingChars = findListOfListsOfMatchingChars(listOfPossibleCharsWithCurrentMatchesRemoved)      
        for recursiveListOfMatchingChars in recursiveListOfListsOfMatchingChars:        
            listOfListsOfMatchingChars.append(recursiveListOfMatchingChars)             
        break

    return listOfListsOfMatchingChars


def findListOfMatchingChars(possibleChar, listOfChars):
    listOfMatchingChars = []                

    for possibleMatchingChar in listOfChars:                
        if possibleMatchingChar == possibleChar:    
            continue                               
        
        distance_between_chars = distanceBetweenChars(possibleChar, possibleMatchingChar)
        angle_between_chars = angleBetweenChars(possibleChar, possibleMatchingChar)
        change_in_area = float(abs(possibleMatchingChar.intBoundingRectArea - possibleChar.intBoundingRectArea)) / float(possibleChar.intBoundingRectArea)
        change_in_width = float(abs(possibleMatchingChar.intBoundingRectWidth - possibleChar.intBoundingRectWidth)) / float(possibleChar.intBoundingRectWidth)
        change_in_height = float(abs(possibleMatchingChar.intBoundingRectHeight - possibleChar.intBoundingRectHeight)) / float(possibleChar.intBoundingRectHeight)

        if (distance_between_chars < (possibleChar.fltDiagonalSize * MAX_DIAG_SIZE_MULTIPLE_AWAY) and
            angle_between_chars < MAX_ANGLE_BETWEEN_CHARS and
            change_in_area < MAX_CHANGE_IN_AREA and
            change_in_width < MAX_CHANGE_IN_WIDTH and
            change_in_height < MAX_CHANGE_IN_HEIGHT):

            listOfMatchingChars.append(possibleMatchingChar)        

    return listOfMatchingChars                 

def distanceBetweenChars(firstChar, secondChar):
    X = abs(firstChar.intCenterX - secondChar.intCenterX)
    Y = abs(firstChar.intCenterY - secondChar.intCenterY)

    return math.sqrt((X ** 2) + (Y ** 2))


def angleBetweenChars(firstChar, secondChar):
    adjacent = float(abs(firstChar.intCenterX - secondChar.intCenterX))
    opposite = float(abs(firstChar.intCenterY - secondChar.intCenterY))

    if adjacent != 0.0:                           
        angle_radian = math.atan(opposite / adjacent)      
    else:
        angle_radian = 1.5708                          

    angle_degree = angle_radian * (180.0 / math.pi)       

    return angle_degree

def remove_innerOverlapping_chars(listOfMatchingChars):
    listOfMatchingCharsWithInnerCharRemoved = list(listOfMatchingChars)                

    for currentChar in listOfMatchingChars:
        for otherChar in listOfMatchingChars:
            if currentChar != otherChar:        
                if distanceBetweenChars(currentChar, otherChar) < (currentChar.fltDiagonalSize * MIN_DIAG_SIZE_MULTIPLE_AWAY):
                    if currentChar.intBoundingRectArea < otherChar.intBoundingRectArea:         
                        if currentChar in listOfMatchingCharsWithInnerCharRemoved:              
                            listOfMatchingCharsWithInnerCharRemoved.remove(currentChar)         
                    else:                                                                     
                        if otherChar in listOfMatchingCharsWithInnerCharRemoved:                
                            listOfMatchingCharsWithInnerCharRemoved.remove(otherChar)           

    return listOfMatchingCharsWithInnerCharRemoved


def recognizeCharsInPlate(threshold_image, listOfMatchingChars):
    strChars = ""
    height, width = threshold_image.shape
    threshold_image_Color = np.zeros((height, width, 3), np.uint8)

    listOfMatchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)

    cv2.cvtColor(threshold_image, cv2.COLOR_GRAY2BGR, threshold_image_Color)                     

    for currentChar in listOfMatchingChars:                                         
        pt1 = (currentChar.intBoundingRectX, currentChar.intBoundingRectY)
        pt2 = ((currentChar.intBoundingRectX + currentChar.intBoundingRectWidth), (currentChar.intBoundingRectY + currentChar.intBoundingRectHeight))
        cv2.rectangle(threshold_image_Color, pt1, pt2, Main.SCALAR_GREEN, 2)           

        cropped_char = threshold_image[currentChar.intBoundingRectY : currentChar.intBoundingRectY + currentChar.intBoundingRectHeight,
                           currentChar.intBoundingRectX : currentChar.intBoundingRectX + currentChar.intBoundingRectWidth]
        resized_cropped_char = cv2.resize(cropped_char, (RESIZED_CHAR_IMAGE_WIDTH, RESIZED_CHAR_IMAGE_HEIGHT))           
        resized_cropped_char_1d = resized_cropped_char.reshape((1, RESIZED_CHAR_IMAGE_WIDTH * RESIZED_CHAR_IMAGE_HEIGHT))        
        resized_cropped_char_1d = np.float32(resized_cropped_char_1d)               
        retval, npaResults, neigh_resp, dists = kNearest.findNearest(resized_cropped_char_1d, k = 1)              
        strCurrentChar = str(chr(int(npaResults[0][0])))            
        strChars = strChars + strCurrentChar                        
    
    # cv2.imshow("threshold", threshold_image_Color)
    return strChars, threshold_image_Color