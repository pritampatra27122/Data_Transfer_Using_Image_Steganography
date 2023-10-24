import sys

from encode import encodeAlgorithm
from decode import decodeAlgorithm
import utils


# The main function basically checks the command line arguments
# and decides to call either the encode or the decode routines.
def main():

	# Check that the necessary command line arguments were provided.
	if len(sys.argv) != 4:
		utils.log('ERROR: incorrect syntax')
		printUsage()
		return -1

	# Store command line arguments for later.
	imgFilename = sys.argv[2]
	msgFilename = sys.argv[3]

	# Decide if we have to encode or decode:
	if sys.argv[1] == '-e':
		utils.log('Encoding...')
		if encodeAlgorithm(imgFilename, msgFilename, utils.DEFAULT_ENCODE_OUTPUT) != utils.ERROR_OK:
			utils.log('ERROR: there was a problem encoding the message')
			return -1
		else:
			utils.log('Encoding executed correctly')
			return 0
	elif sys.argv[1] == '-d':
		utils.log('Decoding...')
		if decodeAlgorithm(imgFilename, msgFilename) != utils.ERROR_OK:
			utils.log('ERROR: there was a problem decoding the message')
			return -1
		else:
			utils.log('Decoding executed correctly')
			return 0
	else:
		utils.log('ERROR: option "{}" not recognized'.format(sys.argv[1]))
		printUsage()
		return -1


# Prints the correct usage of the application to the screen.
def printUsage():
	utils.log('\nUsage:')
	utils.log('\tpython3 lab.py -[e/d] <img_filename> <msg_filename>\n')

if __name__ == '__main__':
	main()