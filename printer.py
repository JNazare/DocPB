import cups
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import base64
import re
from datetime import date, datetime

temp_folder = "temp/"
prints_folder = "static/prints/"
original_file = "example.png"
collage_file = "collage.jpg"
caption = "Brookline, Massachusetts - %s"

def saveImage(b64image, counter):
	filepath = temp_folder + str(counter) + ".png"
	data = re.sub('^data:image/.+;base64,', '', b64image)
	image = Image.open(BytesIO(base64.b64decode(data)))
	image.save(filepath)

def assemblePrint(image_filepaths):
	pwidth = 1500
	pheight=1000
	extra = 30

	iheight = 450
	iwidth = int(iheight*640/480) 
	offset = 640-iwidth
	border = 10

	images= []
	for filepath in image_filepaths:
		image = Image.open(filepath)
		images.append(image)

	for i in range (0,4):
		images[i].thumbnail((iwidth,iheight))

	forPrint = Image.new("RGB", (pwidth, pheight), "white")
	forPrint.paste(images[0],(offset+20,10))
	forPrint.paste(images[1],(offset+20,30+iheight))
	forPrint.paste(images[2],(offset+40+iwidth,10))
	forPrint.paste(images[3],(offset+40+iwidth,30+iheight))
	
	title = Image.open('border.jpg')
	title.thumbnail((1000,1000))
	forPrint.paste(title,(offset+50+iwidth*2,10)) 

	font = ImageFont.truetype('assets/Verdana.ttf', 35)
	draw = ImageDraw.Draw(forPrint)
	draw.text((offset+20, 930),caption % (date.today().strftime("%m/%d/%Y")),font=font, fill="#000000" )

	fheight=int(pheight+extra)
	fwidth=int(fheight*1.5)

	cropPrint = Image.new("RGB", (fwidth, fheight), "white")
	cropPrint.paste(forPrint, (int(0.75*extra),int(0.5*extra)))

	filename = prints_folder + datetime.now().strftime("%Y_%m_%d-%H_%M_%S") + ".jpg"
	cropPrint.save(filename)
	return filename

def sendToPrinter():
	conn = cups.Connection()
	printers = conn.getPrinters()

	printer_name = None
	for name in printers.keys():
		if ('selphy' in name.lower()):
			printer_name = name

	if printer_name:
		conn.printFile(printer_name, collage_file,"PhotoBooth",{"copies": str(1)})
		print("Printing photo...")

	else:
		print("I can't find the printer...")
