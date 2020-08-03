import sys;
import cv2;
import numpy as np;


RawImage = cv2.imread(sys.argv[1]);
cv2.imshow("RawImage", RawImage);


cv2.waitKey(0);
cv2.destroyAllWindows();