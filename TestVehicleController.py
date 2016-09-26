import unittest, math, time

from IllegalArgumentException import *
from APIreader import *
from VehicleController import *
from GroundVehicle import *
from Simulator import *
from Control import *

class TestVehicleController(unittest.TestCase):

	# Test constructor does not throw an error
	def testConstructor(self):
		sim = Simulator()
		pos = [0,0,0]
		gv = GroundVehicle(pos,1,math.pi)
		gv.addSimulator(sim)
		api = APIreader()
		trainid = 'testID'
		t = int(time.time())

		vc = VehicleController(sim, gv, api, trainid, t)

	# Test that getControl behaves as expected
	def testgetControl(self):
		sim = Simulator()
		pos = [0,0,0]
		gv = GroundVehicle(pos,1,math.pi)
		gv.addSimulator(sim)
		api = APIreader()
		trainid = 'testID'
		t = 12345

		vc = VehicleController(sim, gv, api, trainid, t)

		# time = '12345' - no change in time, should return None
		lon = 0
		lat = 0
		bearing = 90
		time = 12345
		c = vc.getControl(lon, lat, bearing, time)
		self.assertEqual(None, c)

		# increment time by one second but do not move vehicle
		# should maintain vehicle location and set speed to zero
		lon = 0
		lat = 0
		bearing = 90
		time = 12346
		c = vc.getControl(lon, lat, bearing, time)
		self.assertAlmostEqual(lon, c.getLoc()[0])
		self.assertAlmostEqual(lat, c.getLoc()[1])
		self.assertAlmostEqual(0, c.getSpeed())
		self.assertAlmostEqual(0, c.getTheta())

		# increment time by one second and move vehicle by one unit
		# should set to new position and extrapolate forward speed of 1 unit / second
		lon = 1
		lat = 0
		bearing = 90
		time = 12347
		c = vc.getControl(lon, lat, bearing, time)
		self.assertAlmostEqual(lon, c.getLoc()[0])
		self.assertAlmostEqual(lat, c.getLoc()[1])
		self.assertAlmostEqual(1, c.getSpeed())
		self.assertAlmostEqual(0, c.getTheta())


	# Tests if bearing angle is successfully converted to theta angle in [-pi, pi)
	def testNormalizeBearingAngle(self):
		# bearing = 0, theta = pi/2 (north)
		self.assertAlmostEqual(math.pi/2, VehicleController.normalizeBearingAngle(0))

		# bearing = 45, theta = pi/4 (northeast)
		self.assertAlmostEqual(math.pi/4, VehicleController.normalizeBearingAngle(45))

		# bearing = 90, theta = 0 (east)
		self.assertAlmostEqual(0, VehicleController.normalizeBearingAngle(90))

		# bearing = 135, theta = -pi/4 (southeast)
		self.assertAlmostEqual(-math.pi/4, VehicleController.normalizeBearingAngle(135))

		# bearing = 180, theta = -pi/2 (south)
		self.assertAlmostEqual(-math.pi/2, VehicleController.normalizeBearingAngle(180))

		# bearing = 225, theta = -3pi/4 (southwest)
		self.assertAlmostEqual(-0.75*math.pi, VehicleController.normalizeBearingAngle(225))

		# bearing = 270, theta = -pi (west)
		self.assertAlmostEqual(-math.pi, VehicleController.normalizeBearingAngle(270))

		# bearing = 315, theta = 3pi/4 (northwest)
		self.assertAlmostEqual(0.75*math.pi, VehicleController.normalizeBearingAngle(315))		

if __name__ == '__main__':
	unittest.main()
