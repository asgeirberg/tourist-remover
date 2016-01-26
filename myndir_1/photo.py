#! /usr/bin/env python
# -*- coding: utf-8 -*-

''' This program takes in photos and returns a picture where each pixel has the median RBG value of the same pixels in 
	other pictures. This is e.g. useful for photographing a crowded place and yet get out the place empty, 
	at least theoretically'''

import os
import sys

import numpy as np
from PIL import Image

def get_filenames():
	''' Get the filenames of all the files in a directory. Returns a list of files.'''
	#TODO: Put in error handling for the filenames

	files = [f for f in os.listdir(os.curdir) if os.path.isfile(f)] #list all the files in the directory.

	for f in files: #take care of unicode stuff.
 		 f = unicode(f, "utf-8")

 	return files	

def get_photos():
	''' Get the filenames of all the photos in a directory. Returns a list of photos.'''
	#TODO: Let the user pass his own directory
	photo_list = []

	for f in get_filenames(): #get all the filename in the directory and filter out the non-photos.
		try:
			with Image.open(f) as im: #if PIL cannot recognise the file as a photo, this will fail.
				photo_list.append(f)
		except IOError:
			pass

	return photo_list

def open_image(photo):
	'''Opens an image and returns an Image object.'''
	try:
		img = Image.open(photo)

	except IOError:
		print "ERROR: Couldn't open " + photo + ", skipping..."
		img = None
	
	return img
	
def create_new_image(images_matrices):
	'''Creates a new image by taking the median of the list of images that are passed to it. Returns an image.'''

	images = np.dstack(tuple(images_matrices)) #dstack only accepts tuples. 
	image = np.median(images, axis=0)

	return Image.fromarray(image)

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

if len(get_photos()) < 10:
	print("Having at least 10 photos is recommended.")

images_matrices = [] #list of numpy matrices, each containing a bitmap of an image

for f in get_photos():
	print "Processing " + f + "..."

	if open_image(f) != None:  
		image_matrix = np.array(open_image(f))
		images_matrices.append(image_matrix)

if len(images_matrices) > 0:
	img = create_new_image(images_matrices)
	save_image(img, "out.jpg")

else:
	print "Couldn't process any images, quitting..."




