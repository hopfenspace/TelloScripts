from djitellopy import Tello
import sys, time

if len(sys.argv) > 1:
	tello = Tello(sys.argv[1])
else:
	tello = Tello()

tello.connect()

speed = tello.query_speed()
snr = tello.query_wifi_signal_noise_ratio()
sdk = tello.query_sdk_version()
serial = tello.query_serial_number()

print("Speed = ", speed)
print("Battery = ", tello.get_battery())
print("Duration = ", tello.get_flight_time())
print("Height = ", tello.get_height())
print("Distance = ", tello.get_distance_tof())
print("Barometer = ", tello.get_barometer())
print("Attitude = ", tello.get_pitch(), tello.get_roll(), tello.get_yaw())
print("WiFi SNR = ", snr)
print("SDK Version = ", sdk)
print("Serial Number = ", serial)

print(tello.get_current_state())
