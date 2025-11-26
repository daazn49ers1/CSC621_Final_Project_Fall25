import SimpleITK as sitk

# converts a path leading to a dicom file to an image
def convert_file(path):
	reader = sitk.ImageSeriesReader()

	reader.SetFileNames(reader.GetGDCMSeriesFileNames(path))

	return reader.execute()


def attempt_register(fixed, moving): 
	img_fixed = convert_file(fixed)
	img_moving = convert_file(moving)

	#apply demons
	#test #iterations


print("met")