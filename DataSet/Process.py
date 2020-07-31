import sys;
import cv2;
import numpy as np;

RawImage = cv2.imread(sys.argv[1]);

# 1. Enhance contrast;
Alpha = 3.0;
Beta = -Alpha*np.mean(cv2.mean(RawImage)[0:3]);
Contrast = cv2.convertScaleAbs(RawImage, alpha = Alpha, beta = Beta);

# 2. Blur;
sigmaColor = [40, 200];
sigmaSpace = 10;
Blur1 = cv2.bilateralFilter(Contrast, d = 0, sigmaColor = sigmaColor[0], sigmaSpace = sigmaSpace, borderType = cv2.BORDER_WRAP);
Blur2 = cv2.bilateralFilter(Contrast, d = 0, sigmaColor = sigmaColor[1], sigmaSpace = sigmaSpace, borderType = cv2.BORDER_WRAP);

# 3. Canny;
Edges1 = cv2.Canny(Blur1, 100, 300);
Edges2 = cv2.Canny(Blur2, 80, 150);

# 4. Crop:
Margin = 5;
Edges1 = Edges1[Margin:-Margin, Margin:-Margin];
Edges2 = Edges2[Margin:-Margin, Margin:-Margin];

# 5. Dilatation:
KernelSize = 3;
Kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (KernelSize, KernelSize));
Dilation1 = cv2.dilate(Edges1, Kernel, iterations = 1);
Dilation2 = cv2.dilate(Edges2, Kernel, iterations = 1);

# 6. Hough;
Lines1 = cv2.HoughLinesP(Dilation1, 1, np.pi/180, threshold = 40, minLineLength = 60, maxLineGap = 5);
Lines2 = cv2.HoughLinesP(Dilation2, 1, np.pi/180, threshold = 40, minLineLength = 60, maxLineGap = 5);

if len(Lines1):
	for X in Lines1:
		cv2.line(RawImage, (X[0][0]+Margin, X[0][1]+Margin), (X[0][2]+Margin, X[0][3]+Margin), (255, 0, 255), 1);
		#print((X[0][0], X[0][1]), (X[0][2], X[0][3]));
		
if len(Lines2):
	for X in Lines2:
		cv2.line(RawImage, (X[0][0]+Margin, X[0][1]+Margin), (X[0][2]+Margin, X[0][3]+Margin), (0, 255, 0), 1);
		#print((X[0][0], X[0][1]), (X[0][2], X[0][3]));

# 7. Identification;
# 8. Modelling;

cv2.imshow("RawImage", RawImage);
cv2.imshow("Contrast", Contrast);
cv2.imshow("Blur1", Blur1);
cv2.imshow("Blur2", Blur2);
cv2.imshow("Dilation1", Dilation1);
cv2.imshow("Dilation2", Dilation2);
#cv2.imshow("Opening", Opening);
#cv2.imshow("Closing", Closing);

cv2.waitKey(0);
cv2.destroyAllWindows();
