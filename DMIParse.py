from pyparsing import Word,nums,alphanums,OneOrMore,Optional,Dict,Group,Suppress,alphas8bit,QuotedString,ParseException
import PIL.Image as Image
import re

def parseFile(file):
	if(file.endswith(".dmi") == False):
		return False

	try:
		im = Image.open(file)
	except IOError as e:
		a = e
		e = a
		print("Unable to open file(" + file + ")")
	try:
		return parseText(im.info["Description"])
	except KeyError:
		return False

def parseText(metadata):
	try:
		header = (
					"# BEGIN DMI"
					"version = " + OneOrMore(Word(nums + ",.").setResultsName("DMIVer")) +
					Optional("width = " + Word(nums).setResultsName("width") +
					"height = " + Word(nums).setResultsName("height"))
				) 

		states = (
					Suppress("state = ") + QuotedString("\"").setResultsName("name") +
					"dirs = "  + Word(nums).setResultsName("dirs") +
					"frames = " + Word(nums).setResultsName("frames") +
					Optional("delay = " + OneOrMore(Word(nums + ",.")).setResultsName("delay"))+
					Optional("loop =" + Word(nums)) +
                                        Optional("rewind =" + Word(nums))
				)

		full = header + Dict(Optional(OneOrMore(Group(states)))).setResultsName("states")

		clean = re.sub(r"(\n)|(\t)","",metadata)
		print(clean)
		return full.parseString(clean).asDict()
	except ParseException as e:
		e = e
		raise Exception("Unable to parse DMI metadata")
