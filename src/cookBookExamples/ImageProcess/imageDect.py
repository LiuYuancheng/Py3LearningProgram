
#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        Desktop button detection .py
#
# Purpose:     This module is used to detect the button/switch base the windows desktop
# 
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2022/01/11
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import cv2
import numpy as np



def findTemplate(source, template):
    srcImg= cv2.imread(source)
    srcGray= cv2.cvtColor(srcImg, cv2.COLOR_BGR2GRAY)
    tmpImg= cv2.imread(template,0)
    result= cv2.matchTemplate(srcGray, tmpImg, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc= cv2.minMaxLoc(result)
    height, width= template.shape[:2]
    top_left= max_loc
    bottom_right= (top_left[0] + width, top_left[1] + height)
    pos_XY = (int((top_left[0]+bottom_right[0])/2), int((top_left[1]+bottom_right[1])/2))
    return pos_XY


image= cv2.imread('3_1.png')
cv2.imshow('sreen short', image)
cv2.waitKey(0)
gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

template= cv2.imread('3_2.png',0)


result= cv2.matchTemplate(gray, template, cv2.TM_CCOEFF)

min_val, max_val, min_loc, max_loc= cv2.minMaxLoc(result)

height, width= template.shape[:2]

top_left= max_loc
bottom_right= (top_left[0] + width, top_left[1] + height)

cv2.rectangle(image, top_left, bottom_right, (0,0,255),3)
font = cv2.FONT_HERSHEY_SIMPLEX
  
# org
org = (top_left[0], top_left[1]-10)
  
# fontScale
fontScale = 0.7

pos_XY = (int((top_left[0]+bottom_right[0])/2), int((top_left[1]+bottom_right[1])/2))

image = cv2.putText(image, 'find match: at %s' %str(pos_XY), org, font, 
                   fontScale, (0,0,255), 1, cv2.LINE_AA)

cv2.imshow('find match', image)
cv2.waitKey(0)
cv2.destroyAllWindows()