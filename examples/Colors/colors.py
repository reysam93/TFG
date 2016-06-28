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
from jderobot import Pose3DPrx

class Automata():

	def __init__(self):
		self.lock = threading.Lock()
		self.displayGui = False
		self.StatesSub1 = [
			"TakeOff",
			"FollowGreenLookBlue",
			"FollowBlueLookGreen",
			"FollowGreenLookRed",
			"FollowRed",
		]

		self.StatesSub3 = [
			"WaitGreen",
			"WaitGreen_ghost",
			"FollowGreen",
			"FollowGreen_ghost",
		]

		self.StatesSub4 = [
			"WaitBlue",
			"WaitBlue_ghost",
			"FollowBlue",
			"FollowBlue_ghost",
		]

		self.StatesSub5 = [
			"WaitGreen2",
			"WaitGreen2_ghost",
			"FollowGreen2",
			"FollowGreen2_ghost",
		]

		self.StatesSub6 = [
			"WaitRed",
			"WaitRed_ghost",
			"FollowingRed",
			"FollowingRed_ghost",
		]

		self.sub1 = "TakeOff"
		self.run1 = True
		self.sub3 = "WaitGreen_ghost"
		self.run3 = True
		self.sub4 = "WaitBlue_ghost"
		self.run4 = True
		self.sub5 = "WaitGreen2_ghost"
		self.run5 = True
		self.sub6 = "WaitRed_ghost"
		self.run6 = True

	def getImage(self):
		img = self.CameraPrx.getImageData("RGB8")
		height = img.description.height
		width=img.description.width
		
		if self.targetX == None and self.targetY == None:
			self.targetX = width/2
			self.targetY = height/2
			print "targetX:", self.targetX, "targetY:,", self.targetY
	
		imgPixels = numpy.zeros((height, width, 3), numpy.uint8)
		imgPixels = numpy.frombuffer(img.pixelData, dtype=numpy.uint8)
		imgPixels.shape = height, width, 3
		return imgPixels
	
	
	def getContours(self, img, minValues, maxValues):
		hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		thresholdImg = cv2.inRange(hsvImg, minValues, maxValues)
		contours, hierarchy = cv2.findContours(thresholdImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		return contours, hierarchy	
	
	
	def getVelocities(self, contours):
		contour = max(contours, key=cv2.contourArea)
		(x, y), radius = cv2.minEnclosingCircle(contour)
		xError = self.targetX - x
		yError = self.targetY - y
	
		xVel = self.xPID.process(xError)
		yVel = self.yPID.process(yError)
		return xVel, yVel
	
	
	def setVelocity(self, vx, vy, vz, yaw):
		cmd = jderobot.CMDVelData()
		cmd.linearX = vy
		cmd.linearY = vx
		cmd.linearZ = vz
		cmd.angularZ = yaw
		cmd.angularX = cmd.angularY = 1.0
		self.CMDVelPrx.setCMDVelData(cmd)
	
	
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
				elif self.cumulativeError < self.Imin:
					self.cumulativeError = self.Imin
		
			def process(self, error, derivative=None, integral=None):
				if -self.Ep < error < self.Ep:
					return 0
		
				P = self.Kp * error
				self.updateCumulativeError(error)
				if integral != None:
					I = self.Ki * integral
				else:
					I = self.Ki * self.cumulativeError
	
				if derivative != None:
					D = self.Kd * derivative
				else:
					D = self.Kd * (error - self.lastError)
				self.lastError = error
				speed = P + I + D
	
				#if speed > 0.4:
				#	speed = 0.4
				#if speed < -0.4:
				#	speed = -0.4
	
				return speed
	
	def startThreads(self):
		self.t1 = threading.Thread(target=self.subautomata1)
		self.t1.start()
		self.t3 = threading.Thread(target=self.subautomata3)
		self.t3.start()
		self.t4 = threading.Thread(target=self.subautomata4)
		self.t4.start()
		self.t5 = threading.Thread(target=self.subautomata5)
		self.t5.start()
		self.t6 = threading.Thread(target=self.subautomata6)
		self.t6.start()

	def createAutomata(self):
		guiSubautomataList = []

		# Creating subAutomata1
		guiSubautomata1 = GuiSubautomata(1,0, self.automataGui)

		guiSubautomata1.newGuiNode(1, 0, 117, 139, 1, 'TakeOff')
		guiSubautomata1.newGuiNode(2, 3, 303, 150, 0, 'FollowGreenLookBlue')
		guiSubautomata1.newGuiNode(5, 4, 421, 244, 0, 'FollowBlueLookGreen')
		guiSubautomata1.newGuiNode(6, 5, 325, 312, 0, 'FollowGreenLookRed')
		guiSubautomata1.newGuiNode(7, 6, 142, 326, 0, 'FollowRed')

		guiSubautomata1.newGuiTransition((303, 150), (421, 244), (421, 157), 4, 2, 5)
		guiSubautomata1.newGuiTransition((421, 244), (325, 312), (436, 325), 5, 5, 6)
		guiSubautomata1.newGuiTransition((325, 312), (142, 326), (232, 331), 6, 6, 7)
		guiSubautomata1.newGuiTransition((117, 139), (303, 150), (194, 174), 15, 1, 2)
		guiSubautomataList.append(guiSubautomata1)

		# Creating subAutomata3
		guiSubautomata3 = GuiSubautomata(3,2, self.automataGui)

		guiSubautomata3.newGuiNode(3, 0, 67, 147, 1, 'WaitGreen')
		guiSubautomata3.newGuiNode(4, 0, 269, 152, 0, 'FollowGreen')

		guiSubautomata3.newGuiTransition((67, 147), (269, 152), (173, 40), 2, 3, 4)
		guiSubautomata3.newGuiTransition((269, 152), (67, 147), (170, 221), 3, 4, 3)
		guiSubautomataList.append(guiSubautomata3)

		# Creating subAutomata4
		guiSubautomata4 = GuiSubautomata(4,5, self.automataGui)

		guiSubautomata4.newGuiNode(8, 0, 111, 129, 1, 'WaitBlue')
		guiSubautomata4.newGuiNode(9, 0, 296, 141, 0, 'FollowBlue')

		guiSubautomata4.newGuiTransition((111, 129), (296, 141), (200, 60), 7, 8, 9)
		guiSubautomata4.newGuiTransition((296, 141), (111, 129), (191, 198), 8, 9, 8)
		guiSubautomataList.append(guiSubautomata4)

		# Creating subAutomata5
		guiSubautomata5 = GuiSubautomata(5,6, self.automataGui)

		guiSubautomata5.newGuiNode(10, 0, 79, 120, 1, 'WaitGreen2')
		guiSubautomata5.newGuiNode(11, 0, 336, 152, 0, 'FollowGreen2')

		guiSubautomata5.newGuiTransition((336, 152), (79, 120), (196, 220), 9, 11, 10)
		guiSubautomata5.newGuiTransition((79, 120), (336, 152), (217, 56), 10, 10, 11)
		guiSubautomataList.append(guiSubautomata5)

		# Creating subAutomata6
		guiSubautomata6 = GuiSubautomata(6,7, self.automataGui)

		guiSubautomata6.newGuiNode(12, 0, 104, 151, 1, 'WaitRed')
		guiSubautomata6.newGuiNode(13, 0, 341, 163, 0, 'FollowingRed')

		guiSubautomata6.newGuiTransition((104, 151), (341, 163), (221, 56), 11, 12, 13)
		guiSubautomata6.newGuiTransition((341, 163), (104, 151), (225, 219), 12, 13, 12)
		guiSubautomataList.append(guiSubautomata6)


		return guiSubautomataList

	def shutDown(self):
		self.run1 = False
		self.run3 = False
		self.run4 = False
		self.run5 = False
		self.run6 = False

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

		#ControlValues
		minError = 10
		self.targetX = None
		self.targetY = None
		self.hIters = 0
		#maxHIters = 35	#For gazebo
		maxHIters = 20	#For real
		refracIters = 0
		refracTime = 35
		
		#Contours
		self.greenConts = []
		self.blueConts = []
		self.redConts = []
		
		#Filter values for simulator. Order: [H, S, V] 
		minGValues = numpy.array([30,  129, 33])
		maxGValues = numpy.array([70, 255 , 190])
		minBValues = numpy.array([0, 140, 37])
		maxBValues = numpy.array([16, 255, 200])
		minRValues = numpy.array([100, 209, 82])
		maxRValues =  numpy.array([153, 255, 200])
		
		#Filter values for real. Order: [H, S, V] 
		#minGValues = numpy.array([31,0,120])
		#maxGValues = numpy.array([70, 46 , 255])
		#minBValues = numpy.array([9,126,175])
		#maxBValues = numpy.array([58,209,255])
		#minRValues = numpy.array([93,195,154])
		#maxRValues =  numpy.array([155,255,255])
		
		#PID control
		self.xPID = self.PID(minError, 0.01, 0.01, 0.02, 5, -5)
		self.yPID = self.PID(minError, 0.01, 0.01, 0.02, 5, -5)
		

		while(self.run1):
			totala = time.time() * 1000000

			# Evaluation if
			if(self.sub1 == "TakeOff"):
				if(self.hIters >= maxHIters):
					self.sub1 = "FollowGreenLookBlue"
					self.setVelocity(0,0,0,0)
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('FollowGreenLookBlue')

			elif(self.sub1 == "FollowGreenLookBlue"):
				if(self.blueConts):
					self.sub1 = "FollowBlueLookGreen"
					print "Reseting Green Conts"
					self.greenConts = []
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('FollowBlueLookGreen')

			elif(self.sub1 == "FollowBlueLookGreen"):
				if(self.greenConts):
					self.sub1 = "FollowGreenLookRed"
					self.blueConts = []
					refracIters = 0
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('FollowGreenLookRed')

			elif(self.sub1 == "FollowGreenLookRed"):
				if(self.redConts):
					self.sub1 = "FollowRed"
					self.greenConts = []
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('FollowRed')


			# Actuation if
			if(self.sub1 == "TakeOff"):
				if self.hIters == 0:
					self.ExtraPrx.takeoff()
					print "taking off"
				else:
					#self.setVelocity(0,0,0.5,0)
					self.setVelocity(0,0,1,0)
				
				self.hIters += 1
				print "ITERS: ", self.hIters
			elif(self.sub1 == "FollowGreenLookBlue"):
				inImg = self.getImage()
				softenedImg = cv2.bilateralFilter(inImg, 9, 75, 75)
				self.greenConts, hierarchy = self.getContours(softenedImg, minGValues, maxGValues)
				self.blueConts,  hierarchy = self.getContours(softenedImg, minBValues, maxBValues) 
				
								
			elif(self.sub1 == "FollowBlueLookGreen"):
				inImg = self.getImage()
				softenedImg = cv2.bilateralFilter(inImg, 9, 75, 75)
				self.blueConts,  hierarchy = self.getContours(softenedImg, minBValues, maxBValues) 
				
				if refracIters >= refracTime:
					self.greenConts, hierarchy = self.getContours(softenedImg, minGValues, maxGValues)
					print "inside refrac time"
				else:
					print "refrac Iters:", refracIters
				
				refracIters += 1
			elif(self.sub1 == "FollowGreenLookRed"):
				inImg = self.getImage()
				softenedImg = cv2.bilateralFilter(inImg, 9, 75, 75)
				self.greenConts, hierarchy = self.getContours(softenedImg, minGValues, maxGValues)
				self.redConts,  hierarchy = self.getContours(softenedImg, minRValues, maxRValues)
				print "RED:", self.redConts
			elif(self.sub1 == "FollowRed"):
				inImg = self.getImage()
				softenedImg = cv2.bilateralFilter(inImg, 9, 75, 75)
				self.redConts, hierarchy = self.getContours(softenedImg, minRValues, maxRValues)

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

			if(self.sub1 == "FollowGreenLookBlue"):
				if ((self.sub3 == "WaitGreen_ghost") or (self.sub3 == "FollowGreen_ghost")):
					ghostStateIndex = self.StatesSub3.index(self.sub3)
					self.sub3 = self.StatesSub3[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub3 == "WaitGreen"):
					if(self.greenConts):
						self.sub3 = "FollowGreen"
						print "Green Finded"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('FollowGreen')

				elif(self.sub3 == "FollowGreen"):
					if(not self.greenConts):
						self.sub3 = "WaitGreen"
						print "Green Lost"
						self.setVelocity(0, 0, 0, 0)
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('WaitGreen')


				# Actuation if
				if(self.sub3 == "WaitGreen"):
					self.setVelocity(0, 0, 0, 0)
				elif(self.sub3 == "FollowGreen"):
					xVel, yVel = self.getVelocities(self.greenConts)
					self.setVelocity(xVel, yVel, 0, 0)
			else:
				if(self.sub3 == "WaitGreen"):
					ghostStateIndex = self.StatesSub3.index(self.sub3) + 1
					self.sub3 = self.StatesSub3[ghostStateIndex]
				elif(self.sub3 == "FollowGreen"):
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


	def subautomata4(self):
		self.run4 = True
		cycle = 100
		t_activated = False
		t_fin = 0



		while(self.run4):
			totala = time.time() * 1000000

			if(self.sub1 == "FollowBlueLookGreen"):
				if ((self.sub4 == "WaitBlue_ghost") or (self.sub4 == "FollowBlue_ghost")):
					ghostStateIndex = self.StatesSub4.index(self.sub4)
					self.sub4 = self.StatesSub4[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub4 == "WaitBlue"):
					if(self.blueConts):
						self.sub4 = "FollowBlue"
						print "Blue Finded"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('FollowBlue')

				elif(self.sub4 == "FollowBlue"):
					if(not self.blueConts):
						self.sub4 = "WaitBlue"
						print "Blue Lost"
						self.setVelocity(0, 0, 0, 0)
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('WaitBlue')


				# Actuation if
				if(self.sub4 == "WaitBlue"):
					self.setVelocity(0, 0, 0, 0)
				elif(self.sub4 == "FollowBlue"):
					xVel, yVel = self.getVelocities(self.blueConts)
					self.setVelocity(xVel, yVel, 0, 0)
			else:
				if(self.sub4 == "WaitBlue"):
					ghostStateIndex = self.StatesSub4.index(self.sub4) + 1
					self.sub4 = self.StatesSub4[ghostStateIndex]
				elif(self.sub4 == "FollowBlue"):
					ghostStateIndex = self.StatesSub4.index(self.sub4) + 1
					self.sub4 = self.StatesSub4[ghostStateIndex]

			totalb = time.time() * 1000000
			msecs = (totalb - totala) / 1000;
			if(msecs < 0 or msecs > cycle):
				msecs = cycle
			else:
				msecs = cycle - msecs

			time.sleep(msecs / 1000)
			if(msecs < 33 ):
				time.sleep(33 / 1000);


	def subautomata5(self):
		self.run5 = True
		cycle = 100
		t_activated = False
		t_fin = 0



		while(self.run5):
			totala = time.time() * 1000000

			if(self.sub1 == "FollowGreenLookRed"):
				if ((self.sub5 == "WaitGreen2_ghost") or (self.sub5 == "FollowGreen2_ghost")):
					ghostStateIndex = self.StatesSub5.index(self.sub5)
					self.sub5 = self.StatesSub5[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub5 == "WaitGreen2"):
					if(self.greenConts):
						self.sub5 = "FollowGreen2"
						print "Green2 finded"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('FollowGreen2')

				elif(self.sub5 == "FollowGreen2"):
					if(not self.greenConts):
						self.sub5 = "WaitGreen2"
						print "Green2 Lost"
						self.setVelocity(0, 0, 0, 0)
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('WaitGreen2')


				# Actuation if
				if(self.sub5 == "WaitGreen2"):
					self.setVelocity(0, 0, 0, 0)
				elif(self.sub5 == "FollowGreen2"):
					xVel, yVel = self.getVelocities(self.greenConts)
					self.setVelocity(xVel, yVel, 0, 0)
			else:
				if(self.sub5 == "WaitGreen2"):
					ghostStateIndex = self.StatesSub5.index(self.sub5) + 1
					self.sub5 = self.StatesSub5[ghostStateIndex]
				elif(self.sub5 == "FollowGreen2"):
					ghostStateIndex = self.StatesSub5.index(self.sub5) + 1
					self.sub5 = self.StatesSub5[ghostStateIndex]

			totalb = time.time() * 1000000
			msecs = (totalb - totala) / 1000;
			if(msecs < 0 or msecs > cycle):
				msecs = cycle
			else:
				msecs = cycle - msecs

			time.sleep(msecs / 1000)
			if(msecs < 33 ):
				time.sleep(33 / 1000);


	def subautomata6(self):
		self.run6 = True
		cycle = 100
		t_activated = False
		t_fin = 0



		while(self.run6):
			totala = time.time() * 1000000

			if(self.sub1 == "FollowRed"):
				if ((self.sub6 == "WaitRed_ghost") or (self.sub6 == "FollowingRed_ghost")):
					ghostStateIndex = self.StatesSub6.index(self.sub6)
					self.sub6 = self.StatesSub6[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub6 == "WaitRed"):
					if(self.redConts):
						self.sub6 = "FollowingRed"
						print "Red FInded"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('FollowingRed')

				elif(self.sub6 == "FollowingRed"):
					if(not self.redConts):
						self.sub6 = "WaitRed"
						print "Red Lost"
						self.setVelocity(0, 0, 0, 0)
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('WaitRed')


				# Actuation if
				if(self.sub6 == "WaitRed"):
					self.setVelocity(0, 0, 0, 0)
				elif(self.sub6 == "FollowingRed"):
					xVel, yVel = self.getVelocities(self.redConts)
					self.setVelocity(xVel, yVel, 0, 0)
			else:
				if(self.sub6 == "WaitRed"):
					ghostStateIndex = self.StatesSub6.index(self.sub6) + 1
					self.sub6 = self.StatesSub6[ghostStateIndex]
				elif(self.sub6 == "FollowingRed"):
					ghostStateIndex = self.StatesSub6.index(self.sub6) + 1
					self.sub6 = self.StatesSub6[ghostStateIndex]

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

		# Contact to Pose3D
		Pose3D = self.ic.propertyToProxy('automata.Pose3D.Proxy')
		if(not Pose3D):
			raise Exception('could not create proxy with Pose3D')
		self.Pose3DPrx = Pose3DPrx.checkedCast(Pose3D)
		if(not self.Pose3DPrx):
			raise Exception('invalid proxy automata.Pose3D.Proxy')
		print 'Pose3D connected'


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
		self.t3.join()
		self.t4.join()
		self.t5.join()
		self.t6.join()


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
