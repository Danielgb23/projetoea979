import sys;
import cv2;
import numpy as np;
import operator;
import copy;

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

# 6. Hough 1;
Lines1 = cv2.HoughLinesP(Dilation1, 1, np.pi/180, threshold = 40, minLineLength = 60, maxLineGap = 5);
Lines2 = cv2.HoughLinesP(Dilation2, 1, np.pi/180, threshold = 40, minLineLength = 60, maxLineGap = 5);

# 7. Merge and filter lines;
MinAngle = 30*np.pi/180;
Lines = list();
for X in Lines1:
	Delta = np.asarray([X[0][0], X[0][1]])-np.asarray([X[0][2], X[0][3]]);
	Angle = np.arctan(Delta[1]/Delta[0]);
	if (np.abs(Angle) > MinAngle):
		Lines.append(X[0]);
		
for X in Lines2:
	Delta = np.asarray([X[0][0], X[0][1]])-np.asarray([X[0][2], X[0][3]]);
	Angle = np.arctan(Delta[1]/Delta[0]);
	if (np.abs(Angle) > MinAngle):
		Lines.append(X[0]);

# 8. Line processing:
Edges = np.zeros(Edges1.shape, np.uint8);
LineWidth = 4;
for L in Lines:
	cv2.line(RawImage, (L[0]+Margin, L[1]+Margin), (L[2]+Margin, L[3]+Margin), (0, 255, 0), 1);
	cv2.line(Edges, (L[0]+Margin, L[1]+Margin), (L[2]+Margin, L[3]+Margin), (255, 255, 255), LineWidth);
	cv2.circle(RawImage, (L[0]+Margin, L[1]+Margin), 2, (255, 0, 0), -1);
	cv2.circle(RawImage, (L[2]+Margin, L[3]+Margin), 2, (255, 0, 0), -1);

# 9. Hough 2:
Lines = cv2.HoughLinesP(Edges, 1, np.pi/180, threshold = 20, minLineLength = 40, maxLineGap = 8);
DrawnEdges = cv2.cvtColor(Edges, cv2.COLOR_GRAY2RGB);
for X in Lines:
	cv2.line(DrawnEdges, (X[0][0]+Margin, X[0][1]+Margin), (X[0][2]+Margin, X[0][3]+Margin), (0, 0, 255), 1);

# 10. Modelling:
Max = 0;
BestI = 0;
BestJ = 0;
LineWeight = 8;
for I, X in enumerate(Lines):
	for J, Y in enumerate(Lines):
		print(I, len(Lines));
		TmpEdges = copy.copy(Edges);
		cv2.line(TmpEdges, (X[0][0]+Margin, X[0][1]+Margin), (X[0][2]+Margin, X[0][3]+Margin), (0, 0, 0), LineWeight);
		cv2.line(TmpEdges, (Y[0][0]+Margin, Y[0][1]+Margin), (Y[0][2]+Margin, Y[0][3]+Margin), (0, 0, 0), LineWeight);
		Count = np.count_nonzero(TmpEdges == 0);
		if (Count > Max):
			Max = Count;
			BestI = I;
			BestJ = J;

X = Lines[BestI][0];
Y = Lines[BestJ][0];

cv2.line(DrawnEdges, (X[0]+Margin, X[1]+Margin), (X[2]+Margin, X[3]+Margin), (255, 0, 255), 5);
cv2.line(DrawnEdges, (Y[0]+Margin, Y[1]+Margin), (Y[2]+Margin, Y[3]+Margin), (255, 0, 255), 5);
cv2.circle(RawImage, (X[0]+Margin, X[1]+Margin), 5, (0, 255, 255), -1);
cv2.circle(RawImage, (X[2]+Margin, X[3]+Margin), 5, (0, 255, 255), -1);
cv2.circle(RawImage, (Y[0]+Margin, Y[1]+Margin), 5, (0, 255, 255), -1);
cv2.circle(RawImage, (Y[2]+Margin, Y[3]+Margin), 5, (0, 255, 255), -1);

cv2.imshow("RawImage", RawImage);
cv2.imshow("Contrast", Contrast);
cv2.imshow("Blur1", Blur1);
cv2.imshow("Blur2", Blur2);
cv2.imshow("Edges1", Edges1);
cv2.imshow("Edges2", Edges2);
cv2.imshow("DrawnEdges", DrawnEdges);

cv2.waitKey(0);
cv2.destroyAllWindows();
