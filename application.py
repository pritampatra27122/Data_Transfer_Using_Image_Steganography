import os
import sys
import random
import string
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename

import master

# Define the folders where we will perform steganography.
UPLOAD_FOLDER_ENCODE = os.path.abspath('./uploads/encode')
UPLOAD_FOLDER_DECODE = os.path.abspath('./uploads/decode')

# Create the folders if they do not exist.
Path(UPLOAD_FOLDER_ENCODE).mkdir(parents=True, exist_ok=True)
Path(UPLOAD_FOLDER_DECODE).mkdir(parents=True, exist_ok=True)

# Only these extensions are allowed for encoding.
ALLOWED_EXTENSIONS_ENCODE = ['.jpg', '.jpeg', '.jpe', '.png', '.JPG', '.JPEG', '.JPE', '.PNG']

# Only these extensions are allowed for decoding.
ALLOWED_EXTENSIONS_DECODE = ['.png', '.PNG']

# Create the app.
app = Flask(__name__)
app.config['UPLOAD_FOLDER_ENCODE'] = UPLOAD_FOLDER_ENCODE
app.config['UPLOAD_FOLDER_DECODE'] = UPLOAD_FOLDER_DECODE
socketio = SocketIO(app)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/encode', methods=['GET', 'POST'])
def encode():
	if request.method == 'POST':

		# Check that the POST request includes a file.
		try:
			if not 'file' in request.files:
				print('ERROR: no image file has been provided')
				return redirect(request.url)
		except Exception as exception:
			print(exception)
			return redirect(request.url)
		print('An image file has been provided')
		image = request.files['file']

		# Check that the image filename is valid.
		if image.filename == '':
			print('ERROR: image filename is not valid')
			return redirect(request.url)
		else:
			print('The image filename is valid')
		
		# Check the extension of the image.
		partialImageFilename = secure_filename(image.filename)
		fileExtension = os.path.splitext(partialImageFilename)[1]
		if fileExtension not in ALLOWED_EXTENSIONS_ENCODE:
			print('ERROR: the image provided does not have a valid extension')
			return redirect(request.url)
		else:
			print('The image has a valid extension')
		
		# Check that the POST request includes a message.
		if 'message' not in request.form:
			print('ERROR: no message has been provided')
			return redirect(request.url)
		else:
			message = request.form['message']
		
		# Decide some input filenames and store the files at the appropriate locations.
		randomId = createRandomId()
		finalImageFilename = os.path.join(app.config['UPLOAD_FOLDER_ENCODE'], randomId + 'original' + fileExtension)
		image.save(finalImageFilename)
		finalMsgFilename = os.path.join(app.config['UPLOAD_FOLDER_ENCODE'], randomId + 'message.txt')
		with open(finalMsgFilename, 'w') as file:
			file.write(message)
		
		# Decide a name for the output image and call the encoding algorithm.
		partialOutputFilename = randomId + 'encoded.png'
		outputFilename = os.path.join(app.config['UPLOAD_FOLDER_ENCODE'], partialOutputFilename)
		if master.encode(finalImageFilename, finalMsgFilename, outputFilename) != 0:
			print('ERROR: there was a problem encoding')
			return redirect(request.url)
		
		return redirect(url_for('encoded', filename=partialOutputFilename))
	
	else:
		return render_template('encode.html')

@app.route('/decode', methods=['GET', 'POST'])
def decode():
	if request.method == 'POST':

		# Check that the POST request includes a file.
		try:
			if not 'file' in request.files:
				print('ERROR: no image file has been provided')
				return redirect(request.url)
		except Exception as exception:
			print(exception)
			return redirect(request.url)
		print('An image file has been provided')
		image = request.files['file']

		# Check that the image filename is valid.
		if image.filename == '':
			print('ERROR: image filename is not valid')
			return redirect(request.url)
		else:
			print('The image filename is valid')
		
		# Check the extension of the image.
		partialImageFilename = secure_filename(image.filename)
		fileExtension = os.path.splitext(partialImageFilename)[1]
		if fileExtension not in ALLOWED_EXTENSIONS_DECODE:
			print('ERROR: the image provided does not have a valid extension')
			return redirect(request.url)
		else:
			print('The image has a valid extension')
		
		# Decide a filename for the input image and store it.
		randomId = createRandomId()
		finalImageFilename = os.path.join(app.config['UPLOAD_FOLDER_DECODE'], randomId + 'encoded' + fileExtension)
		image.save(finalImageFilename)

		# Create a name for the decoded text and call the decode algorithm.
		partialOutputFilename = randomId + 'secret.txt'
		outputFilename = os.path.join(app.config['UPLOAD_FOLDER_DECODE'], partialOutputFilename)
		if master.decode(finalImageFilename, outputFilename) != 0:
			print('ERROR: there was a problem decoding')
			return redirect(request.url)
		
		# If decoding went well, redirect the user to see the text.
		return redirect(url_for('decoded', filename=partialOutputFilename))

	else:
		return render_template('decode.html')

@app.route('/encoded/<filename>')
def encoded(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER_ENCODE'], filename)

@app.route('/decoded/<filename>')
def decoded(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER_DECODE'], filename)

@app.route('/about')
def about():
	return render_template('about.html')

def createRandomId():
	return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=20)) + '_'

if __name__ == '__main__':
	app.debug = True
	socketio.run(app, host='0.0.0.0', port=8081)
