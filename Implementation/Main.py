import sys;
import os.path;
import json;

import IdentifyRunway;
import Display;
import Correct;

def ReadJSON(JSONPath, Path):
	File = open(JSONPath, "r");
	Data = json.loads(File.read());
	Data["Image"] = Path;
	File.close();
	return Data;

def Main():
	if (len(sys.argv) < 2):
		sys.exit("No input file path provided.");
	Path = sys.argv[1];
	JSONPath = os.path.splitext(Path)[0]+".txt";
	if (not os.path.exists(Path)):
		sys.exit("File does not exist.");
	if (not os.path.exists(JSONPath)):
		sys.exit("JSON file does not exist.");

	JSON = ReadJSON(JSONPath, Path);
	JSON = IdentifyRunway.IdentifyRunway(JSON);
	Display.Display(JSON);
	Correct.Correct(JSON);
	#DetermineOrigin(JSON);

if (__name__ == "__main__"):
	Main();
