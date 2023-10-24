import utils

# Opens the image provided at imgFilename and looks for a hidden message inside
# the Least Significant Bits of each pixel value. If a properly formatted secret message 
# is found, it is written to msgFilename.
def decodeAlgorithm(imgFilename, msgFilename):

	# Open the image.
	image = utils.openImage(imgFilename)
	if image == None:
		utils.log('ERROR: could not open the image')
		return utils.ERROR_OPEN
	else:
		utils.log('Image opened correctly')

	# Extract the pixels inside the image.
	pixels = utils.extractPixelsFromImage(image)
	if pixels == None:
		utils.log('ERROR: could not extract pixels from image')
		return utils.ERROR_EXTRACT_PIXELS
	else:
		utils.log('Pixels extracted from image')
	
	# Extract the binary data in the LSBs of the provided pixels.
	binaryString = extractBinaryMessageFromPixels(pixels)
	if binaryString == None:
		utils.log('ERROR: could not extract the LSBs of the pixels inside the image')
		return utils.ERROR_EXTRACT_MSG
	else:
		utils.log('Extracted the LSBs of all the pixels inside the image')

	# Get the string of the secret message, if there is one.
	secretMessage = extractSecretMessage(binaryString)
	if secretMessage == None:
		utils.log('ERROR: no secret message was found inside the image')
		return utils.ERROR_EXTRACT_MSG
	else:
		utils.log('Secret message found inside the image:')
		utils.log('{}'.format(secretMessage))
	
	# Finally, store the secret message inside the requested file.
	if utils.writeStringToFile(secretMessage, msgFilename) != 0:
		utils.log('ERROR: could not write secret message to file {}'.format(msgFilename))
		return utils.ERROR_SAVE_MSG
	else:
		utils.log('Secret message written to file')
	
	return utils.ERROR_OK


# Receives the list of pixels inside the suspected image and extracts the binary values
# of the least significant bits of each value of each pixel, into a string.
def extractBinaryMessageFromPixels(pixels):

	# Create an empty string to store the zeros and ones that we find inside the image.
	binaryData = ''

	# Loop through the pixels inside the image.
	for pixel in pixels:

		# If the pixel is iterable (a tuple), loop through all the values inside the pixel.
		if type(pixel) == tuple:
			binaryData += ''.join([leastSignificantBit(value) for value in pixel])
		
		# If not iterable (just an int), get that value only.
		elif type(pixel) == int:
			binaryData += leastSignificantBit(pixel)
		
		# For any other pixel type, return with error.
		else:
			utils.log('ERROR: unexpected pixel type: {}'.format(type(pixel)))
			return None
	
	return binaryData


# Returns the char corresponding to the Least Significant Bit of the 
# provided value, i.e., a '0' or a '1'.
def leastSignificantBit(value):
	return '0' if value % 2 == 0 else '1'


# Looks for the format tokens at the beginning and end of a suspected message. If found, returns the string
# representing the message itself.
def extractSecretMessage(binaryString):

	# First convert the binary string into a byte array.
	byteArray = bytes(int(binaryString[i : i + 8], 2) for i in range(0, len(binaryString), 8))

	# Create the binary representation of the format tokens.
	binaryToken = utils.FORMAT_TOKEN.encode('utf-8')

	# Try to find the format token at the beginning of the byte array.
	if not byteArray[0:len(binaryToken)] == binaryToken:
		utils.log('ERROR: the binary stream does not start with the expected {} token'.format(utils.FORMAT_TOKEN))
		return None
	
	# Discard the beginning.
	byteArray = byteArray[len(binaryToken):]

	# Try to find again the same sequence that marks the end of the message.
	nextTokenPosition = byteArray.find(binaryToken)
	if nextTokenPosition <= 0:
		utils.log('ERROR: the binary stream does not end with the expected {} token'.format(utils.FORMAT_TOKEN))
		return None
	
	# Discard the token at the end.
	byteArray = byteArray[0:nextTokenPosition]
	
	# Finally, try to decode the byte array into a string using utf-8 as the encoder.
	try:
		return byteArray.decode('utf-8')
	except Exception as exception:
		utils.log(exception)
		utils.log('ERROR: could not decode the byte stream of the secret message')
		return None
