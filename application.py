import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import date

import pickle
import dropbox

import printer

app = Flask(__name__)

NUM_IMAGES = 4
IMAGE_FILES = ["temp/1.png", "temp/2.png", "temp/3.png", "temp/4.png"]
PROMPTS = ["prompt1", "prompt2", "prompt3", "prompt4"]
dbx = dropbox.Dropbox(os.environ['DROPBOX_API_KEY'])

def upload_photo_to_dropox(collage_path):
	with open(collage_path, 'rb') as f:
		date_string, time_string = collage_path.split("/")[-1].split("-")
		dbx.files_upload(f.read(), "/%s/%s" % (date_string, time_string))
		return True
	return False

@app.route("/", methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		return url_for('capture_photo', counter=1)
	return render_template("index.html")

@app.route("/capture/<int:counter>", methods=['GET', 'POST'])
def capture_photo(counter):
	if request.method == 'POST':
		b64image = request.form.get("b64image")
		printer.saveImage(b64image, counter)
		if counter < NUM_IMAGES:
			return url_for('capture_photo', counter=counter+1)
		else:
			collage_path = printer.assemblePrint(IMAGE_FILES)
			uploaded = upload_photo_to_dropox(collage_path)
			if collage_path and uploaded: 
				return url_for('printing', collage_path=collage_path)

	return render_template("capturephoto.html", prompt=PROMPTS[counter-1])

@app.route("/printing", methods=['GET'])
def printing():
	# printer.sendToPrinter()
	return render_template("printing.html", collage_path=request.args.get('collage_path'))

if __name__ == '__main__':
	app.run(debug=True)