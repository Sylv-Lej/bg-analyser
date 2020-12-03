#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 17:37:42 2020

@author: slejamble
"""

import numpy as np
import cv2 as cv2
import imutils
import matplotlib.pyplot as plt

# whiteLower = (0,0,0) 
# whiteUpper = (191, 160, 150)


# font = cv2.FONT_HERSHEY_SIMPLEX
# topLeftCornerOfText = (10,30)
# fontScale = 0.2
# fontColor = (0,0,0)
# lineType = 2


frame = cv2.imread("../data/test/dice_crop.png")
# print(frame.shape)
left_dice = frame[:, 0:int(frame.shape[1]/2)]
right_dice = frame[:, int(frame.shape[1]/2):frame.shape[1]]


# cv2.imshow("left_dice", left_dice)
# key = cv2.waitKey(0)

# cv2.imshow("right_dice", right_dice)
# key = cv2.waitKey(0)

def get_dice_value(frame):
    frame = imutils.resize(frame, width=frame.shape[0]*2)
    blurred = cv2.GaussianBlur(frame, (3, 3), 0)
    # hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    ret, thresholded_img = cv2.threshold(blurred,127,255,cv2.THRESH_BINARY)


    thresholded_img = thresholded_img[:,:,2:]
    detected_circles = cv2.HoughCircles(thresholded_img, cv2.HOUGH_GRADIENT, 1, 20, param1=30, param2=15, minRadius=1, maxRadius=30)
    # for debug
    # if detected_circles is not None: 

    #     # Convert the circle parameters a, b and r to integers. 
    #     detected_circles = np.uint16(np.around(detected_circles)) 
    #     for pt in detected_circles[0, :]: 
    #         a, b, r = pt[0], pt[1], pt[2]
    #         cv2.circle(frame, (a, b), r, (0, 255, 0), 1)
    plt.imshow(thresholded_img)
    plt.show()
    return len(detected_circles[0])

left_dice_value = get_dice_value(left_dice)
print(left_dice_value)

right_dice_value = get_dice_value(right_dice)
print(right_dice_value)

#cv2.imshow("Preview", mask)
#key = cv2.waitKey(0)


# full_img = cv2.imread("../data/test/beginning.png")
# x = full_img.shape[0]
# y = full_img.shape[1]
# print(x)
# print(y)

# sub_dicde_img = full_img[int(y/3):int(y/3)+ 100, int(x*4/5):int(x*4/5) + 230]

# plt.imshow(sub_dicde_img)
# plt.show()