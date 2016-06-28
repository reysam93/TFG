#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
import sys, signal
sys.path.append('/home/samuelvm/TFG/visualHFSM') #Need to find a better way...
import traceback, threading, time
from automatagui import AutomataGui, QtGui, GuiSubautomata
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

		self.StatesSub3 = [
			"A",
			"A_ghost",
			"B",
			"B_ghost",
		]

		self.StatesSub5 = [
			"C",
			"C_ghost",
		]

		self.sub1 = "TakeOff"
		self.run1 = True
		self.sub3 = "A_ghost"
		self.run3 = True
		self.sub5 = "C_ghost"
		self.run5 = True

	def createAutomata(self):
		guiSubautomataList = []

		# Creating subAutomata1
		guiSubautomata1 = GuiSubautomata(1,0, self.automataGui)

		guiSubautomata1.newGuiNode(1, 3, 61, 101, 1, 'TakeOff')
		guiSubautomata1.newGuiNode(2, 0, 283, 75, 0, 'Stabilizing1')
		guiSubautomata1.newGuiNode(3, 0, 497, 130, 0, 'GoFront')
		guiSubautomata1.newGuiNode(4, 0, 489, 320, 0, 'Stoping')
		guiSubautomata1.newGuiNode(5, 0, 250, 408, 0, 'Landing')
		guiSubautomata1.newGuiNode(6, 0, 66, 283, 0, 'Stabilizing2')

		guiSubautomata1.newGuiTransition((61, 101), (283, 75), (9, 212), 1, 1, 2)
		guiSubautomata1.newGuiTransition((283, 75), (497, 130), (413, 79), 2, 2, 3)
		guiSubautomata1.newGuiTransition((497, 130), (489, 320), (570, 239), 3, 3, 4)
		guiSubautomata1.newGuiTransition((489, 320), (250, 408), (410, 411), 4, 4, 5)
		guiSubautomata1.newGuiTransition((250, 408), (66, 283), (152, 338), 6, 5, 6)
		guiSubautomata1.newGuiTransition((66, 283), (61, 101), (9, 212), 1, 6, 1)
		guiSubautomataList.append(guiSubautomata1)

		# Creating subAutomata3
		guiSubautomata3 = GuiSubautomata(3,1, self.automataGui)

		guiSubautomata3.newGuiNode(7, 0, 175, 146, 1, 'A')
		guiSubautomata3.newGuiNode(8, 5, 468, 201, 0, 'B')

		guiSubautomata3.newGuiTransition((175, 146), (468, 201), (348, 79), 1, 7, 8)
		guiSubautomata3.newGuiTransition((468, 201), (175, 146), (303, 215), 2, 8, 7)
		guiSubautomataList.append(guiSubautomata3)

		# Creating subAutomata5
		guiSubautomata5 = GuiSubautomata(5,3, self.automataGui)

		guiSubautomata5.newGuiNode(9, 0, 70, 146, 1, 'C')

		guiSubautomata5.newGuiTransition((70, 146), (70, 146), (70, 186), 3, 9, 9)
		guiSubautomataList.append(guiSubautomata5)


		return guiSubautomataList

	def shutDown(self):
		self.run1 = False
		self.run3 = False
		self.run5 = False

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
				self.automataGui.notifySetNodeAsActive('Stabilizing1')

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
						self.automataGui.notifySetNodeAsActive('GoFront')

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
						self.automataGui.notifySetNodeAsActive('Stoping')

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
						self.automataGui.notifySetNodeAsActive('Landing')

			elif(self.sub1 == "Landing"):
				if(hasLanded):
					self.sub1 = "Stabilizing2"

				self.automataGui.notifySetNodeAsActive('Stabilizing2')

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
						self.automataGui.notifySetNodeAsActive('TakeOff')


			# Actuation if
			if(self.sub1 == "TakeOff"):
				print "Taking Off"
				self.lock.acquire()
				self.extraPrx.takeoff()
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
				self.extraPrx.land()
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


	def subautomata3(self):
		run = True
		cycle = 100
		t_activated = False
		t_fin = 0

		t_A_max = 0.023
		t_B_max = 0.055


		while(run):
			totala = time.time() * 1000000

			if(self.sub1 == "TakeOff"):
				if ((self.sub3 == "A_ghost") or (self.sub3 == "B_ghost")):
					ghostStateIndex = self.StatesSub3.index(self.sub3)
					self.sub3 = self.StatesSub3[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub3 == "A"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_A_max):
							self.sub3 = "B"
							t_activated = False
							self.automataGui.notifySetNodeAsActive('B')
							t_A_max = 0.023

				elif(self.sub3 == "B"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_B_max):
							self.sub3 = "A"
							t_activated = False
							self.automataGui.notifySetNodeAsActive('A')
							t_B_max = 0.055


				# Actuation if
				if(self.sub3 == "A"):
					print "A"
				elif(self.sub3 == "B"):
					print "B"
			else:
				if(self.sub3 == "A"):
					t_A_max = 0.023 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub3.index(self.sub3) + 1
					sub3 = self.StatesSub3[ghostStateIndex]
				elif(self.sub3 == "B"):
					t_B_max = 0.055 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub3.index(self.sub3) + 1
					sub3 = self.StatesSub3[ghostStateIndex]

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
		run = True
		cycle = 100
		t_activated = False

		t_C_max = 0.567


		while(run):
			totala = time.time() * 1000000

			if(self.sub3 == "B"):
				if ((self.sub5 == "C_ghost")):
					ghostStateIndex = self.StatesSub5.index(self.sub5)
					self.sub5 = self.StatesSub5[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub5 == "C"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_C_max):
							self.sub5 = "C"
							t_activated = False
							self.automataGui.notifySetNodeAsActive('C')
							t_C_max = 0.567


				# Actuation if
				if(self.sub5 == "C"):
					print "C"
			else:
				if(self.sub5 == "C"):
					t_C_max = 0.567 - (t_fin - t_ini)
					ghostStateIndex = self.StateSub5.index(self.sub5) + 1
					sub5 = self.StatesSub5[ghostStateIndex]

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
		time.sleep(1)


		self.t1 = threading.Thread(target=self.subautomata1)
		self.t1.start()
		self.t3 = threading.Thread(target=self.subautomata3)
		self.t3.start()
		self.t5 = threading.Thread(target=self.subautomata5)
		self.t5.start()


	def join(self):
		self.guiThread.join()
		self.t1.join()
		self.t3.join()
		self.t5.join()


if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	automata = Automata()
	try:
		automata.connectToProxys()
		automata.start()
		automata.join()

		sys.exit(0)
	except:
		traceback.print_exc()
		automata.destroyIc()
		sys.exit(-1)
