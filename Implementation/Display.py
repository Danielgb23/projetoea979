import sys;
import os;
import numpy as NP;
from PIL import Image;
import matplotlib;
matplotlib.use("GTK3Agg");
import matplotlib.pyplot as PLT;
import json;

def Display(JSON):
	Figure = PLT.figure()
	F = Figure.add_subplot(1, 1, 1);
	F.imshow(Image.open(JSON["Image"]));

	Runway = JSON["Runway"];
	L0 = Runway["L0"];
	R0 = Runway["R0"];
	L1 = Runway["L1"];
	R1 = Runway["R1"];

	P = NP.transpose(NP.vstack([L0, L1, R1, R0, L0]));

	#Plot expected:
	F.plot(P[0], P[1]);

	Results = JSON["Results"];
	L0 = Results["L0"];
	R0 = Results["R0"];
	L1 = Results["L1"];
	R1 = Results["R1"];

	P = NP.transpose(NP.vstack([L0, L1, R1, R0, L0]));

	#Plot obtained:
	F.plot(P[0], P[1]);

	PLT.show();
