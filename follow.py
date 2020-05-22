from djitellopy import Tello
import cv2, math, time

face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')
currentFace = None
seenCount = 0

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
tello.streamon()
frame_read = tello.get_frame_read()

tello.takeoff()
tello.send_rc_control(0, 0, 0, 0)

def getCenter(rect):
	x, y, w, h = rect
	return (x + w / 2, y + h / 2)
def distance(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	dx = x2 - x1
	dy = y2 - y1
	return math.sqrt(dx * dx + dy * dy)
def rectDistance(rect1, rect2):
	p1 = getCenter(rect1)
	p2 = getCenter(rect2)
	return distance(p1, p2)

#vid = cv2.VideoCapture(0)
while True:
	img = frame_read.frame
	#ok, img = vid.read()

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	for face in faces:
		if face is currentFace:
			continue
		x, y, w, h = face
		cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

	foundFace = False
	if len(faces) > 0:
		newFace = max(faces, key=lambda rect: rect[2] * rect[3])
		if currentFace is None:
			currentFace = newFace
			seenCount = 0

		if rectDistance(newFace, currentFace) < 3000:
			currentFace = newFace
			seenCount += 1
			foundFace = True
	
	if not foundFace:
		if seenCount <= 0:
			currentFace = None
		elif seenCount < 10:
			seenCount -= 1
		else:
			seenCount = 9

	if currentFace is not None and seenCount > 10:
		x, y, w, h = currentFace
		centerX, centerY = getCenter(currentFace)
		size = w * h
		width, height, channel = img.shape
		halfWidth = width / 2
		halfHeight = height / 2

		def calcSpeed(norm, steps):
			absNorm = math.fabs(norm)
			for step, speed in steps:
				if absNorm > step:
					return math.copysign(speed, norm)

			return 0

		forwardSpeed = 0 # TODO # calcSpeed((startSize - size) / startSize)
		heightSpeed = calcSpeed(-1 * (centerY - halfHeight) / halfHeight, [(0.3, 50), (0.1, 30), (0.01, 5)])
		rotationSpeed = calcSpeed((centerX - halfWidth) / halfWidth, [(0.7, 50), (0.5, 30), (0.3, 30), (0.1, 5)])

		tello.send_rc_control(0, int(forwardSpeed), int(heightSpeed), int(rotationSpeed))
		cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
	else:
		tello.send_rc_control(0, 0, 0, 0)

	cv2.putText(img, str(tello.get_battery()) + "%", (5, 15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0))
	cv2.imshow("drone", img)

	key = cv2.waitKey(1) & 0xff
	if key == ord('q'):
		tello.end()
		exit(0)
	elif key == ord('w'):
		tello.move_up(30)
	elif key == ord('s'):
		tello.move_down(30)
	elif key == ord('a'):
		tello.rotate_counter_clockwise(20)
	elif key == ord('d'):
		tello.rotate_clockwise(20)
