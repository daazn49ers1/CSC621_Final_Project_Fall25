import os
import sys
import SimpleITK as sitk


def main(_):
	""" Generate a simple image and display it using the SimpleITK Show function. """
	# Create an image
	pixelType = sitk.sitkUInt8
	imageSize = [128, 128]
	image = sitk.Image(imageSize, pixelType)

	# Create a face image
	faceSize = [64, 64]
	faceCenter = [64, 64]
	face = sitk.GaussianSource(pixelType, imageSize, faceSize, faceCenter)

	# Create eye images
	eyeSize = [5, 5]
	eye1Center = [48, 48]
	eye2Center = [80, 48]
	eye1 = sitk.GaussianSource(pixelType, imageSize, eyeSize, eye1Center, 150)
	eye2 = sitk.GaussianSource(pixelType, imageSize, eyeSize, eye2Center, 150)

	# Apply the eyes to the face
	face = face - eye1 - eye2
	face = sitk.BinaryThreshold(face, 200, 255, 255)

	# Create the mouth
	mouthRadii = [30, 20]
	mouthCenter = [64, 76]
	mouth = 255 - sitk.BinaryThreshold(
		sitk.GaussianSource(pixelType, imageSize, mouthRadii, mouthCenter),
		200,
		255,
		255,
	)
	# Paste the mouth into the face
	mouthSize = [64, 18]
	mouthLoc = [32, 76]
	face = sitk.Paste(face, mouth, mouthSize, mouthLoc, mouthLoc)

	# Apply the face to the original image
	image = image + face
	print("in main function")
	return {"output_image": image}

print("in test.py")