import sys;
import os;
import numpy as NP;
from PIL import Image;
import matplotlib;
matplotlib.use("GTK3Agg");
import matplotlib.pyplot as PLT;
import json;

def PerspectiveCoefficients(A, B):
	matrix = [];
	for p1, p2 in zip(A, B):
		matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]]);
		matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]]);

	A = NP.matrix(matrix, dtype=NP.float)
	B = NP.array(B).reshape(8)

	res = NP.dot(NP.linalg.inv(A.T * A) * A.T, B)
	return NP.array(res).reshape(8)

def Correct(JSON):
	#Opens original image:
	I = Image.open(JSON["Image"]);

	Results = JSON["Results"];
	L0 = NP.array(Results["L0"]);
	R0 = NP.array(Results["R0"]);
	L1 = NP.array(Results["L1"]);
	R1 = NP.array(Results["R1"]);
	Runway = JSON["Runway"];
	Width = NP.array(Runway["Width"]);
	Length = NP.array(Runway["Length"]);

	C0 = (L0+R0)/2.0;
	C1 = (L1+R1)/2.0;
	C = (C0+C1)/2.0;
	D = C0-C1;
	Angle = NP.arctan2(D[0], D[1]);

	#Rotate image:
	I = I.rotate(NP.degrees(-Angle), Image.BICUBIC, False, (C[0], C[1]));

	#Rotate points:
	Cos, Sin = NP.cos(Angle), NP.sin(Angle);
	Rotation = NP.array(((Cos, -Sin), (Sin, Cos)));
	[L0, R0, L1, R1, C_] = NP.transpose(NP.matmul(Rotation, NP.c_[L0, R0, L1, R1, C]));

	#Correct center offset:
	D = C-C_;
	[L0, R0, L1, R1] = [L0, R0, L1, R1]+D;

	D = R0-L0;
	ShearFactor = D[1]/D[0];
	#Shear image:
	Shear = NP.eye(3);
	Shear[1][0] = ShearFactor;
	I = I.transform(I.size, Image.AFFINE, Shear.flatten()[:6], Image.BICUBIC);

	#Shear points:
	Shear = NP.eye(2);
	Shear[1][0] = -ShearFactor;
	[L0, R0, L1, R1] = NP.transpose(NP.matmul(Shear, NP.c_[L0, R0, L1, R1]));

	#Crop image:
	Y0 = (R0[1]+L0[1])/2.0;
	Y1 = (R1[1]+L1[1])/2.0;
	X0 = L0[0];
	X1 = X0+R0[0]-L0[0];
	I = I.crop((X0, Y1, X1, Y0));

	D = NP.array([X0, Y1]);
	[L0, R0, L1, R1] = [L0, R0, L1, R1]-D;

	#Perspective:
	W, H = I.size;
	T = PerspectiveCoefficients([(0, H), (W, H), (0, 0), (W, 0)], [L0, R0, L1, R1]);
	I = I.transform(I.size, Image.PERSPECTIVE, T.flatten()[:8], Image.BICUBIC);
	[L0, R0, L1, R1] = [(0, H), (W, H), (0, 0), (W, 0)];

	#Resize:
	AspectRatioFactor = 0.25;
	VScale = AspectRatioFactor*Length/Width;
	I = I.resize((I.size[0], int(VScale*I.size[1])), Image.ANTIALIAS)
	[L0, R0, L1, R1] = [(0, VScale*H), (W, VScale*H), (0, 0), (W, 0)];

	Figure = PLT.figure()
	F = Figure.add_subplot(1, 1, 1);
	F.imshow(I);

	P = NP.transpose(NP.vstack([L0, L1, R1, R0, L0]));

	F.plot(P[0], P[1]);

	PLT.show();
