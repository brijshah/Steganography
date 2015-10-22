#!/usr/bin/python

#-----------------------------------------------------------------------------
#--	SOURCE FILE:	analysis.py -   Stego LSB Analysis
#--
#--	FUNCTIONS:		analyze(filename)
#--					main					
#--
#--	DATE:			October 5, 2015
#--
#--	DESIGNERS:		Brij Shah
#--
#--	PROGRAMMERS:	Brij Shah
#--
#--	NOTES:
#--	Statistical analysis of an image which detects steg'd images which have
#-- been altered using the LSB algorithm.
#-----------------------------------------------------------------------------

import sys, os, argparse, numpy
import matplotlib.pyplot as plt
from PIL import Image

parser = argparse.ArgumentParser(description='Analyze Stego LSB')
parser.add_argument('-f', '--filename', dest='filename', help='file to analyze', required=True)
args = parser.parse_args()

#-----------------------------------------------------------------------------
#-- FUNCTION:       analyze(filename)
#--
#-- VARIABLES(S):   filename - the image to be analyzed
#--
#-- NOTES:
#-- analyze splits the image into blocks. It then computes the average value 
#-- of the LSB's for each block. The plot of the averages should be roughly 0.5
#-- for the areas that contain the embedded messages.
#-----------------------------------------------------------------------------
def analyze(filename):
	blockSize = 100
	image = Image.open(filename)
	(width, height) = image.size
	print "Image size: %dx%s pixels. " % (width, height)
	convertedImage = image.convert('RGB').getdata()

	redList = []
	greenList = []
	blueList = []

	for w in range(width):
		for h in range(height):
			(red,green,blue) = convertedImage.getpixel((w,h))
			redList.append(red & 1)
			greenList.append(green & 1)
			blueList.append(blue & 1)

	averageRed = []
	averageGreen = []
	averageBlue = []

	for i in range(0, len(redList), blockSize):
		averageRed.append(numpy.mean(redList[i:i + blockSize]))
		averageGreen.append(numpy.mean(greenList[i:i + blockSize]))
		averageBlue.append(numpy.mean(blueList[i:i + blockSize]))

	numOfBlocks = len(averageRed)
	blocks = [i for i in range(0, numOfBlocks)]
	plt.axis([0,len(averageRed), 0, 1])
	plt.ylabel('Average LSB per block')
	plt.xlabel('Block Number')
	plt.plot(blocks, averageBlue, 'bo')

	plt.show()

#-----------------------------------------------------------------------------
#-- FUNCTION:       main()
#--
#-- NOTES:
#-- The pseudomain of the application which simply calls the analyze method.
#-----------------------------------------------------------------------------
def main():
	analyze(args.filename)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print "Exiting.."
	except IOError:
		print args.filename + " not found. Try again"
