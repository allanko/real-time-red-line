import unittest

from IllegalArgumentException import *
from Control import *
from math import *

class TestControl(unittest.TestCase):

	#test illegal values for theta
	def testLowTheta(self):
		with self.assertRaises(IllegalArgumentException):
			c = Control(-71.03, 42.3, 5,-10)

	def testHighTheta(self):
		with self.assertRaises(IllegalArgumentException):
			c = Control(-71.03, 42.3, 5, 10)

	#test edge cases for theta
	def testThetaMinusPi(self):
		c = Control(-71.03, 42.3, 5, -math.pi)
		self.assertAlmostEqual(-math.pi, c.getTheta())

	def testThetaPi(self):
		with self.assertRaises(IllegalArgumentException):
			c = Control(-71.03, 42.3, 5, math.pi)

	# test legal arguments
	def testCorrectOutputs(self):
		# values which should not throw errors
		test_lon = -71.03
		test_lat = 42.50
		test_s = 7.5
		test_theta = .2

		test_c = Control(test_lon, test_lat, test_s, test_theta)
		
		self.assertEqual((test_lon, test_lat), test_c.getLoc())
		self.assertEqual(test_s, test_c.getSpeed())
		self.assertEqual(test_theta, test_c.getTheta())


# main method which executes unit tests when TestControl.py is run directly
if __name__ == "__main__":
	unittest.main()


