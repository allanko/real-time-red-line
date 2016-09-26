import unittest, math

from IllegalArgumentException import *
from GroundVehicle import *
from Simulator import *
from Control import *

class TestGoundVehicle(unittest.TestCase):

	# Contructs valid GV to ensure that no exceptions are thrown;
	# also confirms that the GV arguments are properly set
	def testConstructor(self):
		pose = [1,2,0]
		s = 5
		dt = 0
		gv = GroundVehicle(pose, s, dt)
		sim = Simulator()
		gv.addSimulator(sim)

		newPose = gv.getPosition()
		self.assertAlmostEqual(pose[0], newPose[0])
		self.assertAlmostEqual(pose[1], newPose[1])
		self.assertAlmostEqual(pose[2], newPose[2])

		dx = s*math.cos(0)
		dy = s*math.sin(0)

		newVel = gv.getVelocity()
		self.assertAlmostEqual(dx, newVel[0])
		self.assertAlmostEqual(dy, newVel[1])
		self.assertAlmostEqual(dt, newVel[2])

	def testTooManyArgumentsConstructor(self):
		with self.assertRaises(IllegalArgumentException):
			pose = [0,0,0,0]
			gv = GroundVehicle(pose, 0, 0)

	def testTooFewArgumentsConstructor(self):
		with self.assertRaises(IllegalArgumentException):
			pose = [0,0]
			gv = GroundVehicle(pose, 0, 0)

	def testNonArrayPoseArgument(self):
		with self.assertRaises(IllegalArgumentException):
			pose = 'not an array'
			gv = GroundVehicle(pose, 0, 0)

	def testTooManyArgumentsSetPosition(self):
		with self.assertRaises(IllegalArgumentException):
			gv = GroundVehicle([0,0,0], 5, 0)
			gv.setPosition([0,0,0,0])

	def testTooFewArgumentsSetPosition(self):
		with self.assertRaises(IllegalArgumentException):
			gv = GroundVehicle([0,0,0], 5, 0)
			gv.setPosition([0,0])

	# set positions to legal values (all x and y positions are legal)
	def testSetPosValid(self):
		pose = [1,2,0]
		s = 5
		omega = 0
		gv = GroundVehicle(pose, s, omega)

		#zero positions, zero theta
		plegal = [0, 0, 0]
		gv.setPosition(plegal)
		poseset = gv.getPosition()
		self.assertEqual(plegal[0], poseset[0])
		self.assertEqual(plegal[1], poseset[1])
		self.assertEqual(plegal[2], poseset[2])

		#positive positions, zero theta
		plegal = [50.4, 30.4, 0]
		gv.setPosition(plegal)
		poseset = gv.getPosition()
		self.assertEqual(plegal[0], poseset[0])
		self.assertEqual(plegal[1], poseset[1])
		self.assertEqual(plegal[2], poseset[2])

		#negative positions, zero theta
		plegal = [-76.45, -43.81, 0]
		gv.setPosition(plegal)
		poseset = gv.getPosition()
		self.assertEqual(plegal[0], poseset[0])
		self.assertEqual(plegal[1], poseset[1])
		self.assertEqual(plegal[2], poseset[2])

	# set theta to critical values (theta should be clamped to [-pi, pi))
	def testSetTheta(self):
		pose = [1,2,0]
		s = 5
		omega = 0
		gv = GroundVehicle(pose, s, omega)

		#theta < -pi: use theta = -2.5pi -- should clamp to -pi/2
		pnew = [0, 0, -2.5*math.pi]
		gv.setPosition(pnew)
		poseset = gv.getPosition()
		self.assertEqual(pnew[0], poseset[0])
		self.assertEqual(pnew[1], poseset[1])
		self.assertAlmostEqual(-0.5*math.pi, poseset[2])

		#theta = -pi: should clamp to -pi
		pnew = [0, 0, -math.pi]
		gv.setPosition(pnew)
		poseset = gv.getPosition()
		self.assertEqual(pnew[0], poseset[0])
		self.assertEqual(pnew[1], poseset[1])
		self.assertAlmostEqual(pnew[2], poseset[2])

		# -pi < theta < 0: should stay the same
		pnew = [0, 0, -math.pi/3]
		gv.setPosition(pnew)
		poseset = gv.getPosition()
		self.assertEqual(pnew[0], poseset[0])
		self.assertEqual(pnew[1], poseset[1])
		self.assertAlmostEqual(pnew[2], poseset[2])

		#theta = 0 - was tested in above testSetPosValid()

		# 0 < theta < pi: should stay the same
		pnew = [0, 0, 0.9*math.pi]
		gv.setPosition(pnew)
		poseset = gv.getPosition()
		self.assertEqual(pnew[0], poseset[0])
		self.assertEqual(pnew[1], poseset[1])
		self.assertAlmostEqual(pnew[2], poseset[2])

		# theta = pi: should clamp to theta = -pi
		pnew = [0, 0, math.pi]
		gv.setPosition(pnew)
		poseset = gv.getPosition()
		self.assertEqual(pnew[0], poseset[0])
		self.assertEqual(pnew[1], poseset[1])
		self.assertAlmostEqual(-math.pi, poseset[2])

		# theta > pi: using theta = 3.7pi, should clamp to -0.3pi
		pnew = [0, 0, 3.7*math.pi]
		gv.setPosition(pnew)
		poseset = gv.getPosition()
		self.assertEqual(pnew[0], poseset[0])
		self.assertEqual(pnew[1], poseset[1])
		self.assertAlmostEqual(-0.3*math.pi, poseset[2])

	def testSetVelValid(self):
		# all velocities are valid -- test a couple values just to make sure everything works
		theta = math.pi/2
		pose = [1,2, theta]
		s = 5
		omega = 0
		gv = GroundVehicle(pose, s, omega)

		#s, omega both zero
		news = 0
		newomega = 0
		gv.setVelocity(news, newomega)
		velset = gv.getVelocity()
		self.assertAlmostEqual(news*math.cos(theta), velset[0])
		self.assertAlmostEqual(news*math.sin(theta), velset[1])
		self.assertAlmostEqual(newomega, velset[2])

		#s positive, omega zero
		news = 8.6
		newomega = 0
		gv.setVelocity(news, newomega)
		velset = gv.getVelocity()
		self.assertAlmostEqual(news*math.cos(theta), velset[0])
		self.assertAlmostEqual(news*math.sin(theta), velset[1])
		self.assertAlmostEqual(newomega, velset[2])

		#s negative, omega zero
		news = -42.6
		newomega = 0
		gv.setVelocity(news, newomega)
		velset = gv.getVelocity()
		self.assertAlmostEqual(news*math.cos(theta), velset[0])
		self.assertAlmostEqual(news*math.sin(theta), velset[1])
		self.assertAlmostEqual(newomega, velset[2])

		#s zero, omega negative
		news = 0
		newomega = -3.24*math.pi
		gv.setVelocity(news, newomega)
		velset = gv.getVelocity()
		self.assertAlmostEqual(news*math.cos(theta), velset[0])
		self.assertAlmostEqual(news*math.sin(theta), velset[1])
		self.assertAlmostEqual(newomega, velset[2])

		#s zero, omega positive
		news = 0
		newomega = 5.11*math.pi
		gv.setVelocity(news, newomega)
		velset = gv.getVelocity()
		self.assertAlmostEqual(news*math.cos(theta), velset[0])
		self.assertAlmostEqual(news*math.sin(theta), velset[1])
		self.assertAlmostEqual(newomega, velset[2])

	def testControlVehicle(self):
		pose = [0,0,0]
		s = 5
		dt = 0
		gv = GroundVehicle(pose, s, dt)

		#longitude, latitude, speed, and theta all = 0
		lon = 0
		lat = 0
		s = 0
		t = 0
		c = Control(lon, lat, s, t)
		gv.controlVehicle(c)

		newpos = gv.getPosition()
		self.assertAlmostEqual(lon, newpos[0])
		self.assertAlmostEqual(lat, newpos[1])
		self.assertAlmostEqual(t, newpos[2])

		newvel = gv.getVelocity()
		self.assertAlmostEqual(s*math.cos(t), newvel[0])
		self.assertAlmostEqual(s*math.sin(t), newvel[1])

		#longitude, latitude, speed all positive, theta = 0
		lon = 35.5
		lat = 82.3
		s = 4.2
		t = 0
		c = Control(lon, lat, s, t)
		gv.controlVehicle(c)

		newpos = gv.getPosition()
		self.assertAlmostEqual(lon, newpos[0])
		self.assertAlmostEqual(lat, newpos[1])
		self.assertAlmostEqual(t, newpos[2])

		newvel = gv.getVelocity()
		self.assertAlmostEqual(s*math.cos(t), newvel[0])
		self.assertAlmostEqual(s*math.sin(t), newvel[1])

		#longitude, latitude, speed all negative, theta = 0
		lon = -15.72
		lat = -92.3
		s = -80.1
		t = 0
		c = Control(lon, lat, s, t)
		gv.controlVehicle(c)

		newpos = gv.getPosition()
		self.assertAlmostEqual(lon, newpos[0])
		self.assertAlmostEqual(lat, newpos[1])
		self.assertAlmostEqual(t, newpos[2])

		newvel = gv.getVelocity()
		self.assertAlmostEqual(s*math.cos(t), newvel[0])
		self.assertAlmostEqual(s*math.sin(t), newvel[1])

		#theta = -pi
		lon = 35.5
		lat = 82.3
		s = 4.2
		t = -math.pi
		c = Control(lon, lat, s, t)
		gv.controlVehicle(c)

		newpos = gv.getPosition()
		self.assertAlmostEqual(lon, newpos[0])
		self.assertAlmostEqual(lat, newpos[1])
		self.assertAlmostEqual(t, newpos[2])

		newvel = gv.getVelocity()
		self.assertAlmostEqual(s*math.cos(t), newvel[0])
		self.assertAlmostEqual(s*math.sin(t), newvel[1])

		#-pi < theta < 0
		lon = -15.72
		lat = -92.3
		s = -80.1
		t = -math.pi/3
		c = Control(lon, lat, s, t)
		gv.controlVehicle(c)

		newpos = gv.getPosition()
		self.assertAlmostEqual(lon, newpos[0])
		self.assertAlmostEqual(lat, newpos[1])
		self.assertAlmostEqual(t, newpos[2])

		newvel = gv.getVelocity()
		self.assertAlmostEqual(s*math.cos(t), newvel[0])
		self.assertAlmostEqual(s*math.sin(t), newvel[1])

		#theta = 0
		lon = -15.72
		lat = -92.3
		s = -80.1
		t = 0
		c = Control(lon, lat, s, t)
		gv.controlVehicle(c)

		newpos = gv.getPosition()
		self.assertAlmostEqual(lon, newpos[0])
		self.assertAlmostEqual(lat, newpos[1])
		self.assertAlmostEqual(t, newpos[2])

		newvel = gv.getVelocity()
		self.assertAlmostEqual(s*math.cos(t), newvel[0])
		self.assertAlmostEqual(s*math.sin(t), newvel[1])

		#0 < theta < pi
		lon = -15.72
		lat = -92.3
		s = -80.1
		t = math.pi/7
		c = Control(lon, lat, s, t)
		gv.controlVehicle(c)

		newpos = gv.getPosition()
		self.assertAlmostEqual(lon, newpos[0])
		self.assertAlmostEqual(lat, newpos[1])
		self.assertAlmostEqual(t, newpos[2])

		newvel = gv.getVelocity()
		self.assertAlmostEqual(s*math.cos(t), newvel[0])
		self.assertAlmostEqual(s*math.sin(t), newvel[1])

	def testNoneControlVehicle(self):
		#if controlVehicle is passed None, GroundVehicle should do nothing
		t = math.pi/2
		pose = [42.5,-71.4, t]
		s = 5.8
		dt = -20
		gv = GroundVehicle(pose, s, dt)

		gv.controlVehicle(None)

		newpos = gv.getPosition()
		self.assertAlmostEqual(pose[0], newpos[0])
		self.assertAlmostEqual(pose[1], newpos[1])
		self.assertAlmostEqual(pose[2], newpos[2])

		newvel = gv.getVelocity()
		self.assertAlmostEqual(s*math.cos(t), newvel[0])
		self.assertAlmostEqual(s*math.sin(t), newvel[1])
		self.assertAlmostEqual(dt, newvel[2])

	def testAdvance(self):
		# forward motion in the x-direction
		t = 0
		pose = [1, 1, t]
		s = 5
		dt = 0
		gv = GroundVehicle(pose, s, dt)

		gv.advance(1,0)
		newpos = gv.getPosition()
		self.assertAlmostEqual(6, newpos[0])
		self.assertAlmostEqual(1, newpos[1])
		self.assertAlmostEqual(0, newpos[2])

		# backward motion in the x-direction
		t = 0
		pose = [1, 1, t]
		s = -5
		dt = 0
		gv = GroundVehicle(pose, s, dt)

		gv.advance(1,0)
		newpos = gv.getPosition()
		self.assertAlmostEqual(-4, newpos[0])
		self.assertAlmostEqual(1, newpos[1])
		self.assertAlmostEqual(0, newpos[2])

		# forward motion in the y-direction
		t = math.pi/2
		pose = [1, 1, t]
		s = 5
		dt = 0
		gv = GroundVehicle(pose, s, dt)

		gv.advance(1,0)
		newpos = gv.getPosition()
		self.assertAlmostEqual(1, newpos[0])
		self.assertAlmostEqual(6, newpos[1])
		self.assertAlmostEqual(math.pi/2, newpos[2])

		# backward motion in the y-direction
		t = math.pi/2
		pose = [1, 1, t]
		s = -5
		dt = 0
		gv = GroundVehicle(pose, s, dt)

		gv.advance(1,0)
		newpos = gv.getPosition()
		self.assertAlmostEqual(1, newpos[0])
		self.assertAlmostEqual(-4, newpos[1])
		self.assertAlmostEqual(math.pi/2, newpos[2])

		# forward motion in the pi/4 direction
		t = math.pi/4
		pose = [1, 1, t]
		s = 5
		dt = 0
		gv = GroundVehicle(pose, s, dt)

		gv.advance(1,0)
		newpos = gv.getPosition()
		self.assertAlmostEqual(1 + 5/math.sqrt(2), newpos[0])
		self.assertAlmostEqual(1 + 5/math.sqrt(2), newpos[1])
		self.assertAlmostEqual(math.pi/4, newpos[2])

		# backward motion in the pi/4 direction
		t = math.pi/4
		pose = [1, 1, t]
		s = -5
		dt = 0
		gv = GroundVehicle(pose, s, dt)

		gv.advance(1,0)
		newpos = gv.getPosition()
		self.assertAlmostEqual(1 - 5/math.sqrt(2), newpos[0])
		self.assertAlmostEqual(1 - 5/math.sqrt(2), newpos[1])
		self.assertAlmostEqual(math.pi/4, newpos[2])		

		# counterclockwise circular rotation in place
		t = 0
		pose = [0, 0, t]
		s = 0
		dt = math.pi/8
		gv = GroundVehicle(pose, s, dt)

		gv.advance(1,0)
		newpos = gv.getPosition()
		self.assertAlmostEqual(0, newpos[0])
		self.assertAlmostEqual(0, newpos[1])
		self.assertAlmostEqual(math.pi/8, newpos[2])

		gv.advance(1,0)
		newpos = gv.getPosition()
		self.assertAlmostEqual(0, newpos[0])
		self.assertAlmostEqual(0, newpos[1])
		self.assertAlmostEqual(math.pi/4, newpos[2])

		gv.advance(8,0) # check if angle will wrap around once it exceeds [-pi, pi)
		newpos = gv.getPosition()
		self.assertAlmostEqual(0, newpos[0])
		self.assertAlmostEqual(0, newpos[1])
		self.assertAlmostEqual(-0.75*math.pi, newpos[2])

		# clockwise circular rotation in place
		t = 0
		pose = [0, 0, t]
		s = 0
		dt = -math.pi/6
		gv = GroundVehicle(pose, s, dt)

		gv.advance(1,0)
		newpos = gv.getPosition()
		self.assertAlmostEqual(0, newpos[0])
		self.assertAlmostEqual(0, newpos[1])
		self.assertAlmostEqual(-math.pi/6, newpos[2])

		gv.advance(1,0)
		newpos = gv.getPosition()
		self.assertAlmostEqual(0, newpos[0])
		self.assertAlmostEqual(0, newpos[1])
		self.assertAlmostEqual(-math.pi/3, newpos[2])

		gv.advance(8,0) # check if angle will wrap around once it exceeds [-pi, pi)
		newpos = gv.getPosition()
		self.assertAlmostEqual(0, newpos[0])
		self.assertAlmostEqual(0, newpos[1])
		self.assertAlmostEqual(math.pi/3, newpos[2])

		# moving in a counterclockwise circle of radius r = s/omega, starting at 6 o'clock
		t = 0
		pose = [0, 0, t]
		s = 5*math.pi
		dt = math.pi
		gv = GroundVehicle(pose, s, dt)

		gv.advance(0,250) #eighth circle, from 6 o'clock to 4:30
		newpos = gv.getPosition()
		self.assertAlmostEqual(5/math.sqrt(2), newpos[0])
		self.assertAlmostEqual(5 - 5/math.sqrt(2), newpos[1])
		self.assertAlmostEqual(math.pi/4, newpos[2])

		gv.advance(0,250) #another eighth circle, to 3 o'clock
		newpos = gv.getPosition()
		self.assertAlmostEqual(5, newpos[0])
		self.assertAlmostEqual(5, newpos[1])
		self.assertAlmostEqual(math.pi/2, newpos[2])

		gv.advance(0, 500) #another quarter circle, to 12 noon
		newpos = gv.getPosition()
		self.assertAlmostEqual(0, newpos[0])
		self.assertAlmostEqual(10, newpos[1])
		self.assertAlmostEqual(-math.pi, newpos[2])

		gv.advance(1,0) #half circle, back to start position at 6 o'clock
		newpos = gv.getPosition()
		self.assertAlmostEqual(0, newpos[0])
		self.assertAlmostEqual(0, newpos[1])
		self.assertAlmostEqual(0, newpos[2])

	def testAdvanceNoTime(self):
		# make sure that advance does nothing if called with sec = 0, msec = 0
		t = 0
		pose = [0, 0, t]
		s = 5*math.pi
		dt = math.pi
		gv = GroundVehicle(pose, s, dt)

		gv.advance(0,0)
		newpos = gv.getPosition()
		self.assertAlmostEqual(pose[0], newpos[0])
		self.assertAlmostEqual(pose[1], newpos[1])
		self.assertAlmostEqual(pose[2], newpos[2])

	def testAdvanceNegativeTime(self):
		# make sure that advance works in reverse -- if called with negative time

		# moving in a circle of radius r = s/omega, starting at 6 o'clock
		# vehicle is oriented to move counterclockwise, but time is running backward, so vehicle moves clockwise
		t = 0
		pose = [0, 0, t]
		s = 5*math.pi
		dt = math.pi
		gv = GroundVehicle(pose, s, dt)

		gv.advance(0, -250) #eighth circle, from 6 o'clock to 7:30
		newpos = gv.getPosition()
		self.assertAlmostEqual(-5/math.sqrt(2), newpos[0])
		self.assertAlmostEqual(5 - 5/math.sqrt(2), newpos[1])
		self.assertAlmostEqual(-math.pi/4, newpos[2])

		gv.advance(0, -250) #another eighth circle, to 9 o'clock
		newpos = gv.getPosition()
		self.assertAlmostEqual(-5, newpos[0])
		self.assertAlmostEqual(5, newpos[1])
		self.assertAlmostEqual(-math.pi/2, newpos[2])

		gv.advance(0, -500) #another quarter circle, to 12 noon
		newpos = gv.getPosition()
		self.assertAlmostEqual(0, newpos[0])
		self.assertAlmostEqual(10, newpos[1])
		self.assertAlmostEqual(-math.pi, newpos[2])

		gv.advance(-1, 0) #half circle, back to start position at 6 o'clock
		newpos = gv.getPosition()
		self.assertAlmostEqual(0, newpos[0])
		self.assertAlmostEqual(0, newpos[1])
		self.assertAlmostEqual(0, newpos[2])

	# Tests if the returned angle is in the range [-Pi, Pi)
	def testNormalizeAngle(self):
		# Within range boundaries
		self.assertAlmostEqual(0, GroundVehicle.normalizeAngle(0))

		# Near upper boundary
		self.assertAlmostEqual(math.radians(179), GroundVehicle.normalizeAngle(math.radians(179)))

		# Near lower boundary
		self.assertAlmostEqual(-math.pi, GroundVehicle.normalizeAngle(-math.pi))

		# Above upper boundary
		self.assertAlmostEqual(-math.pi/2, GroundVehicle.normalizeAngle(3.5*math.pi))

		# Below lower boundary
		self.assertAlmostEqual(math.pi/2, GroundVehicle.normalizeAngle(-3.5*math.pi))

# main method which executes unit tests when TestGroundVehicle.py is run directly
if __name__ == "__main__":
	unittest.main()