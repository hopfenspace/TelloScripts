from djitellopy import Tello
import cv2, math, time

tello = Tello()
if not tello.connect():
	print("Cannot reach tello, aborting!")
	exit(1)

tello.streamoff()
tello.takeoff()
time.sleep(1)

tello.streamon()

cv2.namedWindow("drone")
frame_read = tello.get_frame_read()

while True:
	img = frame_read.frame
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
