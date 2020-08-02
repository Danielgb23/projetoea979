import sys;
import cv2;
import numpy as np;
import operator;
import copy;

def Cart2Pol(P):
	Rho = np.sqrt(P[0]**2 + P[1]**2);
	Phi = np.arctan2(P[1], P[0]);
	return ([Rho, Phi]);

def Pol2Cart(P):
	return([P[0] * np.cos(P[1]), P[0] * np.sin(P[1])]);

def IdentifyRunway(JSON, ExportPath):
	RawImage = cv2.imread(JSON["Image"]);
	Result = copy.copy(RawImage);

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
		cv2.line(Result, (L[0]+Margin, L[1]+Margin), (L[2]+Margin, L[3]+Margin), (0, 255, 0), 1);
		cv2.line(Edges, (L[0]+Margin, L[1]+Margin), (L[2]+Margin, L[3]+Margin), (255, 255, 255), LineWidth);
		cv2.circle(Result, (L[0]+Margin, L[1]+Margin), 2, (255, 0, 0), -1);
		cv2.circle(Result, (L[2]+Margin, L[3]+Margin), 2, (255, 0, 0), -1);

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
			print(I, len(Lines), end = '\r');
			TmpEdges = copy.copy(Edges);
			cv2.line(TmpEdges, (X[0][0]+Margin, X[0][1]+Margin), (X[0][2]+Margin, X[0][3]+Margin), (0, 0, 0), LineWeight);
			cv2.line(TmpEdges, (Y[0][0]+Margin, Y[0][1]+Margin), (Y[0][2]+Margin, Y[0][3]+Margin), (0, 0, 0), LineWeight);
			Count = np.count_nonzero(TmpEdges == 0);
			if (Count > Max):
				Max = Count;
				BestI = I;
				BestJ = J;
	print("");

	X = Lines[BestI][0];
	Y = Lines[BestJ][0];
	
	#Cartesian coordinates:
	A = (X[0]+Margin, X[1]+Margin);
	B = (X[2]+Margin, X[3]+Margin);
	C = (Y[0]+Margin, Y[1]+Margin);
	D = (Y[2]+Margin, Y[3]+Margin);

	#Draw results:
	cv2.line(DrawnEdges, A, B, (255, 0, 255), 5);
	cv2.line(DrawnEdges, C, D, (255, 0, 255), 5);
	cv2.circle(Result, A, 5, (0, 255, 255), -1);
	cv2.circle(Result, B, 5, (0, 255, 255), -1);
	cv2.circle(Result, C, 5, (0, 255, 255), -1);
	cv2.circle(Result, D, 5, (0, 255, 255), -1);

	A = np.asarray(A);
	B = np.asarray(B);
	C = np.asarray(C);
	D = np.asarray(D);
	Center = (A+B+C+D)/4;

	#Sort vertex:
	Vertex = list();
	Vertex.append(Cart2Pol(A-Center));
	Vertex.append(Cart2Pol(B-Center));
	Vertex.append(Cart2Pol(C-Center));
	Vertex.append(Cart2Pol(D-Center));
	Vertex.sort(key = lambda X: X[1]);
	
	#Add results to JSON:
	JSON["Results"] = dict();
	JSON["Results"]["L0"] = (Pol2Cart(Vertex[3])+Center).tolist();
	JSON["Results"]["R0"] = (Pol2Cart(Vertex[2])+Center).tolist();
	JSON["Results"]["L1"] = (Pol2Cart(Vertex[0])+Center).tolist();
	JSON["Results"]["R1"] = (Pol2Cart(Vertex[1])+Center).tolist();
	
	#Show results:
	cv2.imshow("RawImage", RawImage);
	cv2.imshow("Contrast", Contrast);
	cv2.imshow("Blur1", Blur1);
	cv2.imshow("Blur2", Blur2);
	cv2.imshow("Edges1", Edges1);
	cv2.imshow("Edges2", Edges2);
	cv2.imshow("Drawn Edges", DrawnEdges);
	cv2.imshow("Result", Result);
	
	#Export images:
	if (ExportPath is not None):
		cv2.imwrite(ExportPath+"/01 Image.jpg", RawImage);
		cv2.imwrite(ExportPath+"/02 Contrast.jpg", Contrast);
		cv2.imwrite(ExportPath+"/03 Blur1.jpg", Blur1);
		cv2.imwrite(ExportPath+"/04 Blur2.jpg", Blur2);
		cv2.imwrite(ExportPath+"/05 Edges1.jpg", Edges1);
		cv2.imwrite(ExportPath+"/06 Edges2.jpg", Edges2);
		cv2.imwrite(ExportPath+"/07 DrawnEdges.jpg", DrawnEdges);
		cv2.imwrite(ExportPath+"/08 Result.jpg", Result);

	cv2.waitKey(0);
	cv2.destroyAllWindows();

	return JSON;
