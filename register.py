import SimpleITK as sitk

# converts a path leading to a dicom file to an image
def convert_file(path):
	reader = sitk.ImageSeriesReader()

	reader.SetFileNames(reader.GetGDCMSeriesFileNames(path))

	return reader.execute()


def attempt_register(fixed, moving): 
	
