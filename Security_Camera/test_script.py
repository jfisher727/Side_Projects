import cv2
import sys

def diffImage (t0, t1, t2):
	d1 = cv2.absdiff(t2, t1)
	d2 = cv2.absdiff(t1, t0)
	return cv2.bitwise_and(d1, d2)

camera = cv2.VideoCapture(0)

window_name = "Tester"
cv2.namedWindow (window_name, cv2.WINDOW_AUTOSIZE)

t_minus = cv2.cvtColor(camera.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(camera.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(camera.read()[1], cv2.COLOR_RGB2GRAY)

while True:
	#cv2.imshow (window_name, image)
	diff_image = diffImage(t_minus, t, t_plus)
	cv2.imshow (window_name, diff_image)
	#s, image = camera.read()

	t_minus = t
	t = t_plus
	t_plus = cv2.cvtColor(camera.read()[1], cv2.COLOR_RGB2GRAY)

	sys.stdout.write ( diff_image.toString() )

	key = cv2.waitKey(10)
	if key == 27:
		cv2.destroyWindow (window_name)
		break
print ("Close")