# bspline took too long
# mutual info max based from sitk img reg 4

import SimpleITK as sitk

#export SITK_SHOW_COMMAND=~/Downloads/fiji-latest-linux64-jdk/Fiji/fiji

# converts a path leading to a directory of dicom files
# to an image
def convert_file(path, pixel_type=None):
	reader = sitk.ImageSeriesReader()

	reader.SetFileNames(reader.GetGDCMSeriesFileNames(path))

	if pixel_type:
		reader.SetOutputPixelType(pixel_type)

	return reader.Execute()

def on_iteration(self):
	print(f"{self.GetOptimizerIteration():3}" + f"={self.GetMetricValue():10.5f}")

# Attempt to use different registering algorithm
def attempt_register(fixed, moving):
	img_fixed = convert_file(fixed, sitk.sitkFloat32)
	img_moving = convert_file(moving, sitk.sitkFloat32)

	#print("met: init params: ", tx.GetParameters())

	register_method = sitk.ImageRegistrationMethod()
	register_method.SetMetricAsMattesMutualInformation(24)
	register_method.SetMetricSamplingPercentage(.1, sitk.sitkWallClock)
	# subject to change
	register_method.SetMetricSamplingStrategy(register_method.RANDOM)
	register_method.SetOptimizerAsRegularStepGradientDescent(1.0, 0.001, 200)
	register_method.SetInitialTransform(sitk.TranslationTransform(img_fixed.GetDimension()))
	register_method.SetInterpolator(sitk.sitkLinear)

	#register_method.AddCommand(sitk.sitkIterationEvent, lambda: on_iteration(register_method))

	out_tx = register_method.Execute(img_fixed, img_moving)

	resample = sitk.ResampleImageFilter()
	resample.SetReferenceImage(img_fixed)
	resample.SetInterpolator(sitk.sitkLinear)
	resample.SetDefaultPixelValue(100)
	resample.SetTransform(out_tx)

	resampled = resample.Execute(img_moving)

	cast1 = sitk.Cast(sitk.RescaleIntensity(img_fixed), sitk.sitkUInt8)
	cast2 = sitk.Cast(sitk.RescaleIntensity(resampled), sitk.sitkUInt8)
	composed = sitk.Compose(cast1, cast2, cast1 // 2.0 + cast2 // 2.0)


	return composed



patient1 = "/home/a/main/Dataset/Data/Patient1"
patient2 = "/home/a/main/Dataset/Data/Patient2"

#sitk.Show(convert_file(patient2))

img = attempt_register(patient1, patient2)

sitk.Show(img)

