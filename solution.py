#!/usr/bin/python3

import sys
from os import listdir

# -- load all filenames with .csv extension into a list
fileList = [f for f in listdir() if ".csv" in f]
#print(fileList)

for element in fileList:
	with open(element) as file:
		print(file.read())