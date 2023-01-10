import cv2
import numpy as np

image= cv2.imread('1_1.png')
cv2.imshow('Rainforest', image)
cv2.waitKey(0)
gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

template= cv2.imread('3_1.png',0)


result= cv2.matchTemplate(gray, template, cv2.TM_CCOEFF)

min_val, max_val, min_loc, max_loc= cv2.minMaxLoc(result)

height, width= template.shape[:2]

top_left= max_loc
bottom_right= (top_left[0] + width, top_left[1] + height)

cv2.rectangle(image, top_left, bottom_right, (0,0,255),5)

cv2.imshow('Rainforest', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
