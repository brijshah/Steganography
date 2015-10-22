#!/usr/bin/python

#-----------------------------------------------------------------------------
#--	SOURCE FILE:	decode.py -   Steganography Decoder
#--
#--	FUNCTIONS:		decode()
#--					createFile()
#--					main					
#--
#--	DATE:			October 5, 2015
#--
#--	DESIGNERS:		Brij Shah
#--
#--	PROGRAMMERS:	Brij Shah
#--
#--	NOTES:
#-- decode takes in a cover image and extracts the embedded data from it. The
#-- file name and file size are restored intact just as the original data
#-- was put in.
#-----------------------------------------------------------------------------

from PIL import Image
import sys, array, binascii, argparse

parser = argparse.ArgumentParser(description='Steganography')
parser.add_argument('-c', '--cover', dest='coverImage', help='cover image to decode', required=True)
args = parser.parse_args()

bitList = ""
encodedMessageSize = 0
binaryFileName = []
encodedMessage = ""

#-----------------------------------------------------------------------------
#-- FUNCTION:       decode()
#--
#-- NOTES:
#-- decode takes in a cover image and converts it to bits. The last bits are
#-- stored into a list and converted back to create a new data file
#-- (the original file that was originally embedded into it). It checks for
#-- the null terminator to ensure the right file name and file size are
#-- gathered for later use when re-creating the data file.
#-----------------------------------------------------------------------------
def decode():
	coverImage = Image.open(args.coverImage).convert('RGB')
	pixels = coverImage.load()
	width, height = coverImage.size
	global bitList
	global binaryFileName
	global encodedMessageSize
	encodedMessageSize = 208
	encodedMessageIndex = 0
	count = 0
	byte = ""
	byteList = []
	fileSize = ""
	binaryDelimiter = "00000000"

	for w in range(width):
		for h in range(height):
			red, green, blue = pixels[w,h]
			redPixels = str(bin(red)[2:].zfill(8))[7]
			greenPixels = str(bin(green)[2:].zfill(8))[7]
			bluePixels = str(bin(blue)[2:].zfill(8))[7]
			colourBitList = [redPixels, greenPixels, bluePixels]

			for i in range(len(colourBitList)):
				byte += colourBitList[i]
				if len(byte) == 8:
					byteList.append(byte)
					if byte == binaryDelimiter and count == 0:
						binaryFileName = byteList[0:len(byteList) - 1]
						byteList = []
						count += 1
					elif byte == binaryDelimiter and count == 1:
						encodedMessageSize = ''.join(binascii.unhexlify('%x' % int(b,2)) for b in byteList[0:len(byteList) - 1])
						byteList = []
						count += 1
						continue
					byte = ""

				if count == 2:
					if encodedMessageIndex < int(encodedMessageSize):
						bitList += colourBitList[i]
						encodedMessageIndex += 1
					else:
						return

#-----------------------------------------------------------------------------
#-- FUNCTION:       createFile()
#--
#-- NOTES:
#-- createFile takes the data gathered from the decode method and converts 
#-- it to ascii if needed, it then opens a file for writing and appends the
#-- necessary data back to it. The filename is gathered from the decode 
#-- method and is passed to the fileHandler to create the file with the same
#-- name that was originally encoded.
#-----------------------------------------------------------------------------
def createFile():
	global encodedMessage
	for i in range(int(encodedMessageSize)):
		encodedMessage += bitList[i]
	writeList = []

	for i in range (0, len(encodedMessage)/8):
		writeList.append(int(encodedMessage[i*8:(i+1) * 8], 2))

	fileByteList = array.array('B', writeList).tostring()
	dataToFile = bytearray(fileByteList)

	encodedFilename = ''.join(binascii.unhexlify('%x' % int(b,2)) for b in binaryFileName[0:len(binaryFileName)])
	fileHandler = open(encodedFilename, 'w')
	fileHandler.write(dataToFile)

#-----------------------------------------------------------------------------
#-- FUNCTION:       main()
#--
#-- NOTES:
#-- the pseudomain method which cals the decode and create file methods. 
#-- the python main method calls this method.
#-----------------------------------------------------------------------------
def main():
	decode()
	createFile()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print "Exiting.."

	


 
