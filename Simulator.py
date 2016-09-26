import math, sys, threading, time, random

from IllegalArgumentException import *
from APIreader import *
from VehicleController import *
from GroundVehicle import *
from DisplayClient import *

class Simulator(threading.Thread): 

	def __init__(self, displayClient=None):
		threading.Thread.__init__(self)

		self.__currentSec = 0
		self.__currentMSec = 0

		self._gvList = [] # 'protected' class member

		if displayClient is None:
			# print 'WARNING: No DisplayClient specified'
			pass
		self.__displayClient = displayClient
				
		# Non-Private class members
		self.numControlToUpdate = 0
		self.numVehicleToUpdate = 0

		# Public simulator lock
		self.simulator_lock = threading.Condition()

	#[PLACEHOLDER] check if necessary
	# UPDATE: used for quit condition loop
	def getDisplayClient(self):
		return self.__displayClient

	def getCurrentSec(self):
		self.simulator_lock.acquire() # start critical region
		cSec = self.__currentSec
		self.simulator_lock.release() # end critical region
		return cSec

	def getCurrentMSec(self):
		self.simulator_lock.acquire() # start critical region
		cMSec = self.__currentMSec
		self.simulator_lock.release() # end critical region
		return cMSec

	def advanceClock(self):

		self.simulator_lock.acquire() # start critical region
		self.__currentMSec += 10
		if (self.__currentMSec >= 1e3):
			self.__currentMSec -= 1e3
			self.__currentSec += 1
		self.simulator_lock.release() # end critical region

	def addGroundVehicle(self, gv):
		self.simulator_lock.acquire() # start critical region
		self._gvList.append(gv)
		print "---------Adding Ground Vehicle-----------\n"
		i = 1
		for gv in self._gvList:
			pos = gv.getPosition()
			print "%i : %f,%f,%f" %  (i,pos[0],pos[1],pos[2])
			i+=1
		print " "

		self.numControlToUpdate += 1
		self.numVehicleToUpdate += 1
		self.simulator_lock.release() # end critical region

	def removeGroundVehicle(self, gv):
		self.simulator_lock.acquire() # start critical region
		self._gvList.remove(gv)
		print "---------Remove Ground Vehicle-----------\n"
		i = 1
		for gv in self._gvList:
			pos = gv.getPosition()
			print "%i : %f,%f,%f" %  (i,pos[0],pos[1],pos[2])
			i+=1
		print " "

		self.numControlToUpdate -= 1
		self.numVehicleToUpdate -= 1
		self.simulator_lock.release() # end critical region

	def inList(self, gv):
		self.simulator_lock.acquire() # start critical region
		inlist = gv in self._gvList
		self.simulator_lock.release() # end critical region

		return inlist

	def run(self):

		lastUpdateSec = self.__currentSec
		lastUpdateMSec = self.__currentMSec

		if self.__displayClient:
			self.__displayClient.clear()
			self.__displayClient.traceOff()

		print "Simulator thread started"

		while True:
			#[NOT NECESSARY] Implemented for convenience of having the VC and 
			# Sim threads ends when quit is called on the DisplayServer
			if not self.__displayClient.isConnected():
				print 'SIM: display client NOT connected'
				break

			# if all groundvehicles have been removed, end simulation
			if self._gvList == []:
				break

			deltaSec = self.__currentSec - lastUpdateSec
			deltaMSec = self.__currentMSec - lastUpdateMSec

			if (deltaMSec < 0):
				deltaMSec += 1e3
				deltaSec -= 1

			gvX = []
			gvY = []
			gvTheta = []

			# populate data to be sent to display client 
			for currentGV in self._gvList:
				pos = currentGV.getPosition()
				gvX.append(pos[0])
				gvY.append(pos[1])
				gvTheta.append(pos[2])

			# send GV positions to the DisplayServer using the DisplayClient
			if self.__displayClient:
				self.__displayClient.update(len(self._gvList),gvX,gvY,gvTheta)

			# Start of Conditional Critical Region
			self.simulator_lock.acquire() 

			# update the clock
			lastUpdateSec = self.__currentSec
			lastUpdateMSec = self.__currentMSec

			# sleep ten milliseconds, then advance clock ten milliseconds
			# ( notice - this forces simulation time to run sort of in real-time )
			# ( in reality, simulation time runs slower than real time, because of computing time )
			time.sleep(0.01) 
			self.advanceClock()
			
			# Notify-All waiting VC threads
			self.simulator_lock.notify_all()

			# End of Conditinal Critical Region
			self.simulator_lock.release()

			# acquire lock to wait for all VCs to finish updating
			self.simulator_lock.acquire() # Start of Conditional Critical Region
			while 1:
				# check if all controllers and vehicles updated, otherwise wait
				if self.numControlToUpdate == 0 and self.numVehicleToUpdate == 0:
					break
				self.simulator_lock.wait()

			# reset numControlToUpdate and numVehicleToUpdate after waiting
			self.numControlToUpdate = len(self._gvList)
			self.numVehicleToUpdate = len(self._gvList)
			self.simulator_lock.release() # End of Conditinal Critical Region


			#[DEBUG] delay run speed of program to read print statements
			#time.sleep(1)

		if self.__displayClient:
			self.__displayClient.traceOff()
			self.__displayClient.clear()
		print 'Cleared\n'

# Simulator main method called when Simulator.py is executed directly
if __name__ == '__main__':

		host = socket.gethostbyname(socket.gethostname())
		dc = DisplayClient(host)
		sim = Simulator(dc)

		api = APIreader()

		trains = [] # list of currently active train ids
		api.APIupdate(api.APIget())

		traindictionary = api.getTrains()
		trains = traindictionary.keys()

		gvs = []
		vcs = []

		for tid in trains:
			initialPos = [traindictionary[tid][0], traindictionary[tid][1], traindictionary[tid][2]]
			initialspeed = 0
			omega = 0
			gv = GroundVehicle(initialPos, initialspeed, omega)

			vc = VehicleController(sim, gv, api, tid, traindictionary[tid][3])

			gv.addSimulator(sim)
			sim.addGroundVehicle(gv)

			gvs += [gv]
			vcs += [vc]

		api.start()

		for v in vcs:
			v.start()
		for g in gvs:
			g.start()

		sim.start()
		sim.join()
