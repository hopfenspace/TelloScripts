from djitellopy import Tello
import cv2, math, time

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
if not tello.connect():
	print("Cannot reach tello, aborting!")
	exit(1)

tello.streamoff()
tello.takeoff()
tello.send_rc_control(0, 0, 0, 0)
time.sleep(1)

tello.streamon()

frame_read = tello.get_frame_read()

statsRefresh = 0

#vid = cv2.VideoCapture(0)
while True:
	img = frame_read.frame
	#ok, img = vid.read()

	if tracker:
		ok, bbox = tracker.update(img)
		if ok:
			lastSuccessfullTrack = 0

			x, y, w, h = bbox
			centerX = x + w / 2
			centerY = y + h / 2
			size = w * h
			width, height, channel = img.shape
			halfWidth = width / 2
			halfHeight = height / 4

			def calcSpeed(norm, steps):
				absNorm = math.fabs(norm)
				for step, speed in steps:
					if absNorm > step:
						return math.copysign(speed, norm)

				return 0

			forwardSpeed = 0 # TODO # calcSpeed((startSize - size) / startSize)
			heightSpeed = calcSpeed(-1 * (centerY - halfHeight) / halfHeight, [(0.6, 100), (0.3, 50), (0.1, 20)])
			rotationSpeed = calcSpeed((centerX - halfWidth) / halfWidth, [(0.7, 100), (0.5, 50), (0.3, 30), (0.1, 10)])

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

	statsRefresh = statsRefresh - 1
	if statsRefresh <= 0:
		droneBattery = str(tello.get_battery()).strip()
		statsRefresh = 120
	cv2.putText(img, droneBattery + "%", (5, 15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0))

	cv2.imshow("drone", img)

	key = cv2.waitKey(1) & 0xff
	if key == ord('q'):
		tello.land()
		frame_read.stop()
		tello.streamoff()
		exit(0)
	elif key == ord('w'):
		tello.move_up(30)
	elif key == ord('s'):
		tello.move_down(30)
	elif key == ord('a'):
		tello.rotate_counter_clockwise(20)
	elif key == ord('d'):
		tello.rotate_clockwise(20)

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
