from PIL import Image

# Error codes of the module.
ERROR_OK = 0 # Everything went well.
ERROR_NOT_SUPPORTED = 1 # The image file type is not supported (not PNG nor JPEG).
ERROR_CONVERSION = 2 # Could not convert from JPEG to PNG.
ERROR_OPEN = 3 # Could not open the image.
ERROR_READ_MSG = 4 # Could not read message from the provided file.
ERROR_STR_TO_BIN = 5 # Could not convert the message string to binary format.
ERROR_EXTRACT_PIXELS = 6 # Could not extract the pixels from the image.
ERROR_ENCODING = 7 # Could not encode the message inside the list of pixels.
ERROR_SAVE_IMG = 8 # Could not save pixels to the new image.
ERROR_EXTRACT_MSG = 9 # Could not extract a valid message from the pixels of the image.
ERROR_SAVE_MSG = 10 # Could not save the extracted secret message to a file.
ERROR_MSG_TOO_LARGE = 11 # Could not encode the message inside the image. The message is too long.

# Some default filenames for testing purposes.
DEFAULT_ENCODE_OUTPUT = 'encoded.png'
DEFAULT_DECODE_OUTPUT = 'secret.txt'

# Definition of the allowed extensions.
JPEG_EXTENSIONS = ['.jpg', '.jpeg', '.jpe', '.JPG', '.JPEG', '.JPE']
PNG_EXTENSIONS = ['.png', '.PNG']

# Decides if the program outputs logs to the terminal (normal mode)
# or is silent (unit testing mode).
silent = False

# Define the beginning and end format tokens.
FORMAT_TOKEN = '$$$$$'

# Reads data from a file and returns it as a string.
def readStringFromFile(filename):
	try:
		with open(filename, 'r') as file:
			return file.read()
	except Exception as exception:
		log(exception)
		return None

# Writes a string into a file.
def writeStringToFile(string, filename):
	try:
		with open(filename, 'w') as file:
			file.write(string)
			return 0
	except Exception as exception:
		log(exception)
		return -1

# Opens an image object from file and returns it.
def openImage(filename):
	try:
		return Image.open(filename)
	except Exception as exception:
		log(exception)
		return None

# Saves the pixels provided into a new image.
def saveImage(filename, mode, size, pixels):
	try:
		image = Image.new(mode, size)
		image.putdata(pixels)
		image.save(filename)
	except Exception as exception:
		log(exception)
		return -1
	return 0

# Converts an image from a file format to another.
def convertImage(filenameFrom, filenameTo):
	try:
		Image.open(filenameFrom).save(filenameTo)
	except Exception as exception:
		log(exception)
		return -1
	return 0

# Extracts pixels from the provided image.
def extractPixelsFromImage(image):
	try:
		return list(image.getdata())
	except Exception as exception:
		log(exception)
		return None

# Logs something to the terminal.
def log(element):
	if not silent:
		print(element)

# Decides if the file extension corresponds to a JPEG image.
def isJPEG(extension):
	return extension in JPEG_EXTENSIONS

# Decides if the file extension corresponds to a PNG image.
def isPNG(extension):
	return extension in PNG_EXTENSIONS