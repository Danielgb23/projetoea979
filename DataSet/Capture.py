import sys;
import os;
import numpy as NP;
from PIL import Image;
import matplotlib;
matplotlib.use("GTK3Agg");
import matplotlib.pyplot as PLT;
import pytesseract;

def ReadHeader(I):
	Header = NP.array(I.crop((0, 24, 730, 41)));
	Header[:, :, 0][Header[:, :, 0] < 230] = 0;
	Header[:, :, 1] *= 0;
	Header[:, :, 2] *= 0;
	
	HeaderText = pytesseract.image_to_string(Image.fromarray(Header)).split();

	Lat = HeaderText[1] + " " + HeaderText[2].split("\"")[0]+"'";
	Lon = HeaderText[4] + " " + HeaderText[5].split("\"")[0]+"'";
	Alt = HeaderText[7];
	Mag = HeaderText[10][3:];
	
	return [Lat, Lon, Alt, Mag];

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

In = sys.argv[1];
Out = os.path.splitext(In)[0]+".txt";
I = Image.open(In);

AirportLOWI26 = ["N47° 15.70'", "E11° 21.42'", "1894", "259", "2000", "45", "LOWI 26"];
AirportLOWI08 = ["N47° 15.54'", "E11° 19.94'", "1906", "79", "2000", "45", "LOWI 08"];
Airport = ["N27° 53.82'",
		"W82° 41.17'",
		"10",
		"351",
		"2966",
		"46",
		"KPIE St Pete-Clearwater International Airport 35R"];

Header = ReadHeader(I);
Coordinates = GetCoordinates(I);

ReportData(Out, Header, Coordinates, AirportLOWI08);
