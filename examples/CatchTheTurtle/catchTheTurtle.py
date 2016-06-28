#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
import sys, signal
sys.path.append('/usr/local/share/jderobot/python/visualHFSM_py')
import traceback, threading, time
from automatagui import AutomataGui, QtGui, GuiSubautomata

import numpy
import jderobot
import cv2

from jderobot import ArDroneExtraPrx
from jderobot import CMDVelPrx
from jderobot import CameraPrx

class Automata():

	def __init__(self):
		self.lock = threading.Lock()
		self.displayGui = False
		self.StatesSub1 = [
			"TakeOff",
			"FollowTurtle",
			"Land",
		]

		self.StatesSub2 = [
			"FindTurtle",
			"FindTurtle_ghost",
			"FollowTurtle",
			"FollowTurtle_ghost",
		]

		self.StatesSub3 = [
			"LoseTurtle",
			"LoseTurtle_ghost",
			"Landing",
			"Landing_ghost",
		]

		self.sub1 = "TakeOff"
		self.run1 = True
		self.sub2 = "FindTurtle_ghost"
		self.run2 = True
		self.sub3 = "LoseTurtle_ghost"
		self.run3 = True

	def setVelocity(self, vx, vy, vz, yaw):
		cmd = jderobot.CMDVelData()
		cmd.linearX = vy
		cmd.linearY = vx
		cmd.linearZ = vz
		cmd.angularZ = yaw
		cmd.angularX = cmd.angularY = 1.0
		self.CMDVelPrx.setCMDVelData(cmd)
	
	def getImage(self):
		img = self.CameraPrx.getImageData("RGB8")
		height = img.description.height
		width = img.description.width
		imgPixels = numpy.zeros((height, width, 3), numpy.uint8)
		imgPixels = numpy.frombuffer(img.pixelData, dtype=numpy.uint8)
		imgPixels.shape = height, width, 3
		return imgPixels
	
	def getContours(self):
		img = self.getImage()
		img = cv2.GaussianBlur(img, (5, 5), 0)
		hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	
		maxValues = numpy.array(self.hmax, self.vmax, self.smax)
		minValues = numpy.array(self.hmin, self.vmin, self.smin)
		
		thresoldImg = cv2.inRange(hsvImg, minValues, maxValues)
		conts, hierarchy = cv2.findContours(thresoldImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		return conts, hierarchy	
	
		
	class PID:
		def __init__(self, Epsilon=.01, Kp=1, Ki=1, Kd=1, Imax=300, Imin=-300):
			self.Ep = Epsilon		
			self.Kp = Kp
			self.Ki = Ki
			self.Kd = Kd
			self.Imax = Imax
			self.Imin = Imin
			self.lastError = 0
			self.cumulativeError = 0
	
		def updateCumulativeError(self, error):
			self.cumulativeError += error
			if self.cumulativeError > self.Imax:
				self.cumulativeError = self.Imax
			if self.cumulativeError < self.Imin:
				self.cumulativeError = self.Imin
	
		def process(self, error):
			if -self.Ep < error < self.Ep:
				return 0
			P = self.Kp * error
	
			self.updateCumulativeError(error)
			I = self.Ki * self.cumulativeError
	
			D = self.Kd * (error -  self.lastError)
			self.lastError = error
	
			vel = P + I + D
			return vel
			
	def startThreads(self):
		self.t1 = threading.Thread(target=self.subautomata1)
		self.t1.start()
		self.t2 = threading.Thread(target=self.subautomata2)
		self.t2.start()
		self.t3 = threading.Thread(target=self.subautomata3)
		self.t3.start()

	def createAutomata(self):
		guiSubautomataList = []

		# Creating subAutomata1
		guiSubautomata1 = GuiSubautomata(1,0, self.automataGui)

		guiSubautomata1.newGuiNode(1, 0, 111, 195, 1, 'TakeOff')
		guiSubautomata1.newGuiNode(2, 2, 323, 206, 0, 'FollowTurtle')
		guiSubautomata1.newGuiNode(3, 3, 531, 229, 0, 'Land')

		guiSubautomata1.newGuiTransition((111, 195), (323, 206), (191, 244), 1, 1, 2)
		guiSubautomata1.newGuiTransition((323, 206), (531, 229), (419, 267), 2, 2, 3)
		guiSubautomataList.append(guiSubautomata1)

		# Creating subAutomata2
		guiSubautomata2 = GuiSubautomata(2,2, self.automataGui)

		guiSubautomata2.newGuiNode(4, 0, 118, 156, 1, 'FindTurtle')
		guiSubautomata2.newGuiNode(5, 0, 410, 171, 0, 'FollowTurtle')

		guiSubautomata2.newGuiTransition((118, 156), (410, 171), (276, 101), 3, 4, 5)
		guiSubautomata2.newGuiTransition((410, 171), (118, 156), (258, 221), 4, 5, 4)
		guiSubautomataList.append(guiSubautomata2)

		# Creating subAutomata3
		guiSubautomata3 = GuiSubautomata(3,3, self.automataGui)

		guiSubautomata3.newGuiNode(7, 0, 117, 188, 1, 'LoseTurtle')
		guiSubautomata3.newGuiNode(8, 0, 378, 213, 0, 'Landing')

		guiSubautomata3.newGuiTransition((378, 213), (117, 188), (271, 109), 6, 8, 7)
		guiSubautomata3.newGuiTransition((117, 188), (378, 213), (250, 258), 7, 7, 8)
		guiSubautomataList.append(guiSubautomata3)


		return guiSubautomataList

	def shutDown(self):
		self.run1 = False
		self.run2 = False
		self.run3 = False

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

		self.heighIters = 0
		self.maxIters = 50
		self.contours = []
		
		
		#Filter Values
		self.hmin = 50
		self.hmax = 70
		self.vmin = 20
		self.vmax = 235
		self.smin = 10
		self.smax = 245

		while(self.run1):
			totala = time.time() * 1000000

			# Evaluation if
			if(self.sub1 == "TakeOff"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 2.5):
						self.sub1 = "FollowTurtle"
						t_activated = False
						print "Iters:", self.heighIters
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('FollowTurtle')

			elif(self.sub1 == "FollowTurtle"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 90):
						self.sub1 = "Land"
						t_activated = False
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('Land')


			# Actuation if
			if(self.sub1 == "TakeOff"):
				self.ExtraPrx.takeoff()
				
				#Get some heigh
				self.setVelocity(0, 0, 1, 0)
				
				self.heighIters += 1
			elif(self.sub1 == "FollowTurtle"):
				self.contours, hierarchy = self.getContours()
			elif(self.sub1 == "Land"):
				self.contours, hierarchy = self.getContours()

			totalb = time.time() * 1000000
			msecs = (totalb - totala) / 1000;
			if(msecs < 0 or msecs > cycle):
				msecs = cycle
			else:
				msecs = cycle - msecs

			time.sleep(msecs / 1000)
			if(msecs < 33 ):
				time.sleep(33 / 1000);


	def subautomata2(self):
		self.run2 = True
		cycle = 100
		t_activated = False
		t_fin = 0


		targetX = 125
		targetY = 125
		
		minError = 8
		
		xPid = self.PID(minError, 0.01, 0.02, 0.03, 5, -5)
		yPid = self.PID(minError, 0.01, 0.02, 0.03, 5, -5)

		while(self.run2):
			totala = time.time() * 1000000

			if(self.sub1 == "FollowTurtle"):
				if ((self.sub2 == "FindTurtle_ghost") or (self.sub2 == "FollowTurtle_ghost")):
					ghostStateIndex = self.StatesSub2.index(self.sub2)
					self.sub2 = self.StatesSub2[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub2 == "FindTurtle"):
					if(self.contours):
						self.sub2 = "FollowTurtle"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('FollowTurtle')

				elif(self.sub2 == "FollowTurtle"):
					if(not self.contours):
						self.sub2 = "FindTurtle"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('FindTurtle')


				# Actuation if
				if(self.sub2 == "FindTurtle"):
					if self.heighIters <= self.maxIters:
						self.setVelocity(0, 0, 1, 0)
						self.heighIters += 1
						print "iters:", self.heighIters
					else:
						print "max hight reached"
				elif(self.sub2 == "FollowTurtle"):
					#We assume there is only one green target on the screen
					cnt = self.contours[0]
					
					#Locate the minimal circle enclosing the contour
					(x, y), radius = cv2.minEnclosingCircle(cnt)
					center = (int(x), int(y))
					radius = int(radius)
					
					xError = targetX - center[0]
					yError = targetY - center[1]
					
					xVel = xPid.process(xError)
					yVel = yPidprocess(yError)
					
					#Control Heigh#
					
					self.setVelocity(xVel, yVel, 0, 0)
					print "xError:", xError, "yError:", yError
					print "xVel:", xVel, "yVel:", yVel
			else:
				if(self.sub2 == "FindTurtle"):
					ghostStateIndex = self.StatesSub2.index(self.sub2) + 1
					self.sub2 = self.StatesSub2[ghostStateIndex]
				elif(self.sub2 == "FollowTurtle"):
					ghostStateIndex = self.StatesSub2.index(self.sub2) + 1
					self.sub2 = self.StatesSub2[ghostStateIndex]

			totalb = time.time() * 1000000
			msecs = (totalb - totala) / 1000;
			if(msecs < 0 or msecs > cycle):
				msecs = cycle
			else:
				msecs = cycle - msecs

			time.sleep(msecs / 1000)
			if(msecs < 33 ):
				time.sleep(33 / 1000);


	def subautomata3(self):
		self.run3 = True
		cycle = 100
		t_activated = False
		t_fin = 0



		while(self.run3):
			totala = time.time() * 1000000

			if(self.sub1 == "Land"):
				if ((self.sub3 == "LoseTurtle_ghost") or (self.sub3 == "Landing_ghost")):
					ghostStateIndex = self.StatesSub3.index(self.sub3)
					self.sub3 = self.StatesSub3[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub3 == "LoseTurtle"):
					if(not self.contours):
						self.sub3 = "Landing"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('Landing')

				elif(self.sub3 == "Landing"):
					if(self.contours):
						self.sub3 = "LoseTurtle"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('LoseTurtle')


				# Actuation if
				if(self.sub3 == "LoseTurtle"):
					self.setVelocity(1, 0, 0, 0)
				elif(self.sub3 == "Landing"):
					self.ExtraPrx.land()
			else:
				if(self.sub3 == "LoseTurtle"):
					ghostStateIndex = self.StatesSub3.index(self.sub3) + 1
					self.sub3 = self.StatesSub3[ghostStateIndex]
				elif(self.sub3 == "Landing"):
					ghostStateIndex = self.StatesSub3.index(self.sub3) + 1
					self.sub3 = self.StatesSub3[ghostStateIndex]

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

		# Contact to Extra
		Extra = self.ic.propertyToProxy('automata.ArDroneExtra.Proxy')
		if(not Extra):
			raise Exception('could not create proxy with Extra')
		self.ExtraPrx = ArDroneExtraPrx.checkedCast(Extra)
		if(not self.ExtraPrx):
			raise Exception('invalid proxy automata.ArDroneExtra.Proxy')
		print 'Extra connected'

		# Contact to CMDVel
		CMDVel = self.ic.propertyToProxy('automata.CMDVel.Proxy')
		if(not CMDVel):
			raise Exception('could not create proxy with CMDVel')
		self.CMDVelPrx = CMDVelPrx.checkedCast(CMDVel)
		if(not self.CMDVelPrx):
			raise Exception('invalid proxy automata.CMDVel.Proxy')
		print 'CMDVel connected'

		# Contact to Camera
		Camera = self.ic.propertyToProxy('automata.Camera.Proxy')
		if(not Camera):
			raise Exception('could not create proxy with Camera')
		self.CameraPrx = CameraPrx.checkedCast(Camera)
		if(not self.CameraPrx):
			raise Exception('invalid proxy automata.Camera.Proxy')
		print 'Camera connected'


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
		self.t2.join()
		self.t3.join()


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
