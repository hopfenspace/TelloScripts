from djitellopy import Tello
import cv2

face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')
tracker = None
lastSuccessfullTrack = 0

clickPos = None
def onClick(event, x, y, flags, param):
	global clickPos
	if event == cv2.EVENT_LBUTTONDOWN:
		print(event, x,  y)
		clickPos = (x, y)

cv2.namedWindow("drone")
cv2.setMouseCallback("drone", onClick)


'''tello = Tello()
frame_read = tello.get_frame_read()

tello.connect()
tello.takeoff()'''


vid = cv2.VideoCapture(0)
oldFrame = None
img = None
while True:
	#while img is oldFrame:
	#	img = frame_read.frame
	ok, img = vid.read()

	if tracker:
		ok, bbox = tracker.update(img)
		if ok:
			x, y, w, h = bbox
			x, y, w, h = int(x), int(y), int(w), int(h)
			cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
		else:
			lastSuccessfullTrack = lastSuccessfullTrack + 1
			if lastSuccessfullTrack > 60:
				print("Tracker did not find anything for 60 frames, aborting...")
				tracker = None

		

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	for (x, y, w, h) in faces:
		cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

	cv2.imshow("drone", img)

	key = cv2.waitKey(1) & 0xff
	if key == ord('q'):
		#tello.land()
		exit(0)

	if clickPos:
		clickX, clickY = clickPos
		for (x, y, w, h) in faces:
			print(clickX, clickY, x, y, w, h)
			if clickX >= x and clickX <= x + w and clickY >= y and clickY <= y + h:
				tracker = cv2.TrackerMedianFlow_create()
				if tracker.init(img, (x, y, w, h)):
					print("Starting to track object!")
				else:
					print("Failed initializing the tracker!")
					tracker = None

		clickPos = None
