
#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        Desktop button detection .py
#
# Purpose:     This module is use CV to detect the match area in the screen and 
#              move mouse to the position to click. 
# 
# Author:      Yuancheng Liu
#
# Version:     v_0.0.1
# Created:     2022/01/11
# Copyright:   Copyright (c) 2022 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import os 
import cv2
import pyscreenshot
from datetime import datetime
import mouse
import time

print("Current working directory is : %s" % os.getcwd())
dirpath = os.path.dirname(os.path.abspath(__file__))
print("Current source code location : %s" % dirpath)

DEF_DATA_DIR = 'data'
DEF_SS_NAME = 'screenshot.png' # default screenshot name 

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class screenPosClicker(object):
    def __init__(self) -> None:
        self.dataDir = os.path.join(dirpath, 'data')
        if not os.path.isdir(self.dataDir): os.mkdir(self.dataDir)
        self.clickTemplatePath = None 

    #-----------------------------------------------------------------------------
    def findTemplatePos(self, srcImgPath, templatePath, recordRst=False):
        """ Find the template image center position in the source image.

        Args:
            srcImgPath (str): source image path
            templatePath (str): template need to find image path.
            recordRst (bool, optional): flag to identify whether mark result on 
                source file. Defaults to False.
        Returns:
            (int, int): center position (x, y) to find the template image. if any 
                x or y < 0, it means the template image is not found in the source.
        """
        srcImg = cv2.imread(srcImgPath)
        srcGray = cv2.cvtColor(srcImg, cv2.COLOR_BGR2GRAY)

        tmpImg = cv2.imread(templatePath, 0)

        result = cv2.matchTemplate(srcGray, tmpImg, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        height, width = tmpImg.shape[:2]
        top_left = max_loc
        bottom_right = (top_left[0] + width, top_left[1] + height)
        pos_XY = (int((top_left[0]+bottom_right[0])/2),
                  int((top_left[1]+bottom_right[1])/2))
        # Draw detection result on the src image
        if recordRst:
            print("Draw detection result on the src image")
            cv2.rectangle(srcImg, top_left, bottom_right, (0, 0, 255), 3)
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 0.7
            org = (top_left[0], top_left[1]-10)
            rstImage = cv2.putText(srcImg, 'find match: at %s' % str(pos_XY), org, font,
                                fontScale, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imwrite(srcImgPath, rstImage)

        return pos_XY

    #-----------------------------------------------------------------------------
    def setClickTemplate(self, templatePath):
        if os.path.exists(templatePath):
            self.clickTemplatePath = templatePath
        else:
            print("Error, the click template image file is not exist")

    #-----------------------------------------------------------------------------
    def findAndClick(self, recordRst=False):
        """ Find the template image center position in the source image and click the position.
        """
        # screen short current desktop
        screenshot = pyscreenshot.grab()
        filename = 'screenshot_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.png' if recordRst else DEF_SS_NAME
        filePath = os.path.join(self.dataDir, filename)
        screenshot.save(filePath)
        if self.clickTemplatePath: 
            pos_XY = self.findTemplatePos(filePath, self.clickTemplatePath, recordRst=recordRst)
            if pos_XY[0] >=0 and pos_XY[1] >=0:
                print("Find matched click position: %s" % str(pos_XY))
                mouse.move(pos_XY[0], pos_XY[1])
                time.sleep(0.2)
                mouse.click()
            else:
                print("Warning: didn't find match click position")
        else:
            print("Warning: didn't set click template image")

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

def testCase(mode):
    templateFile = os.path.join(dirpath, 'template.png')
    clicker = screenPosClicker()
    clicker.setClickTemplate(templateFile)
    if mode == 0:
        print("Test case 0: test click without record detection result")
        clicker.findAndClick(recordRst=False)
    elif mode ==1:
        print("Test case 1: test click with record detection result in data folder.")
        clicker.findAndClick(recordRst=True)
    else:
        pass

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    mode = 1
    testCase(mode)

exit()

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
