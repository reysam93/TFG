#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
import sys, signal
sys.path.append('/home/samuelvm/TFG/visualHFSM') #Need to find a better way...
import traceback, threading, time
from automatagui import AutomataGui, QtGui
import jderobot

from jderobot import CameraPrx
from jderobot import Pose3DPrx
from jderobot import CMDVelPrx
from jderobot import ArDroneExtraPrx
from jderobot import NavdataPrx

def finished():
	print "FINISHED!"

class Automata():

	def __init__(self):
		self.lock = threading.Lock()
		self.StatesSub1 = [
			"TakeOff",
			"Stabilizing1",
			"GoFront",
			"Stoping",
			"Landing",
			"Stabilizing2",
		]

		self.sub1 = "TakeOff"
		self.run1 = True

	def createAutomata(self):
		guiSubautomataList = []

		# Creating subAutomata1
		guiSubautomata1 = automatagui.GuiSubautomata(1,0)

		guiSubautomata1.newGuiNode(1, 0, 61, 101, 1, 'TakeOff')
		guiSubautomata1.newGuiNode(2, 0, 283, 75, 0, 'Stabilizing1')
		guiSubautomata1.newGuiNode(3, 0, 497, 130, 0, 'GoFront')
		guiSubautomata1.newGuiNode(4, 0, 488, 320, 0, 'Stoping')
		guiSubautomata1.newGuiNode(5, 0, 250, 408, 0, 'Landing')
		guiSubautomata1.newGuiNode(6, 0, 66, 283, 0, 'Stabilizing2')

		orig11 = automatagui.Point(61, 101)
		dest11 = automatagui.Point(283, 75)
		mid11 = automatagui.Point(38, 179)
		guiSubautomata1.newGuiTransition(orig11, dest11, mid11, 1, 1, 2)

		orig12 = automatagui.Point(283, 75)
		dest12 = automatagui.Point(497, 130)
		mid12 = automatagui.Point(413, 79)
		guiSubautomata1.newGuiTransition(orig12, dest12, mid12, 2, 2, 3)

		orig13 = automatagui.Point(497, 130)
		dest13 = automatagui.Point(488, 320)
		mid13 = automatagui.Point(570, 239)
		guiSubautomata1.newGuiTransition(orig13, dest13, mid13, 3, 3, 4)

		orig14 = automatagui.Point(488, 320)
		dest14 = automatagui.Point(250, 408)
		mid14 = automatagui.Point(410, 411)
		guiSubautomata1.newGuiTransition(orig14, dest14, mid14, 4, 4, 5)

		orig16 = automatagui.Point(250, 408)
		dest16 = automatagui.Point(66, 283)
		mid16 = automatagui.Point(152, 338)
		guiSubautomata1.newGuiTransition(orig16, dest16, mid16, 6, 5, 6)

		orig11 = automatagui.Point(66, 283)
		dest11 = automatagui.Point(61, 101)
		mid11 = automatagui.Point(38, 179)
		guiSubautomata1.newGuiTransition(orig11, dest11, mid11, 1, 6, 1)

		guiSubautomataList.append(guiSubautomata1);

		return guiSubautomataList

	def shutDown(self):
		self.run1 = False

	def runGui(self):
		app = QtGui.QApplication(sys.argv)
		self.automataGui = AutomataGui()
		self.automataGui.setAutomata(self.createAutomata())
		self.automataGui.loadAutomata()
		self.automataGui.show()
		app.exec_()

	def subautomata1(self):
		run = True
		cycle = 100
		t_activated = False

		hasTakenOff = False
		hasLanded = False

		while(run):
			totala = time.time() * 1000000

			# Evaluation if
			if(self.sub1 == "TakeOff"):
				if(hasTakenOff):
					self.sub1 = "Stabilizing1"
					print "Going to Stabilizing"

			elif(self.sub1 == "Stabilizing1"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 1.5):
						self.sub1 = "GoFront"
						t_activated = False
						print "going to GoFront"

			elif(self.sub1 == "GoFront"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 3):
						self.sub1 = "Stoping"
						t_activated = False
						print "going to Stoping"

			elif(self.sub1 == "Stoping"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 3.5):
						self.sub1 = "Landing"
						t_activated = False
						print "going to Land"

			elif(self.sub1 == "Landing"):
				if(hasLanded):
					self.sub1 = "Stabilizing2"


			elif(self.sub1 == "Stabilizing2"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 3):
						self.sub1 = "TakeOff"
						t_activated = False
						print "Restarting"


			# Actuation if
			if(self.sub1 == "TakeOff"):
				print "Taking Off"
				self.lock.acquire()
				#self.extraPrx.takeoff()
				self.lock.release()
				hasTakenOff = True
			elif(self.sub1 == "Stabilizing1"):
				print "Stabilizing"
			elif(self.sub1 == "GoFront"):
				cmd = jderobot.CMDVelData()
				cmd.linearX = 1
				cmd.linearY = 0
				cmd.linearZ = 0
				self.lock.acquire()
				self.cmdPrx.setCMDVelData(cmd)
				self.lock.release()
			elif(self.sub1 == "Stoping"):
				cmd = jderobot.CMDVelData()
				cmd.linearX = 0
				cmd.linearY = 0
				cmd.linearZ = 0
				self.lock.acquire()
				self.cmdPrx.setCMDVelData(cmd)
				self.lock.release()
				print "Stoping"
			elif(self.sub1 == "Landing"):
				print "Landing"
				self.lock.acquire()
				#self.extraPrx.land()
				self.lock.release()
				hasLanded = True
			elif(self.sub1 == "Stabilizing2"):
				finished()

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

		# Contact to camera
		camera = self.ic.propertyToProxy('automata.Camera.Proxy')
		if(not camera):
			raise Exception('could not create proxy with camera')
		self.cameraPrx = CameraPrx.checkedCast(camera)
		if(not self.cameraPrx):
			raise Exception('invalid proxy automata.Camera.Proxy')
		print 'camera connected'

		# Contact to pose3d
		pose3d = self.ic.propertyToProxy('automata.Pose3D.Proxy')
		if(not pose3d):
			raise Exception('could not create proxy with pose3d')
		self.pose3dPrx = Pose3DPrx.checkedCast(pose3d)
		if(not self.pose3dPrx):
			raise Exception('invalid proxy automata.Pose3D.Proxy')
		print 'pose3d connected'

		# Contact to cmd
		cmd = self.ic.propertyToProxy('automata.CMDVel.Proxy')
		if(not cmd):
			raise Exception('could not create proxy with cmd')
		self.cmdPrx = CMDVelPrx.checkedCast(cmd)
		if(not self.cmdPrx):
			raise Exception('invalid proxy automata.CMDVel.Proxy')
		print 'cmd connected'

		# Contact to extra
		extra = self.ic.propertyToProxy('automata.ArDroneExtra.Proxy')
		if(not extra):
			raise Exception('could not create proxy with extra')
		self.extraPrx = ArDroneExtraPrx.checkedCast(extra)
		if(not self.extraPrx):
			raise Exception('invalid proxy automata.ArDroneExtra.Proxy')
		print 'extra connected'

		# Contact to navdata
		navdata = self.ic.propertyToProxy('automata.Navdata.Proxy')
		if(not navdata):
			raise Exception('could not create proxy with navdata')
		self.navdataPrx = NavdataPrx.checkedCast(navdata)
		if(not self.navdataPrx):
			raise Exception('invalid proxy automata.Navdata.Proxy')
		print 'navdata connected'


	def destroyIc(self):
		if(self.ic):
			self.ic.destroy()


	def start(self):
		self.guiThread = threading.Thread(target=self.runGui)
		self.guiThread.start()

		self.t1 = threading.Thread(target=self.subautomata1)
		#self.t1.start()


	def join(self):
		self.guiThread.join()
		self.t1.join()


if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	automata = Automata()
	try:
		#automata.connectToProxys()
		automata.start()
		automata.join()

		sys.exit(0)
	except:
		traceback.print_exc()
		#automata.destroyIc()
		sys.exit(-1)
