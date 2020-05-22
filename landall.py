import time
from djitellopy import TelloSwarm

swarm = TelloSwarm.fromFile("ips.txt")
#swarm.takeoff()
swarm.land()