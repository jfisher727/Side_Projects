import numpy as np
import cv2

BOX_SIZE = 200
cap = cv2.VideoCapture(0)
initial_frame = 1

while(True):
    # Capture frame-by-frame
	ret, initial_frame = cap.read()
	resized = 1

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	height, width = initial_frame.shape[:2]
	left_bound= ((width / 2) - BOX_SIZE)
	right_bound = ((width / 2) + BOX_SIZE)
	bottom_bound = ((height / 2) + BOX_SIZE)
	top_bound = ((height / 2) - BOX_SIZE)
    #print ("Height: " + str(height) + " Width: " + str(width) + "Left: " + str(left_bound) + " Right: " + str(right_bound) + " Top: " + str(top_bound) + " Bottom: " + str(bottom_bound))
	cv2.rectangle(initial_frame,(left_bound,top_bound),(right_bound,bottom_bound),(0,255,0),3)
	resized = cv2.resize(initial_frame, (width / 2, height / 2))

	gray = cv2.cvtColor(initial_frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	frameDelta = cv2.absdiff(initial_frame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
 
	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue
 
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		#text = "Occupied"

    # Display the resulting frame
	cv2.imshow('frame',resized)
    #cv2.imshow('image',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()