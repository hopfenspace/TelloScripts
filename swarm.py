import sys, time
from djitellopy import TelloSwarm

swarm = TelloSwarm.fromFile("ips.txt")

if len(swarm) != 4:
	print("This script was made to be run with four tellos!")
	exit(1)

swarm.connect()
swarm.set_speed(80)
swarm.takeoff()
swarm.move_up(100)

def workerFunc(i, tello):
	tello.move_left(150 - 50 * i)
	swarm.sync()
	tello.move_forward(i * 30)
	swarm.sync()

	if i == 0:
		swarm.sync()
		swarm.sync()
		tello.rotate_clockwise(90)
	elif i == 1:
		tello.move_back(150)
		swarm.sync()
		tello.move_left(50)
		swarm.sync()
	elif i == 2:
		tello.move_back(150)
		swarm.sync()
		tello.move_right(50)
		swarm.sync()
		tello.rotate_counter_clockwise(90)
	else: # i == 3
		swarm.sync()
		swarm.sync()
		tello.rotate_clockwise(180)

#swarm.parallel(workerFunc)

for i in range(0, 5):
	swarm.move_forward(150)
	swarm.rotate_clockwise(90)

time.sleep(1)
swarm.land()