import sys;
import os;
import numpy as NP;
from PIL import Image;
import matplotlib;
matplotlib.use("GTK3Agg");
import matplotlib.pyplot as PLT;
import json;

"""
def GetCoordinates(I):
	Figure = PLT.figure()
	F = Figure.add_subplot(1, 1, 1);
	F.imshow(I);

	Coordinates = [];

	def Click(Event):
		if (Event.button == matplotlib.backend_bases.MouseButton.RIGHT):
			Coordinates.append((Event.xdata, Event.ydata));

			if (len(Coordinates) == 4):
				Figure.canvas.mpl_disconnect(CID);
				PLT.close(Figure);
		return;

	CID = Figure.canvas.mpl_connect("button_press_event", Click);
	PLT.show();
	return NP.round(Coordinates).astype(int);

def ReportData(Out, Header, Coordinates, Airport):
	F = open(Out, "w");
	F.write("{\n");
	
	if (Header != None):
		F.write("\t\"Aircraft\":\n");
		F.write("\t{\n");
		F.write("\t\t\"Lat\": \"" + Header[0] + "\",\n");
		F.write("\t\t\"Lon\": \"" + Header[1] + "\",\n");
		F.write("\t\t\"Alt\": " + Header[2] + ",\n");
		F.write("\t\t\"Mag\": " + Header[3] + "\n");
		F.write("\t},\n");	

	F.write("\t\"Runway\":\n");
	F.write("\t{\n");
	F.write("\t\t\"L0\": [" + str(Coordinates[0][0]) + ", " + str(Coordinates[0][1]) + "],\n");
	F.write("\t\t\"R0\": [" + str(Coordinates[1][0]) + ", " + str(Coordinates[1][1]) + "],\n");
	F.write("\t\t\"L1\": [" + str(Coordinates[2][0]) + ", " + str(Coordinates[2][1]) + "],\n");
	F.write("\t\t\"R1\": [" + str(Coordinates[3][0]) + ", " + str(Coordinates[3][1]) + "],\n");
	F.write("\t\t\"Lat\": \"" + Airport[0] + "\",\n");
	F.write("\t\t\"Lon\": \"" + Airport[1] + "\",\n");
	F.write("\t\t\"Alt\": " + Airport[2] + ",\n");
	F.write("\t\t\"Mag\": " + Airport[3] + ",\n");
	F.write("\t\t\"Length\": " + Airport[4] + ",\n");
	F.write("\t\t\"Width\": " + Airport[5] + ",\n");
	F.write("\t\t\"Name\": \"" + Airport[6] + "\",\n");
	F.write("\t}\n");
	
	F.write("}\n");
	F.close();
"""
In = sys.argv[1];
InTxt = os.path.splitext(In)[0]+".txt";
I = Image.open(In);

File = open(InTxt, "r");
S = File.read();
print(S);
Data = json.loads(S);
File.close();
print(Data);
