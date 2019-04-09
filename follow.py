from djitellopy import Tello
import cv2, math, time

speed_factor = 400

face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')
tracker = None
startSize = 0
lastSuccessfullTrack = 0

clickPos = None
def onClick(event, x, y, flags, param):
	global clickPos
	if event == cv2.EVENT_LBUTTONDOWN:
		print(event, x,  y)
		clickPos = (x, y)

cv2.namedWindow("drone")
cv2.setMouseCallback("drone", onClick)


tello = Tello()
tello.connect()

tello.streamoff()
tello.takeoff()
tello.send_rc_control(0, 0, 0, 0)
time.sleep(3)

tello.streamon()

frame_read = tello.get_frame_read()


#vid = cv2.VideoCapture(0)
while True:
	img = frame_read.frame
	#ok, img = vid.read()

	if tracker:
		ok, bbox = tracker.update(img)
		if ok:
			x, y, w, h = bbox
			centerX = x + w / 2
			centerY = y + h / 2
			size = w * h
			width, height, channel = img.shape

			normDistance = (startSize - size) / (width * height)
			normHeight = (centerY - height / 2) / height
			normAngle = (centerX - width / 2) / width

			forwardSpeed = speed_factor * (normDistance * normDistance * normDistance)
			heightSpeed = speed_factor * (normHeight * normHeight * normHeight)
			rotationSpeed = speed_factor * (normAngle * normAngle * normAngle)

			if math.fabs(forwardSpeed) > 100:
				forwardSpeed = math.copysign(100, forwardSpeed)
			if math.fabs(heightSpeed) > 100:
				heightSpeed = math.copysign(100, heightSpeed)
			if math.fabs(rotationSpeed) > 100:
				rotationSpeed = math.copysign(100, rotationSpeed)

			tello.send_rc_control(0, int(forwardSpeed), int(heightSpeed), int(rotationSpeed))

			x, y, w, h = int(x), int(y), int(w), int(h)
			cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
		else:
			tello.send_rc_control(0, 0, 0, 0)
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
		tello.land()
		frame_read.stop()
		exit(0)

	if clickPos:
		clickX, clickY = clickPos
		for (x, y, w, h) in faces:
			print(clickX, clickY, x, y, w, h)
			if clickX >= x and clickX <= x + w and clickY >= y and clickY <= y + h:
				tracker = cv2.TrackerMedianFlow_create()
				if tracker.init(img, (x, y, w, h)):
					startSize = w * h
					print("Starting to track object!")
				else:
					print("Failed initializing the tracker!")
					tracker = None

		clickPos = None
