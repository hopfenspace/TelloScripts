import time
from TelloSwarm import TelloSwarm

swarm = TelloSwarm.fromFile("ips.txt")
#swarm.takeoff()
swarm.land()