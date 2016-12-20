import codecs,sys

filename = sys.argv[1]
#sys.stdout = codecs.getwriter('sjis')(sys.stdout)

with codecs.open(filename, "r", "utf-8") as f:
	for l in f.readlines():
		print l.rstrip()
