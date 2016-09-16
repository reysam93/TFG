#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
import sys, signal
sys.path.append('/usr/local/share/jderobot/python/visualHFSM_py')
import traceback, threading, time
from automatagui import AutomataGui, QtGui, GuiSubautomata

import random
import math

from jderobot import MotorsPrx
from jderobot import Pose3DPrx
from jderobot import LaserPrx

class Automata():

	def __init__(self):
		self.lock = threading.Lock()
		self.displayGui = False
		self.StatesSub1 = [
			"Go",
			"GoBack",
			"Rotate",
		]

		self.sub1 = "Go"
		self.run1 = True

	def getRobotTheta(self):
	        d = self.EncodersPrx.getPose3DData()
	        theta = math.atan2(2*(d.q0*d.q3 + d.q1*d.q2), 1-2*(d.q2*d.q2 + d.q3*d.q3))
	        return theta
	def startThreads(self):
		self.t1 = threading.Thread(target=self.subautomata1)
		self.t1.start()

	def createAutomata(self):
		guiSubautomataList = []

		# Creating subAutomata1
		guiSubautomata1 = GuiSubautomata(1,0, self.automataGui)

		guiSubautomata1.newGuiNode(1, 0, 112, 126, 1, 'Go')
		guiSubautomata1.newGuiNode(2, 0, 372, 136, 0, 'GoBack')
		guiSubautomata1.newGuiNode(3, 0, 238, 308, 0, 'Rotate')

		guiSubautomata1.newGuiTransition((112, 126), (372, 136), (237, 114), 1, 1, 2)
		guiSubautomata1.newGuiTransition((372, 136), (238, 308), (305, 222), 2, 2, 3)
		guiSubautomata1.newGuiTransition((238, 308), (112, 126), (140, 216), 3, 3, 1)
		guiSubautomataList.append(guiSubautomata1)


		return guiSubautomataList

	def shutDown(self):
		self.run1 = False

	def runGui(self):
		app = QtGui.QApplication(sys.argv)
		self.automataGui = AutomataGui()
		self.automataGui.setAutomata(self.createAutomata())
		self.automataGui.loadAutomata()
		self.startThreads()
		self.automataGui.show()
		app.exec_()

	def subautomata1(self):
		self.run1 = True
		cycle = 100
		t_activated = False
		t_fin = 0

		laserData = self.LasersPrx.getLaserData()
		minDistance = 1.5
		dist = None
		destinyAngle = None
		error = 0
		
		print "numero de lasers (grados):", laserData.numLaser
		

		while(self.run1):
			totala = time.time() * 1000000

			# Evaluation if
			if(self.sub1 == "Go"):
				if(dist != None and dist < minDistance):
					self.sub1 = "GoBack"
					self.MotorsPrx.setV(0)
					print "stopping"
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('GoBack')

			elif(self.sub1 == "GoBack"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 1.5):
						self.sub1 = "Rotate"
						t_activated = False
						angle = self.getRobotTheta()
						print "my Angle:", angle
						self.MotorsPrx.setV(0)
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('Rotate')

			elif(self.sub1 == "Rotate"):
				if(error <= 0.1 and error >= -0.1):
					self.sub1 = "Go"
					destinyAngle =None
					self.MotorsPrx.setW(0)
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('Go')


			# Actuation if
			if(self.sub1 == "Go"):
				self.MotorsPrx.setV(1)
				laserData = self.LasersPrx.getLaserData()
				
				dist = None
				for i in range(60, 120):
					dist = laserData.distanceData[i]/1000
					if dist == None or laserData.distanceData[i]/1000 < dist:
						dist = laserData.distanceData[i]/1000
				
				print "dist:", dist
			elif(self.sub1 == "GoBack"):
				self.MotorsPrx.setV(-0.1)
				print "back"
			elif(self.sub1 == "Rotate"):
				if destinyAngle == None:
					turn = random.uniform(-math.pi, math.pi)
					destinyAngle = (angle + turn) % (math.pi)
					print "DestinyAngle:", destinyAngle
				
				angle =  self.getRobotTheta()
				error = (destinyAngle - angle)*0.75
				
				if error > 0 and error < 0.1:
					error = 0.1
				elif error < 0 and error > -0.1:
					error = -0.1
				
				print "angle:", angle, "destiny:", destinyAngle, "speed:", error
				self.MotorsPrx.setW(error)

			totalb = time.time() * 1000000
			msecs = (totalb - totala) / 1000;
			if(msecs < 0 or msecs > cycle):
				msecs = cycle
			else:
				msecs = cycle - msecs

			time.sleep(msecs / 1000)
			if(msecs < 33 ):
				time.sleep(33 / 1000);


	def connectToProxys(self):
		self.ic = Ice.initialize(sys.argv)

		# Contact to Motors
		Motors = self.ic.propertyToProxy('automata.Motors.Proxy')
		if(not Motors):
			raise Exception('could not create proxy with Motors')
		self.MotorsPrx = MotorsPrx.checkedCast(Motors)
		if(not self.MotorsPrx):
			raise Exception('invalid proxy automata.Motors.Proxy')
		print 'Motors connected'

		# Contact to Pose3D
		Pose3D = self.ic.propertyToProxy('automata.Pose3D.Proxy')
		if(not Pose3D):
			raise Exception('could not create proxy with Pose3D')
		self.Pose3DPrx = Pose3DPrx.checkedCast(Pose3D)
		if(not self.Pose3DPrx):
			raise Exception('invalid proxy automata.Pose3D.Proxy')
		print 'Pose3D connected'

		# Contact to Laser
		Laser = self.ic.propertyToProxy('automata.Laser.Proxy')
		if(not Laser):
			raise Exception('could not create proxy with Laser')
		self.LaserPrx = LaserPrx.checkedCast(Laser)
		if(not self.LaserPrx):
			raise Exception('invalid proxy automata.Laser.Proxy')
		print 'Laser connected'


	def destroyIc(self):
		if(self.ic):
			self.ic.destroy()


	def start(self):
		if self.displayGui:
			self.guiThread = threading.Thread(target=self.runGui)
			self.guiThread.start()
		else:
			self.startThreads()



	def join(self):
		if self.displayGui:
			self.guiThread.join()
		self.t1.join()


	def readArgs(self):
		for arg in sys.argv:
			splitedArg = arg.split('=')
			if splitedArg[0] == '--displaygui':
				if splitedArg[1] == 'True' or splitedArg[1] == 'true':
					self.displayGui = True
					print 'runtime gui enabled'
				else:
					self.displayGui = False
					print 'runtime gui disabled'


if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	automata = Automata()
	try:
		automata.connectToProxys()
		automata.readArgs()
		automata.start()
		automata.join()

		sys.exit(0)
	except:
		traceback.print_exc()
		automata.destroyIc()
		sys.exit(-1)
