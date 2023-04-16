# Given a pdf file, convert it to a series of images and save them in a tmp folder.

import sys
import os
import pdf2image

def convert_to_images(filename):
	"""
	Converts a pdf to images using the pdf2image library. The images are saved in a tmp folder.
	If tmp folder does not exist, it will be created.
	If there is a conflict with the tmp folder, the program will overwrite the files.
	@param filename: the name of the pdf file
	@return: None
	"""
	# open file for reading
	infile = open(filename, "r")

	# throw error if file is not pdf
	if not filename.endswith(".pdf"):
		print("Error: file is not pdf")
		sys.exit(1)

	# convert pdf to image
	images = pdf2image.convert_from_path(filename)

	# save images into tmp folder
	# make tmp folder if it doesn't exist
	if not os.path.exists("tmp"):
		os.makedirs("tmp")

	# filename without extension
	filename = filename.split(".")[0]

	# save images
	for i in range(len(images)):
		images[i].save(f"tmp/{filename}_{i}.png")

	# close file
	infile.close()

################## TESTING ##################
if __name__ == "__main__":
	# get name from command line
	if len(sys.argv) < 2:
		print("Usage: converter.py filename")
		sys.exit(1)
	filename = sys.argv[1]

	# throw error if file does not exist
	if not os.path.exists(filename):
		print("Error: file does not exist")
		sys.exit(1)

	convert_to_images(filename)