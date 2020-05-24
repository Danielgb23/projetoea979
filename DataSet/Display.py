import sys;
import os;
import numpy as NP;
from PIL import Image;
import matplotlib;
matplotlib.use("GTK3Agg");
import matplotlib.pyplot as PLT;
import json;

In = sys.argv[1];
InTxt = os.path.splitext(In)[0]+".txt";
I = Image.open(In);

Figure = PLT.figure()
F = Figure.add_subplot(1, 1, 1);
F.imshow(I);

File = open(InTxt, "r");
Data = json.loads(File.read());

Runway = Data["Runway"];
L0 = Runway["L0"];
R0 = Runway["R0"];
L1 = Runway["L1"];
R1 = Runway["R1"];

P = NP.transpose(NP.vstack([L0, L1, R1, R0, L0]));

F.plot(P[0], P[1]);

PLT.show();

File.close();
