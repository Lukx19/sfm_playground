import cv2

import sys; sys.stdout.flush()

img = cv2.imread('2.png',1)
cv2.imshow('img',img)
i = 0
while i < 2:
    cv2.waitKey(0)
    print(i)
    i=i+1

