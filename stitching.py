import cv2 as cv

images = []
m1 = cv.imread("capture1.jpg")
m2 = cv.imread("capture2.jpg")
m3 = cv.imread("capture3.jpg")
m4 = cv.imread("capture4.jpg")

images.append(m1)
images.append(m2)
images.append(m3)
images.append(m4)

#stitcher = cv.Stitcher_create()
stitcher = cv.Stitcher.create(cv.Stitcher_PANORAMA)
(status, stitched) = stitcher.stitch(images)

if status == 0:
	# write the output stitched image to disk
	#cv.imwrite(args["output"], stitched)
	# display the output stitched image to our screen
	cv.imshow("Stitched", stitched)
	cv.waitKey(0)
	cv.destroyAllWindows()
else: print("[INFO] image stitching failed ({})".format(status))
	

#cv.imshow("Stitching",m1)

