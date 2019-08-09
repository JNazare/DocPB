import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import date

import pickle
import dropbox
import random
import printer

app = Flask(__name__)

NUM_IMAGES = 4
IMAGE_FILES = ["temp/1.png", "temp/2.png", "temp/3.png", "temp/4.png"]
ALL_PROMPTS = ["a smiling photo", "a serious one", "a silly one", "a crazy one","a playful one","a 'Sam-and-Anneli' one","a pouty one","a ridiculous one","a stylish one","a howling one"]
dbx = dropbox.Dropbox(os.environ['DROPBOX_API_KEY'])



def upload_photo_to_dropox(collage_path):
	with open(collage_path, 'rb') as f:
		date_string, time_string = collage_path.split("/")[-1].split("-")
		dbx.files_upload(f.read(), "/%s/%s" % (date_string, time_string))
		return True
	return False

@app.route("/", methods=['GET', 'POST'])
def index():
	global PROMPTS
	PROMPTS = random.sample(ALL_PROMPTS,4)
	PROMPTS[0] = 'First, '+PROMPTS[0]+'...'
	PROMPTS[1] = 'Next, '+PROMPTS[1]+'...'
	PROMPTS[2] = 'Now, '+PROMPTS[2]+'...'
	PROMPTS[3] = 'Last, '+PROMPTS[3]+'!'

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
	collage_path = request.args.get('collage_path')
	printer.sendToPrinter(collage_path)
	return render_template("printing.html", collage_path=collage_path)

if __name__ == '__main__':
	app.run(debug=True)