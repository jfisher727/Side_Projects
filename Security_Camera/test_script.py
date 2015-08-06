import cv2

def diffImage (t0, t1, t2):
	d1 = cv2.absdiff(t2, t1)
	d2 = cv2.absdiff(t1, t0)
	return cv2.bitwise_and(d1, d2)

camera = cv2.VideoCapture(0)

window_name = "Tester"
cv2.namedWindow (window_name, cv2.CV_WINDOW_AUTOSIZE)

t_minus = cv2.cvtColor(camera.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(camera.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(camera.read()[1], cv2.COLOR_RGB2GRAY)

while True:
	#cv2.imshow (window_name, image)
	cv2.imshow (window_name, diffImage(t_minus, t, t_plus))
	#s, image = camera.read()

	t_minus = t
	t = t_plus
	t_plus = cv2.cvtColor(camera.read()[1], cv2.COLOR_RGB2GRAY)

	key = cv2.waitKey(10)
	if key == 27:
		cv2.destroyWindow (window_name)
		break
print ("Close")