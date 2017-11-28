# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 15:34:57 2017

@author: Twisha
"""



import cv2
import numpy as np
from collections import defaultdict
import project
import os
from io import BytesIO
from pdfdocument.document import PDFDocument

try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import os

class Sudoku:
    @staticmethod
    def sudoku():
        color_img = cv2.imread('question.png')
        img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
        imageCharacteristic = cv2.minMaxLoc(img)
        print imageCharacteristic[2]
        
        median = np.median(img)
        sigma = 0.33
        min_threshold = max(0, (1.0 - sigma) * median)
        max_threshold = min(255, (1.0 + sigma) * median)
        
        edges = cv2.Canny(img, min_threshold, max_threshold)
        
        #
        #print(edges)
        #
        ##plt.subplot(121),plt.imshow(img,cmap = 'gray')
        ##plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        #plt.subplot(122),plt.imshow(edges,cmap = 'gray')
        #plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
        
        #plt.show()
        #cv2.imshow("Original", img)
        #cv2.imshow("Edges", edges)
        #cv2.waitKeydet_lines = []
        detected_lines = cv2.HoughLines(edges, 1, np.pi/180, 300, 0, 0 );
        
        lines = detected_lines[0]
        cartesianLine = list()
        for lines in detected_lines: 
            line = sorted(lines, key=lambda line:line[0])
            pos_hori = 0
            pos_vert = 0
                # Create a list to store new bundle of lines
            straightLines = []
                # Store intersection points
            for rho,theta in line:

                 a = np.cos(theta)
                 b = np.sin(theta)
                 x0 = a*rho
                 y0 = b*rho
                 x1 = int(x0 + 1000*(-b))
                 y1 = int(y0 + 1000*(a))
                 x2 = int(x0 - 1000*(-b))
                 y2 = int(y0 - 1000*(a))
                 
                 if (b>0.5):
                  # Check the position
                  if(rho-pos_hori>10):
                   # Update the position
                   pos_hori=rho
                   # Saving new line, 0 is horizontal line, 1 is vertical line
                   straightLines.append([rho,theta, 0])
                   cartesianLine.append((straightLines))
        #           cv2.line(color_img,(x1,y1),(x2,y2),(0,255,0),2)
                 else:
                  if(rho-pos_vert>10):
                   pos_vert=rho
                   straightLines.append([rho,theta, 1])
                   cartesianLine.append(straightLines)
        #           cv2.line(color_img,(x1,y1),(x2,y2),(0,0,255),2)
                   
        IntersectionPoints = defaultdict(list)
        IntersectionList = list()
        for i in range(len(cartesianLine)):
            for j in range(len(cartesianLine)):
                if(cartesianLine[j][0][2] == 1 and cartesianLine[i][0][2] == 0):
                    x1 = np.cos(cartesianLine[i][0][1])
                    y1 = np.sin(cartesianLine[i][0][1])
                    x2 = np.cos(cartesianLine[j][0][1])
                    y2 = np.sin(cartesianLine[j][0][1])
                    b1 = cartesianLine[i][0][0]
                    b2 = cartesianLine[j][0][0]
                    a = np.array([[x1, y1], [x2, y2]])
                    b = np.array([b1, b2])
                    x = np.linalg.solve(a, b)
                    x = (int(x[0]) , int(x[1]))

                    if(len(IntersectionList) == 0):
                        IntersectionPoints[x[0]].append(x[1])
                        IntersectionList.append(x)
                        cv2.circle(color_img, tuple(x), 2,(255,0,0),2)
                    
                    elif(Sudoku.substantialDistance(x, IntersectionList)):
                         IntersectionPoints[x[0]].append(x[1])
                         IntersectionList.append(x)
                         cv2.circle(color_img, tuple(x), 2,(255,0,0),2)
        
        IntersectionList = sorted(IntersectionList)
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 101, 1)
        f = 0;
        for i in range(0,9):
            for j in range(0,9):
               y1q=int(IntersectionList[j+i*10][1]+5)
               y2q=int(IntersectionList[j+i*10+11][1]-5)
               x1q=int(IntersectionList[j+i*10][0]+5)
               x2q=int(IntersectionList[j+i*10+11][0]-5)
               cv2.rectangle(color_img, (x1q, y1q), (x2q, y2q), (0,255,0), 2)
               f = f + 1
               cv2.imwrite( str(f)+".jpg", img[y1q: y2q, x1q: x2q])
        #cv2.line(color_img,(x1,y1),(x2,y2),(0,255,0),2)
        #cv2.circle(color_img,(int(coList[0]), int(coList[1])), 63, (0,0,255), -1)
        
        cv2.imwrite('houghlines3.jpg',color_img)
        cv2.imwrite('houghlines4.jpg',img)
        
    @staticmethod    
    def substantialDistance(x, points):
#        print points
        flag = True
        for p in range(len(points)):
            if(Sudoku.dist(np.array(x), np.array(points[p])) < 40 ):
                flag = False
        return flag
     
    @staticmethod    
    def dist(x,y):   
        return np.sqrt(np.sum((x-y)**2))        
        
             
    @staticmethod

    def getNumberArray():
        pytesseract.pytesseract.tesseract_cmd = 'E:\\python\\Tesseract-OCR\\tesseract.exe'
        tessdata_dir_config = '--tessdata-dir "E:\\python\\python\\Lib\\site-packages\\pytesseract"'

        input = list()
        for x in range(81):
            filename = str(x+1) + '.jpg'
            string = (pytesseract.image_to_string(Image.open(os.path.abspath(filename)), config='-psm 10'))
            if string == '':
                string = '0'
            input.append(string)

        sudoku = ''
        for i in range(0,9):
            for j in range(0,9):
                sudoku = sudoku + input[i + (9*j)]
        return sudoku;


    @staticmethod
    def solveSudoku():
        Sudoku.sudoku()
        grid = Sudoku.getNumberArray()
        print grid
        project.display(project.solve(grid))
        print os.path.dirname(os.path.realpath(__file__))
        for file in os.listdir(os.path.dirname(os.path.realpath(__file__))) :
            if file.endswith('.jpg'):
                os.remove(file)



        #==============================================================================
    #          coefficients = np.polyfit([x1, x2], [y1, y2], 1)
    #          coList = coefficients.tolist()
    #          cartesianLine.append(coList)
    #          cv2.line(color_img,(x1,y1),(x2,y2),(0,255,0),2)
    #          cv2.circle(color_img,(int(coList[0]), int(coList[1])), 63, (0,0,255), -1)
    # #print(cartesianLine)
    # 
    # for i in range(len(cartesianLine)):
    #     for j in range(len(cartesianLine)):
    #         if i < j:
    #             x1 = cartesianLine[i][0]
    #             y1 = -1
    #             x2 = cartesianLine[j+i][0]
    #             y2 = -1
    #             b1 = cartesianLine[i][1] * -1
    #             b2 = cartesianLine[j+i][1] * -1
    #             a = np.array([[x1,y1], [x2, y2]])
    #             b = np.array([b1,b2])
    #             print(a, b)
    #             x = np.linalg.solve(a, b)
    # #        print(x)
    #         
    #         
    # cv2.imwrite('houghlines3.jpg',color_img)
    #==============================================================================
Sudoku.solveSudoku()

