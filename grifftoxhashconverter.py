#!C:\Python27\python.exe
# Author: Tomas Fearon
# Script: grifftoxhashconverter.py
# Purpose: Converts Griffeye Hash Files to the correct encoding so they can be imported into X-Ways

#import modules
import os, sys, codecs

## Define Usage
if len(sys.argv)!=2:
	print "\nUsage: Python hashconverter.py [Path to folder containing hash files] \n"
	sys.exit(0)

FilePath = sys.argv[1]

#define converter function - adds MD5 to top line and converts to UTF-8 encoding
def converter(hshfil):

	# Remove BOM from original file
	buffer_size = 4096
	bom_length = len(codecs.BOM_UTF8)
	
	with open(hshfil, "r+b") as fp:
		chunk = fp.read(buffer_size)
		if chunk.startswith(codecs.BOM_UTF8):
			i = 0
			chunk = chunk[bom_length:]
			while chunk:
				fp.seek(i)
				fp.write(chunk)
				i += len(chunk)
				fp.seek(bom_length, os.SEEK_CUR)
				chunk = fp.read(buffer_size)
			fp.seek(-bom_length, os.SEEK_CUR)
			fp.truncate()
	
	#Write new file with MD5 on first line. 
	md5 = "MD5\r\n"
	
	with codecs.open(hshfil, 'r+', encoding = "utf-8") as f:
		file_data = f.read()
		contents = md5 + file_data
		f.seek(0,0)
		f.write(contents)
		f.close()
		
#Iterate over files in directory with .txt extention
for subdir, dirs, files in os.walk(FilePath):
	for hshfil in files:
		if hshfil.endswith(".txt"):
			converter(hshfil)