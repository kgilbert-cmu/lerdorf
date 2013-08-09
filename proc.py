import os
import sys
import glob, codecs

def main():
	curdir = os.getcwd();
	filedir = curdir + "/sgm/*.sgm";
	filepath = glob.glob(filedir);
	with codecs.open("place.txt", 'w', encoding = 'UTF-8') as outfile:
		for filename in filepath:
			flag = 0;
			with codecs.open(filename, 'r', encoding = 'UTF-8') as infile:
				for line in infile.readlines():
					if (line.startswith("<Spatial")):
						outfile.write("<NEW_DOC>\n");
					if (line.startswith("<TEXT>")):
						flag = 1;
						outfile.write("<TEXT>\n");
					if (line.startswith("\n") and flag == 1):
						outfile.write("<PARA>\n");
					l1 = line.find('<');
					l2 = line.find('<', l1+1);
					if (line[l1+1] == 'P'):
						outfile.write(line[l1: l2] + '\n');
					while (line.find('<', l2) != -1):
						l1 = line.find('<', l2);
						l2 = line.find('<', l1+1);
						if (line[l1+1] == 'P'):
							outfile.write(line[l1: l2] + '\n');
if __name__=="__main__":
	main();