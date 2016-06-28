#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
import sys, signal
sys.path.append('/usr/local/share/jderobot/python/visualHFSM_py')
import traceback, threading, time
from automatagui import AutomataGui, QtGui, GuiSubautomata

import numpy
import cv2
import jderobot

from jderobot import ArDroneExtraPrx
from jderobot import CMDVelPrx
from jderobot import Pose3DPrx
from jderobot import CameraPrx

class Automata():

	def __init__(self):
		self.lock = threading.Lock()
		self.displayGui = False
		self.StatesSub1 = [
			"TakeOff",
			"FollowRoad",
			"MonitorArea",
			"TurnAround",
			"Landing",
			"END",
			"HeighControl",
		]

		self.StatesSub3 = [
			"FindRoad",
			"FindRoad_ghost",
			"FollowingRoad",
			"FollowingRoad_ghost",
		]

		self.StatesSub5 = [
			"ToFirstPos",
			"ToFirstPos_ghost",
			"ToSecondPos",
			"ToSecondPos_ghost",
			"ToThirdPos",
			"ToThirdPos_ghost",
			"Return",
			"Return_ghost",
		]

		self.StatesSub6 = [
			"Descending",
			"Descending_ghost",
			"Land",
			"Land_ghost",
		]

		self.sub1 = "TakeOff"
		self.run1 = True
		self.sub3 = "FindRoad_ghost"
		self.run3 = True
		self.sub5 = "ToFirstPos_ghost"
		self.run5 = True
		self.sub6 = "Descending_ghost"
		self.run6 = True

	def getImage(self):
		img = self.CameraPrx.getImageData("RGB8")
		height = img.description.height
		width=img.description.width
		imgPixels = numpy.zeros((height, width, 3), numpy.uint8)
		imgPixels = numpy.frombuffer(img.pixelData, dtype=numpy.uint8)
		imgPixels.shape = height, width, 3
		return imgPixels
	
	def setVelocity(self, vx, vy, vz, yaw):
		cmd = jderobot.CMDVelData()
		cmd.linearX = vy
		cmd.linearY = vx
		cmd.linearZ = vz
		cmd.angularZ = yaw
		cmd.angularX = cmd.angularY = 1.0
		self.CMDVelPrx.setCMDVelData(cmd)
	
	#The factor indicate the margin of the error multipliyin the error for this factor
	def droneInPosition(self, pos, factor=1 ):
		return (abs(pos[0] - self.xPos) < self.minDist*factor) and (abs(pos[1] - self.yPos) < self.minDist*factor)
	
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
			print 
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
			if speed > 3:
				speed = 3
			elif speed < -3:
				speed = -3
			return speed
	
	def startThreads(self):
		self.t1 = threading.Thread(target=self.subautomata1)
		self.t1.start()
		self.t3 = threading.Thread(target=self.subautomata3)
		self.t3.start()
		self.t5 = threading.Thread(target=self.subautomata5)
		self.t5.start()
		self.t6 = threading.Thread(target=self.subautomata6)
		self.t6.start()

	def createAutomata(self):
		guiSubautomataList = []

		# Creating subAutomata1
		guiSubautomata1 = GuiSubautomata(1,0, self.automataGui)

		guiSubautomata1.newGuiNode(1, 0, 62, 66, 1, 'TakeOff')
		guiSubautomata1.newGuiNode(2, 3, 189, 116, 0, 'FollowRoad')
		guiSubautomata1.newGuiNode(6, 5, 308, 267, 0, 'MonitorArea')
		guiSubautomata1.newGuiNode(11, 0, 263, 428, 0, 'TurnAround')
		guiSubautomata1.newGuiNode(12, 6, 53, 239, 0, 'Landing')
		guiSubautomata1.newGuiNode(14, 0, 41, 427, 0, 'END')
		guiSubautomata1.newGuiNode(17, 0, 481, 139, 0, 'HeighControl')

		guiSubautomata1.newGuiTransition((189, 116), (308, 267), (274, 172), 7, 2, 6)
		guiSubautomata1.newGuiTransition((308, 267), (263, 428), (349, 362), 13, 6, 11)
		guiSubautomata1.newGuiTransition((263, 428), (189, 116), (164, 318), 14, 11, 2)
		guiSubautomata1.newGuiTransition((189, 116), (53, 239), (82, 154), 19, 2, 12)
		guiSubautomata1.newGuiTransition((53, 239), (41, 427), (43, 326), 22, 12, 14)
		guiSubautomata1.newGuiTransition((481, 139), (189, 116), (328, 116), 26, 17, 2)
		guiSubautomata1.newGuiTransition((62, 66), (481, 139), (430, 27), 27, 1, 17)
		guiSubautomata1.newGuiTransition((189, 116), (481, 139), (315, 70), 28, 2, 17)
		guiSubautomata1.newGuiTransition((308, 267), (481, 139), (378, 195), 29, 6, 17)
		guiSubautomata1.newGuiTransition((481, 139), (308, 267), (412, 279), 30, 17, 6)
		guiSubautomataList.append(guiSubautomata1)

		# Creating subAutomata3
		guiSubautomata3 = GuiSubautomata(3,2, self.automataGui)

		guiSubautomata3.newGuiNode(3, 0, 156, 228, 1, 'FindRoad')
		guiSubautomata3.newGuiNode(4, 0, 427, 255, 0, 'FollowingRoad')

		guiSubautomata3.newGuiTransition((156, 228), (427, 255), (297, 157), 2, 3, 4)
		guiSubautomata3.newGuiTransition((427, 255), (156, 228), (265, 320), 3, 4, 3)
		guiSubautomataList.append(guiSubautomata3)

		# Creating subAutomata5
		guiSubautomata5 = GuiSubautomata(5,6, self.automataGui)

		guiSubautomata5.newGuiNode(7, 0, 86, 275, 1, 'ToFirstPos')
		guiSubautomata5.newGuiNode(8, 0, 247, 92, 0, 'ToSecondPos')
		guiSubautomata5.newGuiNode(9, 0, 491, 303, 0, 'ToThirdPos')
		guiSubautomata5.newGuiNode(10, 0, 281, 455, 0, 'Return')

		guiSubautomata5.newGuiTransition((86, 275), (247, 92), (166, 184), 9, 7, 8)
		guiSubautomata5.newGuiTransition((247, 92), (491, 303), (369, 198), 10, 8, 9)
		guiSubautomata5.newGuiTransition((491, 303), (281, 455), (386, 379), 11, 9, 10)
		guiSubautomata5.newGuiTransition((281, 455), (86, 275), (184, 365), 12, 10, 7)
		guiSubautomataList.append(guiSubautomata5)

		# Creating subAutomata6
		guiSubautomata6 = GuiSubautomata(6,12, self.automataGui)

		guiSubautomata6.newGuiNode(15, 0, 126, 185, 1, 'Descending')
		guiSubautomata6.newGuiNode(16, 0, 350, 190, 0, 'Land')

		guiSubautomata6.newGuiTransition((126, 185), (350, 190), (232, 220), 24, 15, 16)
		guiSubautomataList.append(guiSubautomata6)


		return guiSubautomataList

	def shutDown(self):
		self.run1 = False
		self.run3 = False
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

		self.targetX = 125
		self.targetY = 125
		self.targetZ = 2.5
		self.initPos = (-1, -8.5)
		landingPose = (self.Pose3DPrx.getPose3DData().x, self.Pose3DPrx.getPose3DData().y)
		
		#Minimun errors
		self.minError = 10
		self.minActit = 0.5
		self.minAltit = 0.01
		self.minDist = 0.01
		heighMargin = 1
		
		#Control Variables
		self.heigh = 0
		self.contours = []
		self.monitorComplet = False
		self.xPos = landingPose[0]
		self.yPos = landingPose[1]
		initAngle = None
		self.hasLanded = False
		currentState = "FollowRoad"
		takenOff = False
		
		#Filter Values
		self.hmin = 90
		self.hmax = 97
		self.vmin = 0
		self.vmax = 50
		self.smin = 45
		self.smax = 80
		
		#Control PID
		self.xPid = self.PID(Epsilon=self.minError, Kp=0.01, Ki=0.04, Kd=0.003, Imax=5, Imin=-5)
		self.zPid = self.PID(Epsilon=self.minAltit, Kp=1, Ki=0.02, Kd=0, Imax=5, Imin=-5)
		self.aPid = self.PID(Epsilon=self.minActit, Kp=0.01, Ki=0.04, Kd=0.003, Imax=5, Imin=-5)

		while(self.run1):
			totala = time.time() * 1000000

			# Evaluation if
			if(self.sub1 == "TakeOff"):
				if(takenOff):
					self.sub1 = "HeighControl"
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('HeighControl')

			elif(self.sub1 == "FollowRoad"):
				if((self.droneInPosition(self.initPos, 200)) and (not self.monitorComplet)):
					self.sub1 = "MonitorArea"
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('MonitorArea')

				elif((self.droneInPosition(landingPose, 75)) and (self.monitorComplet)):
					self.sub1 = "Landing"
					self.setVelocity(0,0,0,0)
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('Landing')

				elif(abs(self.targetZ - self.heigh) > heighMargin):
					self.sub1 = "HeighControl"
					currentState = "FollowRoad"
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('HeighControl')

			elif(self.sub1 == "MonitorArea"):
				if(self.monitorComplet):
					self.sub1 = "TurnAround"
					self.setVelocity(0, 0, 0, 0)
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('TurnAround')

				elif(abs(self.targetZ - self.heigh) > heighMargin):
					self.sub1 = "HeighControl"
					currentState = "MonitorArea"
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('HeighControl')

			elif(self.sub1 == "TurnAround"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 2.5):
						self.sub1 = "FollowRoad"
						t_activated = False
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('FollowRoad')

			elif(self.sub1 == "Landing"):
				if(self.hasLanded):
					self.sub1 = "END"
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('END')

			elif(self.sub1 == "HeighControl"):
				if((abs(self.targetZ - self.heigh) < self.minAltit) and (currentState == "FollowRoad")):
					self.sub1 = "FollowRoad"
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('FollowRoad')

				elif((abs(self.targetZ - self.heigh) < self.minAltit) and (currentState == "MonitorArea")):
					self.sub1 = "MonitorArea"
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('MonitorArea')


			# Actuation if
			if(self.sub1 == "TakeOff"):
				#Taking Off
				self.ExtraPrx.takeoff()
				takenOff = True
			elif(self.sub1 == "FollowRoad"):
				lastState = "FollowRoad"
				
				#Get and prepare image
				inImg = self.getImage()
				softenedImg = cv2.bilateralFilter(inImg, 9, 75, 75)
				hsvImg = cv2.cvtColor(softenedImg, cv2.COLOR_BGR2HSV)
				
				#Get threshold image
				minValues = numpy.array([self.hmin, self.vmin, self.smin])
				maxValues = numpy.array([self.hmax, self.vmax, self.smax])
				thresholdImg = cv2.inRange(hsvImg, minValues, maxValues)
				
				#Get contours
				self.contours, hierarchy = cv2.findContours(thresholdImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
				
				#Update Heigh
				self.heigh = self.Pose3DPrx.getPose3DData().z
			elif(self.sub1 == "TurnAround"):
				self.setVelocity(0, 0, 0, 1)
				pose= self.Pose3DPrx.getPose3DData()
				print "q0", pose.q0, "q1",pose.q1, "q2",pose.q2, "q3",pose.q3
			elif(self.sub1 == "END"):
				print "SHUT DOWN"
				self.shutDown()
			elif(self.sub1 == "HeighControl"):
				#Controling heigh
				self.heigh = self.Pose3DPrx.getPose3DData().z
				zVel = self.zPid.process(self.targetZ - self.heigh)
				self.setVelocity(0, 0, zVel, 0)
				print "Heigh:", self.heigh
				print "Vel:", zVel

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

			if(self.sub1 == "FollowRoad"):
				if ((self.sub3 == "FindRoad_ghost") or (self.sub3 == "FollowingRoad_ghost")):
					ghostStateIndex = self.StatesSub3.index(self.sub3)
					self.sub3 = self.StatesSub3[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub3 == "FindRoad"):
					if(self.contours):
						self.sub3 = "FollowingRoad"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('FollowingRoad')

				elif(self.sub3 == "FollowingRoad"):
					if(not self.contours):
						self.sub3 = "FindRoad"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('FindRoad')


				# Actuation if
				if(self.sub3 == "FindRoad"):
					self.setVelocity(0, 0, 0.75, 0)
					print "Road lost"
				elif(self.sub3 == "FollowingRoad"):
					contour = max(self.contours, key=cv2.contourArea)
					try:
						(x, y), radius = cv2.minEnclosingCircle(contour)
						center = (int(x), int(y))
						ellipse = cv2.fitEllipse(contour)
						inclination = ellipse[2]
					
						if inclination < 90:
							yAngle = -inclination
						else:
							yAngle = 180 - inclination
					
						avel = self.aPid.process(yAngle)
						xError = self.targetX - center[0]
						xvel = self.xPid.process(xError)
						speed = max((self.targetX - pow(1.09, abs(xError)))/125.,0)
						
						self.setVelocity(xvel, speed, 0, avel)
					except:
						print "EXCEPTION FOUND"
						self.contours = []
					
					self.xPos = self.Pose3DPrx.getPose3DData().x
					self.yPos = self.Pose3DPrx.getPose3DData().y
					print "Xpos:", self.xPos, "Ypos:", self.yPos
			else:
				if(self.sub3 == "FindRoad"):
					ghostStateIndex = self.StatesSub3.index(self.sub3) + 1
					self.sub3 = self.StatesSub3[ghostStateIndex]
				elif(self.sub3 == "FollowingRoad"):
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


	def subautomata5(self):
		self.run5 = True
		cycle = 100
		t_activated = False
		t_fin = 0


		firstPos = (10, -20)
		secondPos = (5, -30)
		thirdPos = (-10, -20)
		
		#Same value in the parent subautomata
		self.minDist = 0.01
		
		#Control PID
		xDistPid = self.PID(self.minDist, 1, 0.001, 0.001, 5, -5)
		yDistPid = self.PID(self.minDist, 1, 0.001, 0.001, 5, -5)

		while(self.run5):
			totala = time.time() * 1000000

			if(self.sub1 == "MonitorArea"):
				if ((self.sub5 == "ToFirstPos_ghost") or (self.sub5 == "ToSecondPos_ghost") or (self.sub5 == "ToThirdPos_ghost") or (self.sub5 == "Return_ghost")):
					ghostStateIndex = self.StatesSub5.index(self.sub5)
					self.sub5 = self.StatesSub5[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub5 == "ToFirstPos"):
					if(self.droneInPosition(firstPos, 3)):
						self.sub5 = "ToSecondPos"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('ToSecondPos')

				elif(self.sub5 == "ToSecondPos"):
					if(self.droneInPosition(secondPos, 3)):
						self.sub5 = "ToThirdPos"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('ToThirdPos')

				elif(self.sub5 == "ToThirdPos"):
					if(self.droneInPosition(thirdPos, 3)):
						self.sub5 = "Return"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('Return')

				elif(self.sub5 == "Return"):
					if(self.droneInPosition(self.initPos, 3)):
						self.sub5 = "ToFirstPos"
						self.monitorComplet = True
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('ToFirstPos')


				# Actuation if
				if(self.sub5 == "ToFirstPos"):
					self.xPos = self.Pose3DPrx.getPose3DData().x
					self.yPos = self.Pose3DPrx.getPose3DData().y
					
					xError = firstPos[0] - self.xPos
					xVel = xDistPid.process(xError)
					yError = firstPos[1] - self.yPos
					yVel = yDistPid.process(yError)
					
					print "Xerror:", xError, "Yerror:", yError
					print "Xvel:", xVel, "Yvel:", -yVel
					
					self.setVelocity(xVel, -yVel, 0, 0)
				elif(self.sub5 == "ToSecondPos"):
					self.xPos = self.Pose3DPrx.getPose3DData().x
					self.yPos = self.Pose3DPrx.getPose3DData().y
					
					xError = secondPos[0] - self.xPos
					xVel = xDistPid.process(xError)
					yError = secondPos[1] - self.yPos
					yVel = yDistPid.process(yError)
					
					print "xError:",xError, "Yerror:", yError
					print "Xvel:", xVel, "Yvel:", -yVel
					
					self.setVelocity(xVel, -yVel, 0, 0)
				elif(self.sub5 == "ToThirdPos"):
					self.xPos = self.Pose3DPrx.getPose3DData().x
					self.yPos = self.Pose3DPrx.getPose3DData().y
					
					xError = thirdPos[0] - self.xPos
					xVel = xDistPid.process(xError)
					yError = thirdPos[1] - self.yPos
					yVel = yDistPid.process(yError)
					
					print "Xerror:", xError, "Yerror:", yError
					print "Xvel:", xVel, "Yvel:", yVel
					print "Xvel:", xVel, "Yvel:", -yVel
					
					self.setVelocity(xVel, -yVel, 0, 0)
				elif(self.sub5 == "Return"):
					self.xPos = self.Pose3DPrx.getPose3DData().x
					self.yPos = self.Pose3DPrx.getPose3DData().y
					
					xError = self.initPos[0] - self.xPos
					xVel = xDistPid.process(xError)
					yError = self.initPos[1] - self.yPos
					yVel = yDistPid.process(yError)
					
					print "Xerror:", xError, "Yerror:", yError
					print "Xvel:", xVel, "Yvel:", -yVel
					
					self.setVelocity(xVel, -yVel, 0, 0)
			else:
				if(self.sub5 == "ToFirstPos"):
					ghostStateIndex = self.StatesSub5.index(self.sub5) + 1
					self.sub5 = self.StatesSub5[ghostStateIndex]
				elif(self.sub5 == "ToSecondPos"):
					ghostStateIndex = self.StatesSub5.index(self.sub5) + 1
					self.sub5 = self.StatesSub5[ghostStateIndex]
				elif(self.sub5 == "ToThirdPos"):
					ghostStateIndex = self.StatesSub5.index(self.sub5) + 1
					self.sub5 = self.StatesSub5[ghostStateIndex]
				elif(self.sub5 == "Return"):
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


		targetZDescend = 0.5

		while(self.run6):
			totala = time.time() * 1000000

			if(self.sub1 == "Landing"):
				if ((self.sub6 == "Descending_ghost") or (self.sub6 == "Land_ghost")):
					ghostStateIndex = self.StatesSub6.index(self.sub6)
					self.sub6 = self.StatesSub6[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub6 == "Descending"):
					if(abs(targetZDescend - self.heigh) < self.minAltit):
						self.sub6 = "Land"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('Land')


				# Actuation if
				if(self.sub6 == "Descending"):
					#Controling heigh
					self.heigh = self.Pose3DPrx.getPose3DData().z
					zVel = self.zPid.process(targetZDescend - self.heigh)
					self.setVelocity(0, 0, zVel, 0)
					print "Heigh:", self.heigh
				elif(self.sub6 == "Land"):
					self.setVelocity(0,0,0,0)
					if not self.hasLanded:
						self.ExtraPrx.land()
						self.hasLanded =True
			else:
				if(self.sub6 == "Descending"):
					ghostStateIndex = self.StatesSub6.index(self.sub6) + 1
					self.sub6 = self.StatesSub6[ghostStateIndex]
				elif(self.sub6 == "Land"):
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

		# Contact to Pose3D
		Pose3D = self.ic.propertyToProxy('automata.Pose3D.Proxy')
		if(not Pose3D):
			raise Exception('could not create proxy with Pose3D')
		self.Pose3DPrx = Pose3DPrx.checkedCast(Pose3D)
		if(not self.Pose3DPrx):
			raise Exception('invalid proxy automata.Pose3D.Proxy')
		print 'Pose3D connected'

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
		self.t3.join()
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
