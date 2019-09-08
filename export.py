import sys
import os
sys.path.append(os.getcwd())
import tkinter as tk
import tkinter.filedialog as filedialog
import PIL.Image as Image
import json
import re
from DMIParse import parseFile,parseText

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfiles(defaultextension=".dmi")

destination_path = filedialog.askdirectory()


for file in file_path:
	metadata = parseFile(file.name)

	if(metadata == False):
		continue

	im = Image.open(file.name)
	statenames = list(metadata["states"])
	fallback = 0
	try:
		icoh = int(metadata["height"])
		icow = int(metadata["width"])
	except KeyError:
		for value in statenames:
			fallback = fallback + (int(metadata["states"][value]["frames"]) * int(metadata["states"][value]["dirs"]))
		icow = im.width / fallback
		icoh = im.height
	

	amtwide = int(im.width / icow)
	amthigh = int(im.height / icoh)

	
	index = 0
	lastw = 0
	lasth = 0
	toskip = 0
	animindex = 1
	for y in range(amthigh):
		if(index==len(statenames)):
				break
		for x in range(amtwide):
			if(index==len(statenames)):
				break
			if(toskip > 0):
				toskip = toskip - 1
				animindex = animindex + 1
			else:
				toskip = int(metadata["states"][statenames[index]]["frames"]) * int(metadata["states"][statenames[index]]["dirs"]) - 1
				animindex = 1
			cropped = im.crop((x*icow,y*icoh,(1 + x)*icow,(1 + y)*icoh))

			ofilen = re.sub(".*/","",im.filename)

			if(int(metadata["states"][statenames[index]]["frames"]) - 1):
				cropped.save(destination_path + "/" + ofilen + "-" + statenames[index] + "[dir_" + metadata["states"][statenames[index]]["dirs"] + "][frame_" + str(animindex) + "].png")
			else:
				cropped.save(destination_path + "/" + ofilen + "-" + statenames[index] + "[dir_" + metadata["states"][statenames[index]]["dirs"] + "].png")
			print("updating index in " + str(toskip) + " frames.done with icon at pos(XY): " + str(x) + "," + str(y) + statenames[index])
			
			cropped.close()
			if(toskip == 0):
				index = index + 1
	im.close()
print("done")