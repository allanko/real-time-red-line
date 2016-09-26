import math

from IllegalArgumentException import *

class Control:
	
	def __init__(self, lon, lat, s, theta):
		# Check to make sure theta in range
		if (theta<-math.pi or theta>=math.pi):
			raise IllegalArgumentException("theta out of range")

		self.__lon = lon
		self.__lat = lat
		self.__s = s
		self.__theta = theta

	def getLoc(self):
		return self.__lon, self.__lat

	def getSpeed(self):
		return self.__s

	def getTheta(self):
		return self.__theta

