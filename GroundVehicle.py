import math, threading, sys, random

from IllegalArgumentException import *

class GroundVehicle(threading.Thread):
	# static class members (call using: Class.<member>)
	totalNumVehicles = 0
	# A simple re-entrant lock suffices here because this
	# lock is only used for gated access to the resource
	gv_class_lock = threading.RLock()

	def __init__(self, pose, s, omega):
		threading.Thread.__init__(self)

		# check for legal arguments
		if len(pose) != 3:
			raise IllegalArgumentException("Incorrect size Pos array")

		# initiate Ground Vehicle
		self.__x = pose[0]
		self.__y = pose[1]
		self.__theta = self.normalizeAngle(pose[2])

		self.__s = s
		self.__omega = omega

		# intrinsic "self" lock
		self.gv_lock = threading.RLock()

		self.__sim = None

		self.__lastCheckedSec = 0
		self.__lastCheckedMSec = 0

		# synchronize incrementation on all GV objects
		GroundVehicle.gv_class_lock.acquire()
		self.__vehicleID = GroundVehicle.totalNumVehicles
		GroundVehicle.totalNumVehicles += 1
		GroundVehicle.gv_class_lock.release()

	def addSimulator(self, sim):
		self.__sim = sim

	def getVehicleID(self):
		return self.__vehicleID

	def getPosition(self):
		pos = []

		self.gv_lock.acquire() # start critical region
		pos = [self.__x, self.__y, self.__theta]
		self.gv_lock.release() # end critical region

		return pos

	def getVelocity(self):
		vel = []

		self.gv_lock.acquire() # start critical region
		dx = self.__s*math.cos(self.__theta)
		dy = self.__s*math.sin(self.__theta)
		vel = [dx, dy, self.__omega]
		self.gv_lock.release() # end critical region

		return vel

	def setPosition(self,pos):
		if len(pos) != 3:
			raise IllegalArgumentException("new Pos array must be of length 3")

		self.gv_lock.acquire() # start critical region
		self.__x = pos[0]
		self.__y = pos[1]
		self.__theta = self.normalizeAngle(pos[2])

		self.gv_lock.release() # end critical region


	def setVelocity(self, s, omega):

		self.gv_lock.acquire() # start critical region
		self.__s = s
		self.__omega = omega
		self.gv_lock.release() # end critical region

	def controlVehicle(self,c):
		if c == None:
			return

		lon, lat = c.getLoc()
		speed = c.getSpeed()
		theta = c.getTheta()

		self.gv_lock.acquire() # start critical region

		# set x and y
		self.__x = lon
		self.__y = lat

		# set theta
		self.__theta = self.normalizeAngle(theta)

		# set speed
		self.__s = speed

		self.gv_lock.release() # end critical region

	@staticmethod
	def normalizeAngle(theta):

		rtheta = math.fmod(theta - math.pi, 2*math.pi)
		if rtheta < 0:
			rtheta += 2*math.pi

		rtheta -= math.pi

		return rtheta

	def advance(self,sec,msec):
		t = sec + msec*1e-3

		self.gv_lock.acquire() # start critical region

		if math.fabs(self.__omega) <= 1e-7: #if angular velocity is effectively zero
			self.__x = self.__s*math.cos(self.__theta)*t + self.__x
			self.__y = self.__s*math.sin(self.__theta)*t + self.__y
		else: 
			self.__x = (self.__s/self.__omega)*(math.sin(self.__theta + self.__omega*t) - math.sin(self.__theta)) + self.__x
			self.__y = -(self.__s/self.__omega)*(math.cos(self.__theta + self.__omega*t) - math.cos(self.__theta)) + self.__y
			self.__theta = self.normalizeAngle(self.__omega*t + self.__theta)

		self.gv_lock.release() # end critical region

	def run(self):

		print "GV: %i thread started" % self.__vehicleID

		currentSec = 0
		currentMSec = 0

		while True:
			if not self.__sim.getDisplayClient().isConnected():
				break

			# end thread if this GroundVehicle is no longer in the Simulator
			if not self.__sim.inList(self):
				break 

			# Start Condition Critical Region
			self.__sim.simulator_lock.acquire()

			currentSec = self.__sim.getCurrentSec()
			currentMSec = self.__sim.getCurrentMSec()

			while 1:

				# check if time has changed since last update
				if not (self.__lastCheckedSec == currentSec and 
						self.__lastCheckedMSec == currentMSec):

					currentSec = self.__sim.getCurrentSec()
					currentMSec = self.__sim.getCurrentMSec()
					break # exit "while 1" loop once current time is updated

				# wait until Simulator notifies all threads that time has passed
				self.__sim.simulator_lock.wait() 
												 
				currentSec = self.__sim.getCurrentSec()
				currentMSec = self.__sim.getCurrentMSec()

			self.advance(0,10)

			# End Condition Critical Region
			self.__sim.simulator_lock.release()

			# update the time of the last control
			self.__lastCheckedSec = currentSec
			self.__lastCheckedMSec = currentMSec

			# start critical region
			self.__sim.simulator_lock.acquire()

			# decrement number of controllers left to update
			if self.__sim.numVehicleToUpdate > 0:
				self.__sim.numVehicleToUpdate -= 1
			self.__sim.simulator_lock.notify_all()

			# end critical region
			self.__sim.simulator_lock.release() 


