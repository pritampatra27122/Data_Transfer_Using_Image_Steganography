import os
import math

import utils

# Reads an image from imgFilename and a text from msgFilename and encodes
# the text inside the image using Least Significant Bit Steganography.
# The output image is called outputFilename.
def encodeAlgorithm(imgFilename, msgFilename, outputFilename):

	# If the image is not JPEG or PNG, return with error.
	fileRoot, fileExtension = os.path.splitext(imgFilename)
	if not utils.isJPEG(fileExtension) and not utils.isPNG(fileExtension):
		utils.log('ERROR: the extension of the image is not supported')
		utils.log('ERROR: please provide a PNG or JPEG image')
		return utils.ERROR_NOT_SUPPORTED

	# If a JPEG image was provided, first convert it to PNG (a lossless 
	# format is needed not to lose the information of the message).
	filename = fileRoot + '.png'
	if utils.isJPEG(fileExtension):
		if utils.convertImage(imgFilename, filename) != 0:
			utils.log('ERROR: could not convert image from JPEG to PNG')
			return utils.ERROR_CONVERSION
		utils.log('JPEG image has been converted to PNG')
	else:
		utils.log('PNG image, no conversion needed')
	
	# Open the image.
	image = utils.openImage(filename)
	if image == None:
		utils.log('ERROR: could not open the image')
		return utils.ERROR_OPEN
	else:
		utils.log('Image opened correctly')

	# Get the string inside the provided message file.
	stringMessage = utils.readStringFromFile(msgFilename)
	if stringMessage == None:
		utils.log('ERROR: there was a problem reading the message from the provided file')
		return utils.ERROR_READ_MSG
	else:
		utils.log('Message read from file:')
		utils.log('{}'.format(stringMessage))

	# Transform the secret message to binary format.
	binaryMessage = stringToBinary(stringMessage)
	if binaryMessage == None:
		utils.log('ERROR: could not convert the message to binary format')
		return utils.ERROR_STR_TO_BIN
	else:
		utils.log('Message converted to binary format:')
		utils.log('{}'.format(binaryMessage))

	# Get all the pixel values in the image.
	pixels = utils.extractPixelsFromImage(image)
	if pixels == None:
		utils.log('ERROR: could not extract pixels from image')
		return utils.ERROR_EXTRACT_PIXELS
	else:
		utils.log('Pixels extracted from image')
	utils.log('First ten pixels in the input image:')
	for i in range(10):
		utils.log('\t{} -> {}'.format(i, pixels[i]))

	# Calculate the number of bits that can be used and check if the message fits.
	if numBitsInImage(pixels) < len(binaryMessage):
		utils.log('ERROR: the image is not big enough to fit the message')
		return utils.ERROR_MSG_TOO_LARGE

	# Get a new pixel list where the message is encoded in the least significant bits.
	newPixels = encodeMessageInPixels(pixels, binaryMessage)
	if newPixels == None:
		utils.log('ERROR: there was a problem encoding the message inside the image')
		return utils.ERROR_ENCODING
	else:
		utils.log('Message encoded correctly inside the image')
	utils.log('First ten pixels of the encoded image:')
	for i in range(10):
		utils.log('\t{} -> {}'.format(i, newPixels[i]))
	
	# Create the new image with the new pixel values and export it.
	if utils.saveImage(outputFilename, image.mode, image.size, newPixels) != 0:
		utils.log('ERROR: there was a problem saving the new pixels into the new image')
		return utils.ERROR_SAVE_IMG

	# If a PNG image was created on the fly from a JPEG image, remove it from the filesystem.
	if utils.isJPEG(fileExtension):
		try:
			os.remove(filename)
		except Exception as exception:
			utils.log(exception)
			pass

	return utils.ERROR_OK


# Appends the format tokens to the beginning and end of the string, then gets
# the binary representation of the string using utf-8 as the encoder. Returns a string
# of only '0' and '1' characters.
def stringToBinary(string):

	# Add format tokens to the string and transform into a byte array.
	try:
		byteList = bytearray(utils.FORMAT_TOKEN + string + utils.FORMAT_TOKEN, encoding='utf-8')
	except Exception as exception:
		utils.log(exception)
		return None

	# Join all those bytes in one big string of only 0 and 1 chars, like '0110101'.
	return ''.join([format(byte, '08b') for byte in byteList])


# Receives the list of pixels, flattened, found in the original image,
# and the string encoded in binary format. It then modifies the least significant
# bit of each value of each pixel to store the message.
def encodeMessageInPixels(pixels, binaryMessage):

	# A list to store the new pixel values.
	newPixels = []

	# Current position inside the binary message, and length of the message.
	currentIndex = 0
	messageLen = len(binaryMessage)

	# Iterate over all the pixels in the original image.
	for pixel in pixels:

		# If the pixel is iterable (a tuple), go through all its values.
		if type(pixel) == tuple:
			newPixel = ()
			for value in pixel:
				newPixel += (newPixelValue(value, binaryMessage, currentIndex, messageLen), )
				currentIndex += 1
		
		# If the pixel is not iterable, get only one new value.
		elif type(pixel) == int:
			newPixel = newPixelValue(pixel, binaryMessage, currentIndex, messageLen)
			currentIndex += 1
		
		# If the pixel is of any other type, return with error.
		else:
			utils.log('ERROR: unexpected pixel type: {}'.format(type(pixel)))
			return None

		# Get the new pixel inside the growing list of pixels.
		newPixels.append(newPixel)
	
	return newPixels


# Receives the current value inside a pixel and a binary message, and tries to
# modify the LSB of the value to store the next bit of the message.
# If the binary message has already been consumed, it just returns the value itself.
def newPixelValue(value, binaryMessage, currentIndex, messageLen):

	if currentIndex < messageLen:
		return math.floor(value / 2) * 2 + int(binaryMessage[currentIndex], 2)
	else:
		return value


# Receives the pixel list obtained from the image and calculates the number
# of bits it can fit inside.
# Remember we perform steganography only on the least significant bit of each value.
def numBitsInImage(pixels):
	if len(pixels) != 0:
		if type(pixels[0]) == tuple:
			return len(pixels) * len(pixels[0])
		elif type(pixels[0]) == int:
			return len(pixels)
	else:
		return 0