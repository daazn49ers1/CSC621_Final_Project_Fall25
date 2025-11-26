import SimpleITK as sitk

# converts a path leading to a directory of dicom files
# to an image
def convert_file(path):
	reader = sitk.ImageSeriesReader()

	reader.SetFileNames(reader.GetGDCMSeriesFileNames(path))

	return reader.Execute()


def attempt_register(fixed, moving): 
	img_fixed = convert_file(fixed)
	img_moving = convert_file(moving)

	#apply demons
	#test #iterations


patient1 = "/home/a/main/Dataset/Data/Patient1"
patient2 = "/home/a/main/Dataset/Data/Patient2"

sitk.Show(convert_file(patient1))
sitk.Show(convert_file(patient2))
