from djitellopy import Tello

tello = Tello()
if not tello.connect():
	print("Cannot reach tello, aborting!")
	exit(1)

tello.connect_to_wifi("Bunker", "E3JDWhLYJqY8fP7e")
