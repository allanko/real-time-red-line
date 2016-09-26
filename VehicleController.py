import math, threading, random, time

from IllegalArgumentException import *
from APIreader import *
from GroundVehicle import *
from Simulator import *
from Control import *

class VehicleController(threading.Thread):

	def __init__(self, sim, gv, api, trainid, time):
		threading.Thread.__init__(self)

		self.__sim = sim
		self.__gv = gv
		self.__api = api 
		self.__id = trainid 

		self.__timelastsynced = time

	def getControl(self, lon, lat, bearing, time):
		if time == self.__timelastsynced:
			return None
		else:
			x, y, theta = self.__gv.getPosition()

			#if time has passed but vehicle has not moved, set speed to 0
			if math.fabs(x - lon) <= 1e-8 and math.fabs(y - lat) <= 1e-8:
				print 'stationary!'
				c = Control(lon, lat, 0, self.normalizeBearingAngle(bearing))
			else:
				s = math.sqrt((x - lon)**2 + (y - lat)**2) / (time - self.__timelastsynced)
				print 'extrapolated speed: ', s
				c = Control(lon, lat, s, self.normalizeBearingAngle(bearing))

			#update timelastsynced
			self.__timelastsynced = time
			return c

	@staticmethod 
	def normalizeBearingAngle(bearing):
		#converts a bearing (in degrees clockwise from north) 
		#to proper theta coordinates (radians counterclockwise from east)
		theta = math.pi*(90 - bearing) / 180

		# clamp theta to [-pi, pi)
		rtheta = math.fmod(theta - math.pi, 2*math.pi)
		if rtheta < 0:
			rtheta += 2*math.pi

		rtheta -= math.pi

		return rtheta

	def run(self):

		print "VC controlling GV: %i thread started" % self.__gv.getVehicleID()

		while True:
			
			#[NOT NECESSARY] Implemented for convenience of having the VC and 
			# Sim threads ends when quit is called on the DisplayServer
			if not self.__sim.getDisplayClient().isConnected():
				print 'VC: display client NOT connected'
				break

			trains = self.__api.getTrains()

			if self.__id in trains.keys():
				# get train data = [lon, lat, bearing, time]
				traindata = trains[self.__id]

				# generate a new control 
				nextControl = self.getControl(traindata[0], traindata[1], traindata[2], traindata[3])

				# send control to vehicle
				self.__gv.controlVehicle(nextControl)


				# start critical region
				self.__sim.simulator_lock.acquire()
				
				# decrement number of controllers left to update
				if self.__sim.numControlToUpdate > 0:
					self.__sim.numControlToUpdate -= 1
				
				self.__sim.simulator_lock.notify_all()
				
				# end critical region
				self.__sim.simulator_lock.release() 

				# remove GroundVehicles and break if APIreader has stopped running
				if not self.__api.isAlive():
					self.__sim.simulator_lock.acquire()
					self.__sim.removeGroundVehicle(self.__gv)
					self.__sim.simulator_lock.release()
					break 

			else: # if this train id is no longer in trains.keys, remove GroundVehicle from Simulator, break loop and end the thread
				self.__sim.simulator_lock.acquire()
				self.__sim.removeGroundVehicle(self.__gv)
				self.__sim.simulator_lock.release()

				break