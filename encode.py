#!/usr/bin/python

#-----------------------------------------------------------------------------
#--	SOURCE FILE:	encode.py -   Steganography Encoder
#--
#--	FUNCTIONS:		encode()
#--					main					
#--
#--	DATE:			October 5, 2015
#--
#--	DESIGNERS:		Brij Shah
#--
#--	PROGRAMMERS:	Brij Shah
#--
#--	NOTES:
#--	encoder takes any type of data and stores it into a cover image.  The 
#-- data is converted into bits, and the least significant bit in each pixel
#-- is swapped with one bit from the data, thus encoding 'secret' data into
#-- the cover medium.
#-----------------------------------------------------------------------------

import sys, os, argparse, binascii, array
from PIL import Image

#Command Line Argument Parser
parser = argparse.ArgumentParser(description='Steganography')
parser.add_argument('-c', '--cover', dest='coverImage', help='cover image')
parser.add_argument('-s', '--secret', dest='secretData', help='secret data')
parser.add_argument('-e', '--extension', dest='fileExtension', help='save file extension', required=True)
args = parser.parse_args()

#Globals
byteList = ""
binaryDelimiter = "00000000"
binaryFilename = ""
binaryFileData = ""

#File name and Conversions
filename = os.path.basename(args.secretData)
for f in filename:
	binaryFilename += format(ord(f), 'b').zfill(8)

byteList += binaryFilename + binaryDelimiter

with open(filename, 'rb') as myfile:
	data_byte_array = bytearray(myfile.read())

for byte in data_byte_array:
	binaryFileData += bin(byte)[2:].zfill(8)

filesize = list(str(len(binaryFileData)))
filesizeBinary = ''.join(format(ord(x), 'b').zfill(8) for x in filesize)
filesizeBinary += binaryDelimiter

byteList += filesizeBinary + binaryFileData

#-----------------------------------------------------------------------------
#-- FUNCTION:       check_size(cover, data)
#--
#-- VARIABLES(S):   cover - the cover image
#--					data = the data to be hidden
#--
#-- NOTES:
#-- takes in a cover image and any type of data to check whether the cover 
#-- image has enough room to store the data.
#-----------------------------------------------------------------------------
def check_size(cover, data):
	numPixels = len(cover.getdata()) * 8 * 3
	maxBits = str(numPixels)
	secretDataSize = os.path.getsize(data)
	totalDataSize = str((len(data) * (8 + 4)) + len(bin(secretDataSize)[2:]) + (len(data) * 8) + 16)
	#before stego, check size and see if cover image is big enough for secret image

#-----------------------------------------------------------------------------
#-- FUNCTION:       encode()
#--
#-- NOTES:
#-- this function opens the cover image and gathers all the pixels by appending
#-- them to a list. It then converts the pixels to bits and swaps the least
#-- significant bit with the bit from the secret data file. It also keeps
#-- track of the file name and file size(which is used for decoding)
#-----------------------------------------------------------------------------
def encode():
	cover = Image.open(args.coverImage).convert('RGB')
	pixels = cover.load()
	width, height = cover.size
	indexByteList = 0;
	lastPixelBit = 0;

	for w in range(width):
		for h in range(height):
			red, green, blue = pixels[w,h]
			redPixels = list(bin(red)[2:].zfill(8))
			greenPixels = list(bin(green)[2:].zfill(8))
			bluePixels = list(bin(blue)[2:].zfill(8))
			rgbList = [redPixels, greenPixels, bluePixels]
			rgbDecimalVal = []

			if lastPixelBit == 0:
				for rgbBitVal in rgbList:
					rgbBitVal[7] = byteList[indexByteList]
					indexByteList += 1
					rgbDecimalVal.append(int(''.join(str(e) for e in rgbBitVal), 2))
				pixels[w,h] = (rgbDecimalVal[0],rgbDecimalVal[1],rgbDecimalVal[2])

			if len(byteList) - indexByteList < 3:
				if lastPixelBit == 0:
					lastPixelBit = 1
					continue;
				else:
					rgbDecimalVal = [red,green,blue]
					for i in range(len(byteList) - indexByteList):
						rgbList[i][7] = byteList[indexByteList]
						rgbDecimalVal[i] = (int(''.join(str(e) for e in rgbList[i]), 2))
					pixels[w,h] = (rgbDecimalVal[0],rgbDecimalVal[1],rgbDecimalVal[2])
	cover.save("hidden" + args.fileExtension)

#-----------------------------------------------------------------------------
#-- FUNCTION:       main()
#--
#-- NOTES:
#-- the pseudomain method which is called in the pyton main method below. 
#-- this method also calls the encode method above.
#-----------------------------------------------------------------------------
def main():
	encode()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print "Exiting.."