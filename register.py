import SimpleITK as sitk

#export SITK_SHOW_COMMAND=~/Downloads/fiji-latest-linux64-jdk/Fiji/fiji

# converts a path leading to a directory of dicom files
# to an image
def convert_file(path):
	reader = sitk.ImageSeriesReader()

	reader.SetFileNames(reader.GetGDCMSeriesFileNames(path))

	return reader.Execute()


def attempt_register(fixed, moving): 
	img_fixed = convert_file(fixed)
	img_moving = convert_file(moving)

	#print(img_fixed.GetPixelID()) # 4

	matcher = sitk.HistogramMatchingImageFilter()
	matcher.SetNumberOfHistogramLevels(1024)
	matcher.SetNumberOfMatchPoints(7)
	matcher.ThresholdAtMeanIntensityOn()

	img_moving = matcher.Execute(img_moving, img_fixed)
	
	#apply demons
	demons = sitk.FastSymmetricForcesDemonsRegistrationFilter()
	demons.SetNumberOfIterations(5)
	demons.SetStandardDeviations(1.0)

	#displacement_field = demons.Execute(img_fixed, img_moving)
	print("check")

patient1 = "/home/a/main/Dataset/Data/Patient1"
patient2 = "/home/a/main/Dataset/Data/Patient2"

#sitk.Show(convert_file(patient2))

attempt_register(patient1, patient2)
