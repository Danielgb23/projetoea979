import sys;
import cv2;
import numpy as np;

#Adapted from https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv
def Contrast(Image, Brightness = 0.0, Contrast = 2.0):
	return cv2.addWeighted(Image, Contrast, Image, 0.0, 127*(1.0+Brightness-Contrast));

RawImage = cv2.imread(sys.argv[1]);

# 1. Enhance contrast;
Contrast = Contrast(RawImage, 0, 3);

# 2. Blur;
Blur = cv2.bilateralFilter(Contrast, 20, 100, 20);

# 3. Canny;
Edges = cv2.Canny(Blur, 100, 300);

# 4. Dilatation:
KernelSize = 2;
Kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (KernelSize, KernelSize));
Dilation = cv2.dilate(Edges, Kernel, iterations = 1);

Opening = cv2.morphologyEx(Dilation, cv2.MORPH_OPEN, Kernel);
Closing = cv2.morphologyEx(Opening, cv2.MORPH_CLOSE, Kernel);

# 5. Hough;
Lines = cv2.HoughLinesP(Opening, 1, np.pi/180, threshold = 80, minLineLength = 100, maxLineGap = 5);

for X in Lines:
	cv2.line(Blur, (X[0][0], X[0][1]), (X[0][2], X[0][3]), (255, 0, 255), 3);
	print((X[0][0], X[0][1]), (X[0][2], X[0][3]));

# 5. Identification;
# 6. Modelling;

cv2.imshow("RawImage", RawImage);
cv2.imshow("Contrast", Contrast);
cv2.imshow("Blur", Blur);
cv2.imshow("Edges", Edges);
cv2.imshow("Dilation", Dilation);
cv2.imshow("Opening", Opening);
cv2.imshow("Closing", Closing);

cv2.waitKey(0);
cv2.destroyAllWindows();
