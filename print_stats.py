from djitellopy import Tello
import sys, time

tello = Tello(sys.argv[1])
if not tello.connect():
	print("Cannot reach tello, aborting!")
	exit(1)

speed = tello.get_speed()
battery = tello.get_battery()
duration = tello.get_flight_time()
height = tello.get_height()
distance = tello.get_distance_tof()
attitude = tello.get_attitude()
barometer = tello.get_barometer()
sdk = tello.get_sdk_version()
serial = tello.get_serial_number()

print("Speed = ", speed.strip())
print("Battery = ", battery.strip())
print("Duration = ", duration.strip())
print("Height = ", height.strip())
print("Distance = ", distance.strip())
print("Attitude = ", attitude.strip())
print("Barometer = ", barometer.strip())
print("SDK Version = ", sdk)
print("Serial Number = ", serial.strip())
