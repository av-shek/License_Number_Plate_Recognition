from PIL import Image
import cv2
import csv
import numpy as np
import os
from xml.dom import minidom
import xml.etree.ElementTree as ET
import DetectChars
import DetectPlates
import PossiblePlate
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtGui import QPixmap

# python -m PyQt5.uic.pyuic -x project.ui -o project.py

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, read_image, img, thresh, chars):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1621, 861)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(60, 650, 1491, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 115, 471, 41))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.pixmap = QPixmap(read_image)
        self.label_2.setPixmap(self.pixmap)
        self.label_2.setGeometry(QtCore.QRect(60, 150, 981, 471))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1080, 121, 301, 41))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.pixmap = QPixmap(img)
        self.label_4.setPixmap(self.pixmap)
        self.label_4.setGeometry(QtCore.QRect(1080, 160, 461, 111))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(1080, 480, 221, 41))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(1080, 520, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setText(chars)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(610, 70, 361, 31))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(480, 0, 621, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_8.setTextFormat(QtCore.Qt.AutoText)
        self.label_8.setScaledContents(False)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(690, 40, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(60, 630, 141, 31))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(60, 660, 181, 31))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(1330, 660, 231, 31))
        self.label_12.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_12.setTextFormat(QtCore.Qt.PlainText)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(1450, 630, 111, 31))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(1300, 690, 261, 31))
        self.label_14.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_14.setTextFormat(QtCore.Qt.PlainText)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(1360, 720, 201, 31))
        self.label_15.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_15.setTextFormat(QtCore.Qt.PlainText)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(1230, 750, 331, 31))
        self.label_16.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_16.setTextFormat(QtCore.Qt.PlainText)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(1300, 780, 261, 31))
        self.label_17.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_17.setTextFormat(QtCore.Qt.PlainText)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(1080, 290, 261, 41))
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.pixmap = QPixmap(thresh)
        self.label_19.setPixmap(self.pixmap)
        self.label_19.setGeometry(QtCore.QRect(1080, 340, 510, 111))
        self.label_19.setObjectName("label_19")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1621, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GUI for License Number Plate Recognition"))
        self.label.setText(_translate("MainWindow", "Original Image with Detected License Number Plate"))
        # self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "Cropped Image of Detected Plate"))
        # self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.label_5.setText(_translate("MainWindow", "License Number in Text"))
        # self.label_6.setText(_translate("MainWindow", "TextLabel"))
        self.label_7.setText(_translate("MainWindow", "LICENSE NUMBER PLATE RECOGNITION"))
        self.label_8.setText(_translate("MainWindow", "INDIAN INSTITUTE OF INFORMATION TECHNOLOGY, "))
        self.label_9.setText(_translate("MainWindow", "ALLAHABAD, INDIA"))
        self.label_10.setText(_translate("MainWindow", "Supervised by-"))
        self.label_11.setText(_translate("MainWindow", "Prof. Ranjana Vyas"))
        self.label_12.setText(_translate("MainWindow", "Aman Joshi (IIT2018042)"))
        self.label_13.setText(_translate("MainWindow", "Project by-"))
        self.label_14.setText(_translate("MainWindow", "Anish Gir Gusai (IIT2018044)"))
        self.label_15.setText(_translate("MainWindow", "Avishek  (IIT2018051)"))
        self.label_16.setText(_translate("MainWindow", "Nagendra Singh Tomar (IIT2018057)"))
        self.label_17.setText(_translate("MainWindow", "Laxman Goliya  (IIT2018066)"))
        self.label_18.setText(_translate("MainWindow", "Segmentaion of Characters"))
        # self.label_19.setText(_translate("MainWindow", "TextLabel"))

SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

def main():
    
    success = DetectChars.KNN_data_loading_and_training()
    if success == False:
        return
    # for files in os.walk("Final_detected_plateImages"):
    #     print(files)
    images = []
    # for filename in os.listdir("Final_detected_plateImages"):
    #     img = filename
    #     images.append(img)
    # for filename in os.listdir("Testing_Dataset"):
    #     img = "Testing_Dataset/" + filename
    #     images.append(img)
    for filename in os.listdir("Training_Dataset/images"):
        img = "Training_Dataset/images/" + filename
        images.append(img)
    # for img in images:
        # tree = ET.parse(img)
        # root = tree.getroot()
        # filename = root.find('./filename').text
        # height = root.find('./size/height').text
        # width = root.find('./size/width').text
        # print('filename =', filename
        # print('height = ', height)
        # print('width = ', width)
    count1 = 0
    count2 = 0
    for img in images:
        # read_image = "Testing_Dataset/52.jpeg"
        input_image  = cv2.imread(img)               

        if input_image is None:                            
            print("\nImage not found!! \n")  
            return

        Detected_Plates = DetectPlates.detectPlatesInScene(input_image)           
        Detected_Plates = DetectChars.detectCharsInPlates(Detected_Plates)        

        # cv2.imshow("input_image", input_image)
        
        if len(Detected_Plates) == 0:                        
            print("\nLicense Plate Detection Failed!!\n") 
            row = [img]
            with open('data1.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(row)
            count1 = count1 + 1
        else:     
            count2 = count2 + 1                                                 
            Detected_Plates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)
            Final_detected_plate = Detected_Plates[0]

            # cv2.imshow("cropped_plate", Final_detected_plate.imgPlate)
            Cropped_plate = "Outputs/CroppedPlates/"+Final_detected_plate.strChars+".png"
            # cv2.imwrite(Cropped_plate, Final_detected_plate.imgPlate)
            thresh = "Outputs/ThresholdPlates/"+Final_detected_plate.strChars+".png"
            # cv2.imwrite(thresh, Final_detected_plate.imgThresh)
            # cv2.imshow("threshold_image", Final_detected_plate.imgThresh)

            if len(Final_detected_plate.strChars) == 0:                     
                print("\nCharacter Recognition Failed!!\n\n")  
                # return                                          

            Boundary_Around_Detected_Plate(input_image, Final_detected_plate)

            print("\nLicense plate number from image = " + Final_detected_plate.strChars + "\n")  
            Recognized_Chars_on_input_image(input_image, Final_detected_plate)
            
            detect = "Outputs/DetectedPlates/"+ Final_detected_plate.strChars +".png"
            # cv2.imwrite(detect, input_image)

            row = [img]
            with open('data2.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(row)
            # height, width, channel = input_image.shape
            # row = [read_image, height, width, Final_detected_plate.strChars]
            # with open('Outputs/data.csv', 'a') as f:
            #     writer = csv.writer(f)
            #     writer.writerow(row)
            
            # app = QtWidgets.QApplication(sys.argv)
            # MainWindow = QtWidgets.QMainWindow()
            # object_env = Ui_MainWindow()
            # object_env.setupUi(MainWindow, detect, Cropped_plate, thresh, Final_detected_plate.strChars)
            # MainWindow.show()
            # sys.exit(app.exec_())

    print("License Number Plate Detection Successful: " + str(count2))
    print("License Number Plate Detection Failed: " + str(count1))
    result = (count2/(count1+count2))*100
    print("Accuracy for License Number Plate Detection: " + str(result) + "%.")
    return

def Boundary_Around_Detected_Plate(input_image, Final_detected_plate):

    boundary_coordinates = cv2.boxPoints(Final_detected_plate.rrLocationOfPlateInScene)

    cv2.line(input_image, tuple(boundary_coordinates[0]), tuple(boundary_coordinates[1]), SCALAR_RED, 2)         
    cv2.line(input_image, tuple(boundary_coordinates[1]), tuple(boundary_coordinates[2]), SCALAR_RED, 2)
    cv2.line(input_image, tuple(boundary_coordinates[2]), tuple(boundary_coordinates[3]), SCALAR_RED, 2)
    cv2.line(input_image, tuple(boundary_coordinates[3]), tuple(boundary_coordinates[0]), SCALAR_RED, 2)

def Recognized_Chars_on_input_image(input_image, Final_detected_plate):
    Center_X = 0                             
    Center_Y = 0
    BottomLeft_X = 0                          
    BottomLeft_Y = 0

    input_image_Height, input_image_Width, input_image_Channels = input_image.shape
    plate_Height, plate_Width, plate_Channels = Final_detected_plate.imgPlate.shape

    Font_face = cv2.FONT_HERSHEY_SIMPLEX                      
    Font_scale = float(plate_Height) / 30.0                    
    Font_thickness = int(round(Font_scale * 1.5))           

    textSize, baseline = cv2.getTextSize(Final_detected_plate.strChars, Font_face, Font_scale, Font_thickness)        

    ( (Plate_Center_X, Plate_Center_Y), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg ) = Final_detected_plate.rrLocationOfPlateInScene

    Plate_Center_X = int(Plate_Center_X)         
    Plate_Center_Y = int(Plate_Center_Y)
    Center_X = int(Plate_Center_X)        

    if Plate_Center_Y < (input_image_Height * 0.75):                                                  
        Center_Y = int(round(Plate_Center_Y)) + int(round(plate_Height * 1.6)) 
    else:                                                                                      
        Center_Y = int(round(Plate_Center_Y)) - int(round(plate_Height * 1.6)) 
    
    textSizeWidth, textSizeHeight = textSize   
    BottomLeft_X = int(Center_X - (textSizeWidth / 2))           
    BottomLeft_Y = int(Center_Y + (textSizeHeight / 2))          

    cv2.putText(input_image, Final_detected_plate.strChars, (BottomLeft_X, BottomLeft_Y), Font_face, Font_scale, SCALAR_YELLOW, Font_thickness)

if __name__ == "__main__":
    main()