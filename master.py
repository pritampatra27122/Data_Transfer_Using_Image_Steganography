import sys
sys.path.append('./lab')
from encode import encodeAlgorithm
from decode import decodeAlgorithm

def encode(imgFilename, msgFilename, outputFilename):
	return encodeAlgorithm(imgFilename, msgFilename, outputFilename)

def decode(imgFilename, outputFilename):
	return decodeAlgorithm(imgFilename, outputFilename)