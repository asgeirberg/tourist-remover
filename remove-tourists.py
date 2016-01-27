#! /usr/bin/env python
# -*- coding: utf-8 -*-

''' This program takes in photos and returns a picture where each pixel has the median RBG value of the same pixels in 
	other pictures. This is e.g. useful for photographing a crowded place and yet get out the place empty, 
	at least theoretically'''

import os
import sys
import numpy as np

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from PIL import Image

def get_parser():
    """Get parser object"""
   
    parser = ArgumentParser(description=__doc__,
                           formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-o", "--output",
                        dest="output",
                        default="out.jpg",
                        help="Filename to write output"
                        )
    parser.add_argument("-d", "--directory",
                        dest="directory",
                        default=os.curdir,
                        help="Path to scan for photos"
                        )
    return parser

def get_filenames(directory):
	''' Get the filenames of all the files in a directory. Returns a list of files.'''
	#TODO: Put in error handling for the filenames

	files = [f for f in os.listdir(directory) if os.path.isfile(f)] #list all the files in the directory.

	for f in files: #take care of unicode stuff.
 		 f = unicode(f, "utf-8")

 	return files	

def get_photos(directory):
	''' Get the filenames of all the photos in a directory. Returns a list of photos.'''
	#TODO: Let the user pass his own directory
	photo_list = []

	for f in get_filenames(directory): #get all the filename in the directory and filter out the non-photos.
		try:
			with Image.open(f) as im: #if PIL cannot recognise the file as a photo, this will fail.
				photo_list.append(f)
		except IOError:
			pass

	return photo_list

def open_image(photo):
	'''Opens an image and returns an Image object.'''
	try:
		image = Image.open(photo)

	except IOError:
		print "ERROR: Couldn't open " + photo + ", skipping..."
		image = None
	
	return image.convert('RGB')
	
def create_new_image(image_matrices):
	'''Creates a new image by taking the median of the list of images that are passed to it. Returns an image.'''

	image_stack = np.concatenate([im[..., None] for im in image_matrices], axis = 3)
	median_image = np.median(image_stack, axis = 3)

	return Image.fromarray(median_image.astype('uint8'))

def save_image(image, filename):
	'''Saves the image passed to it as a jpg.'''

	if image.mode != 'RGB':
		image = image.convert('RGB')
    
	try:
		image.save(filename)
	except IOError:
		print "ERROR: Couldn't save " + photo + ", aborting..."
		
		return False

	return True	

if __name__ == "__main__":
	args = get_parser().parse_args()
	pathname = os.path.abspath(args.directory)

	if not os.path.isdir(pathname):
		print args.directory + " is not a directory.\nQuitting..."
		sys.exit() #if the user puts in a malformed directory, nothing is done.

	if len(get_photos(args.directory)) < 10:
		print("Having at least 10 photos is recommended.")

	images_matrices = [] #list of numpy matrices, each containing a bitmap of an image

	for photo in get_photos(args.directory):
		print "Processing " + photo + "..."

		if open_image(photo) != None:  
			image_matrix = np.array(open_image(photo))
			images_matrices.append(image_matrix)

	if len(images_matrices) > 0:
		img = create_new_image(images_matrices)
		save_image(img, args.output)
	else:
		print "Couldn't process any images, quitting..."




