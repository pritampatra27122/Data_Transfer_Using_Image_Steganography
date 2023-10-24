import unittest
from filecmp import cmp
import os

from encode import encodeAlgorithm
from decode import decodeAlgorithm
import utils


class TestImages(unittest.TestCase):

	# This function will perform compression, then decompression.
	# If compression or decompression fails, it will fail.
	# If both go well, it will assert equality between the initial and the decoded messages.
	def runCompleteTest(self, imageFile, msgFile):

		# Remove garbage files if they are present
		try:
			os.remove(utils.DEFAULT_ENCODE_OUTPUT)
		except OSError:
			pass
		try:
			os.remove(utils.DEFAULT_DECODE_OUTPUT)
		except OSError:
			pass
		
		# Execute the tests.
		self.assertEqual(encodeAlgorithm(imageFile, msgFile, utils.DEFAULT_ENCODE_OUTPUT), utils.ERROR_OK)
		self.assertEqual(decodeAlgorithm(utils.DEFAULT_ENCODE_OUTPUT, utils.DEFAULT_DECODE_OUTPUT), utils.ERROR_OK)
		self.assertTrue(cmp(msgFile, utils.DEFAULT_DECODE_OUTPUT))

		# Remove garbage files again.
		try:
			os.remove(utils.DEFAULT_ENCODE_OUTPUT)
		except OSError:
			pass
		try:
			os.remove(utils.DEFAULT_DECODE_OUTPUT)
		except OSError:
			pass

	# Test RGB and RGBA images, PNG format, normal ASCII text.
	def test_PNG_RGBA_ASCII(self):
		utils.silent = True
		self.runCompleteTest('test_files/png_16rgba.png', 'test_files/txt_ascii.txt')
		self.runCompleteTest('test_files/png_16rgb.png', 'test_files/txt_ascii.txt')
		self.runCompleteTest('test_files/png_8rgb.png', 'test_files/txt_ascii.txt')
		self.runCompleteTest('test_files/png_HDrgba.png', 'test_files/txt_ascii.txt')

	# Test Black and White images, PNG format, normal ASCII text.
	def test_PNG_BW_ASCII(self):
		utils.silent = True
		self.runCompleteTest('test_files/png_8l.png', 'test_files/txt_ascii.txt')
	
	# Test all JPEG images, normal ASCII text.
	def test_JPEG_ASCII(self):
		utils.silent = True
		self.runCompleteTest('test_files/jpg_small.jpg', 'test_files/txt_ascii.txt')
		self.runCompleteTest('test_files/jpg_big.jpg', 'test_files/txt_ascii.txt')
		self.runCompleteTest('test_files/jpg_huge.jpg', 'test_files/txt_ascii.txt')
	
	# Test a big ASCII text on a big and a small image.
	def test_ASCII_huge(self):
		utils.silent = True
		self.runCompleteTest('test_files/jpg_huge.jpg', 'test_files/txt_ascii_huge.txt')
		self.assertEqual(encodeAlgorithm('test_files/png_8l.png', 'test_files/txt_ascii_huge.txt', utils.DEFAULT_ENCODE_OUTPUT), utils.ERROR_MSG_TOO_LARGE)

	# Test the sample UTF-8 file with RGBA PNG images.
	def test_PNG_RGBA_UTF8(self):
		utils.silent = True
		self.runCompleteTest('test_files/png_16rgba.png', 'test_files/txt_utf8.txt')
		self.runCompleteTest('test_files/png_16rgb.png', 'test_files/txt_utf8.txt')
		self.runCompleteTest('test_files/png_8rgb.png', 'test_files/txt_utf8.txt')
		self.runCompleteTest('test_files/png_HDrgba.png', 'test_files/txt_utf8.txt')

	# Test the sample UTF-8 file with BW PNG images.
	def test_PNG_BW_UTF8(self):
		utils.silent = True
		self.assertEqual(encodeAlgorithm('test_files/png_8l.png', 'test_files/txt_utf8.txt', utils.DEFAULT_ENCODE_OUTPUT), utils.ERROR_MSG_TOO_LARGE)

	# TODO: test a non JPEG and non PNG image.

	# TODO: test decode with an image that does not contain a message hidden.

if __name__ == '__main__':
	unittest.main()