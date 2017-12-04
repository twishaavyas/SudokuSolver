# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 15:34:57 2017

@author: Twisha
"""

import sys

sys.path.append('E:\python\Lib\site-packages')
import cv2
import numpy as np
from collections import defaultdict
import SudokuSolution
import pytesseract
import os
from PIL import Image


class Sudoku:
    @staticmethod
    def sudoku(image):
        # dynamic image
        image = cv2.imread(image)
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        detected_lines = Sudoku.preprocessImage(img)
        if detected_lines is not None and len(detected_lines) > 19:
            lines = detected_lines[0]
            cartesianLine = list()
            for lines in detected_lines:
                line = sorted(lines, key=lambda line: line[0])
                pos_hori = 0
                pos_vert = 0
                # Create a list to store new bundle of lines
                straightLines = []
                # Store intersection points
                for rho, theta in line:

                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    x1 = int(x0 + 1000 * (-b))
                    y1 = int(y0 + 1000 * (a))
                    x2 = int(x0 - 1000 * (-b))
                    y2 = int(y0 - 1000 * (a))

                    if (b > 0.5):
                        # Check the position
                        if (rho - pos_hori > 10):
                            # Update the position
                            pos_hori = rho
                            # Saving new line, 0 is horizontal line, 1 is vertical line
                            straightLines.append([rho, theta, 0])
                            cartesianLine.append((straightLines))
                            # cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
                    else:
                        if (rho - pos_vert > 10):
                            pos_vert = rho
                            straightLines.append([rho, theta, 1])
                            cartesianLine.append(straightLines)
                            # cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)

            IntersectionPoints = defaultdict(list)
            IntersectionList = list()
            for i in range(len(cartesianLine)):
                for j in range(len(cartesianLine)):
                    if (cartesianLine[j][0][2] == 1 and cartesianLine[i][0][2] == 0):
                        x1 = np.cos(cartesianLine[i][0][1])
                        y1 = np.sin(cartesianLine[i][0][1])
                        x2 = np.cos(cartesianLine[j][0][1])
                        y2 = np.sin(cartesianLine[j][0][1])
                        b1 = cartesianLine[i][0][0]
                        b2 = cartesianLine[j][0][0]
                        a = np.array([[x1, y1], [x2, y2]])
                        b = np.array([b1, b2])
                        x = np.linalg.solve(a, b)
                        x = (int(x[0]), int(x[1]))

                        if (len(IntersectionList) == 0):
                            IntersectionPoints[x[0]].append(x[1])
                            IntersectionList.append(x)
                            cv2.circle(image, tuple(x), 2, (255, 0, 0), 2)

                        elif (Sudoku.substantialDistance(x, IntersectionList)):
                            IntersectionPoints[x[0]].append(x[1])
                            IntersectionList.append(x)
                            cv2.circle(image, tuple(x), 2, (255, 0, 0), 12)

            IntersectionList = sorted(IntersectionList)
            # print len(IntersectionList)
            img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 101, 1)
            f = 0
            if True:
                for i in range(0, 9):
                    for j in range(0, 9):
                        y1q = int(IntersectionList[j + i * 10][1] + 5)
                        y2q = int(IntersectionList[j + i * 10 + 11][1] - 5)
                        x1q = int(IntersectionList[j + i * 10][0] + 5)
                        x2q = int(IntersectionList[j + i * 10 + 11][0] - 5)
                        cv2.rectangle(image, (x1q, y1q), (x2q, y2q), (255, 255, 0), 2)
                        f = f + 1
                        cv2.imwrite(str(f) + ".jpg", img[y1q: y2q, x1q: x2q])
                cv2.imwrite('houghlines3.jpg', image)
                return True
        return False

    @staticmethod
    def substantialDistance(x, points):
        flag = True
        for p in range(len(points)):
            if (Sudoku.dist(np.array(x), np.array(points[p])) < 20):
                flag = False
        return flag

    @staticmethod
    def dist(x, y):
        return np.sqrt(np.sum((x - y) ** 2))

    @staticmethod
    def getNumberArray():
        pytesseract.pytesseract.tesseract_cmd = 'E:\\python\\Tesseract-OCR\\tesseract.exe'
        tessdata_dir_config = '--tessdata-dir "E:\\python\\Lib\\site-packages\\pytesseract"'

        input = list()
        for x in range(81):
            filename = str(x + 1) + '.jpg'
            string = (pytesseract.image_to_string(Image.open(os.path.abspath(filename)), config='-psm 10'))
            if string == '':
                string = '0'
            input.append(string)

        sudoku = ''
        for i in range(0, 9):
            for j in range(0, 9):
                sudoku = sudoku + input[i + (9 * j)]
        # return sudoku


        w, h = 9, 9;
        sudokuMatrix = [[0 for x in range(w)] for y in range(h)]
        index = 0
        for i in range(0, 9):
            for j in range(0, 9):
                sudokuMatrix[i][j] = int(sudoku[index])
                index = index + 1
        return sudokuMatrix


    @staticmethod
    def solveSudoku(image):
        isSudokuProblem = Sudoku.sudoku(image)
        # print isSudokuProblem
        if (isSudokuProblem):
            grid = Sudoku.getNumberArray()
            # print grid
            if (True):
                # print 'in'
                SudokuSolution.solve(grid)
                print grid
            for file in os.listdir(os.path.dirname(os.path.realpath(__file__))):
                if file.endswith('.jpg'):
                    os.remove(file)

    @staticmethod
    def preprocessImage(img):
        median = np.median(img)
        sigma = 0
        min_threshold = max(0, (1.0 - sigma) * median)
        max_threshold = min(255, (1.0 + sigma) * median)
        edges = cv2.Canny(img, min_threshold, max_threshold, apertureSize=3)

        detected_lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        cv2.imwrite('houghlines6.jpg', edges)

        return detected_lines
