#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
import sys, signal
sys.path.append('/usr/local/share/jderobot/python/visualHFSM_py')
import traceback, threading, time
from automatagui import AutomataGui, QtGui, GuiSubautomata

import jderobot

from jderobot import Pose3DPrx
from jderobot import CMDVelPrx
from jderobot import ArDroneExtraPrx



















class Automata():

	def __init__(self):
		self.lock = threading.Lock()
		self.displayGui = False
		self.StatesSub1 = [
			"TakeOff",
			"GoFront",
			"DoSquare",
			"Landing",
			"END",
		]

		self.StatesSub2 = [
			"TakingOff",
			"TakingOff_ghost",
			"Stabilizing1",
			"Stabilizing1_ghost",
		]

		self.StatesSub3 = [
			"GoingFront",
			"GoingFront_ghost",
			"Stabilizing2",
			"Stabilizing2_ghost",
			"goneFront",
			"goneFront_ghost",
		]

		self.StatesSub4 = [
			"empty1",
			"empty1_ghost",
			"empty2",
			"empty2_ghost",
		]

		self.StatesSub5 = [
			"DoingRigthSide",
			"DoingRigthSide_ghost",
			"DoingTopSide",
			"DoingTopSide_ghost",
			"DoingLeftSide",
			"DoingLeftSide_ghost",
			"DoingBottomSide",
			"DoingBottomSide_ghost",
		]

		self.StatesSub6 = [
			"GoingToTop",
			"GoingToTop_ghost",
			"StabilizingTop",
			"StabilizingTop_ghost",
			"GoneToTop",
			"GoneToTop_ghost",
		]

		self.StatesSub8 = [
			"GoingToLeft",
			"GoingToLeft_ghost",
			"StabilizingLeft",
			"StabilizingLeft_ghost",
			"GoneToLeft",
			"GoneToLeft_ghost",
		]

		self.StatesSub9 = [
			"GoingToBottom",
			"GoingToBottom_ghost",
			"StabilizingBottom",
			"StabilizingBottom_ghost",
			"GoneToBottom",
			"GoneToBottom_ghost",
		]

		self.StatesSub10 = [
			"GoingToRigth",
			"GoingToRigth_ghost",
			"StabilizingRigth",
			"StabilizingRigth_ghost",
			"GoneToRigth",
			"GoneToRigth_ghost",
		]

		self.sub1 = "TakeOff"
		self.run1 = True
		self.sub2 = "TakingOff_ghost"
		self.run2 = True
		self.sub3 = "GoingFront_ghost"
		self.run3 = True
		self.sub4 = "empty1_ghost"
		self.run4 = True
		self.sub5 = "DoingRigthSide_ghost"
		self.run5 = True
		self.sub6 = "GoingToTop_ghost"
		self.run6 = True
		self.sub8 = "GoingToLeft_ghost"
		self.run8 = True
		self.sub9 = "GoingToBottom_ghost"
		self.run9 = True
		self.sub10 = "GoingToRigth_ghost"
		self.run10 = True

	def startThreads(self):
		self.t1 = threading.Thread(target=self.subautomata1)
		self.t1.start()
		self.t2 = threading.Thread(target=self.subautomata2)
		self.t2.start()
		self.t3 = threading.Thread(target=self.subautomata3)
		self.t3.start()
		self.t4 = threading.Thread(target=self.subautomata4)
		self.t4.start()
		self.t5 = threading.Thread(target=self.subautomata5)
		self.t5.start()
		self.t6 = threading.Thread(target=self.subautomata6)
		self.t6.start()
		self.t8 = threading.Thread(target=self.subautomata8)
		self.t8.start()
		self.t9 = threading.Thread(target=self.subautomata9)
		self.t9.start()
		self.t10 = threading.Thread(target=self.subautomata10)
		self.t10.start()

	def createAutomata(self):
		guiSubautomataList = []

		# Creating subAutomata1
		guiSubautomata1 = GuiSubautomata(1,0, self.automataGui)

		guiSubautomata1.newGuiNode(1, 2, 76, 158, 1, 'TakeOff')
		guiSubautomata1.newGuiNode(5, 3, 323, 136, 0, 'GoFront')
		guiSubautomata1.newGuiNode(14, 5, 587, 181, 0, 'DoSquare')
		guiSubautomata1.newGuiNode(15, 0, 395, 467, 0, 'Landing')
		guiSubautomata1.newGuiNode(16, 0, 89, 421, 0, 'END')

		guiSubautomata1.newGuiTransition((76, 158), (323, 136), (189, 145), 2, 1, 5)
		guiSubautomata1.newGuiTransition((323, 136), (587, 181), (446, 132), 6, 5, 14)
		guiSubautomata1.newGuiTransition((395, 467), (89, 421), (226, 464), 8, 15, 16)
		guiSubautomata1.newGuiTransition((89, 421), (76, 158), (48, 290), 28, 16, 1)
		guiSubautomata1.newGuiTransition((587, 181), (395, 467), (491, 324), 37, 14, 15)
		guiSubautomataList.append(guiSubautomata1)

		# Creating subAutomata2
		guiSubautomata2 = GuiSubautomata(2,1, self.automataGui)

		guiSubautomata2.newGuiNode(2, 0, 106, 141, 1, 'TakingOff')
		guiSubautomata2.newGuiNode(3, 0, 283, 219, 0, 'Stabilizing1')

		guiSubautomata2.newGuiTransition((106, 141), (283, 219), (138, 243), 1, 2, 3)
		guiSubautomata2.newGuiTransition((283, 219), (106, 141), (244, 116), 26, 3, 2)
		guiSubautomataList.append(guiSubautomata2)

		# Creating subAutomata3
		guiSubautomata3 = GuiSubautomata(3,5, self.automataGui)

		guiSubautomata3.newGuiNode(9, 0, 127, 107, 1, 'GoingFront')
		guiSubautomata3.newGuiNode(10, 4, 511, 137, 0, 'Stabilizing2')
		guiSubautomata3.newGuiNode(11, 0, 298, 291, 0, 'goneFront')

		guiSubautomata3.newGuiTransition((127, 107), (511, 137), (319, 123), 2, 9, 10)
		guiSubautomata3.newGuiTransition((511, 137), (298, 291), (405, 214), 3, 10, 11)
		guiSubautomata3.newGuiTransition((298, 291), (127, 107), (212, 199), 27, 11, 9)
		guiSubautomataList.append(guiSubautomata3)

		# Creating subAutomata4
		guiSubautomata4 = GuiSubautomata(4,10, self.automataGui)

		guiSubautomata4.newGuiNode(12, 0, 232, 178, 1, 'empty1')
		guiSubautomata4.newGuiNode(13, 0, 445, 217, 0, 'empty2')

		guiSubautomata4.newGuiTransition((232, 178), (445, 217), (357, 129), 4, 12, 13)
		guiSubautomata4.newGuiTransition((445, 217), (232, 178), (316, 271), 5, 13, 12)
		guiSubautomataList.append(guiSubautomata4)

		# Creating subAutomata5
		guiSubautomata5 = GuiSubautomata(5,14, self.automataGui)

		guiSubautomata5.newGuiNode(17, 6, 465, 388, 1, 'DoingRigthSide')
		guiSubautomata5.newGuiNode(18, 8, 461, 140, 0, 'DoingTopSide')
		guiSubautomata5.newGuiNode(19, 9, 134, 130, 0, 'DoingLeftSide')
		guiSubautomata5.newGuiNode(20, 10, 141, 389, 0, 'DoingBottomSide')

		guiSubautomata5.newGuiTransition((465, 388), (461, 140), (463, 264), 9, 17, 18)
		guiSubautomata5.newGuiTransition((461, 140), (134, 130), (298, 136), 10, 18, 19)
		guiSubautomata5.newGuiTransition((134, 130), (141, 389), (137, 260), 11, 19, 20)
		guiSubautomata5.newGuiTransition((141, 389), (465, 388), (303, 388), 12, 20, 17)
		guiSubautomataList.append(guiSubautomata5)

		# Creating subAutomata6
		guiSubautomata6 = GuiSubautomata(6,17, self.automataGui)

		guiSubautomata6.newGuiNode(21, 0, 352, 452, 1, 'GoingToTop')
		guiSubautomata6.newGuiNode(22, 0, 280, 218, 0, 'StabilizingTop')
		guiSubautomata6.newGuiNode(23, 0, 448, 105, 0, 'GoneToTop')

		guiSubautomata6.newGuiTransition((352, 452), (280, 218), (212, 319), 13, 21, 22)
		guiSubautomata6.newGuiTransition((280, 218), (448, 105), (350, 132), 14, 22, 23)
		guiSubautomata6.newGuiTransition((448, 105), (352, 452), (400, 279), 16, 23, 21)
		guiSubautomataList.append(guiSubautomata6)

		# Creating subAutomata8
		guiSubautomata8 = GuiSubautomata(8,18, self.automataGui)

		guiSubautomata8.newGuiNode(24, 0, 135, 397, 1, 'GoingToLeft')
		guiSubautomata8.newGuiNode(25, 0, 213, 194, 0, 'StabilizingLeft')
		guiSubautomata8.newGuiNode(26, 0, 416, 260, 0, 'GoneToLeft')

		guiSubautomata8.newGuiTransition((135, 397), (213, 194), (174, 295), 17, 24, 25)
		guiSubautomata8.newGuiTransition((213, 194), (416, 260), (314, 227), 18, 25, 26)
		guiSubautomata8.newGuiTransition((416, 260), (135, 397), (275, 328), 19, 26, 24)
		guiSubautomataList.append(guiSubautomata8)

		# Creating subAutomata9
		guiSubautomata9 = GuiSubautomata(9,19, self.automataGui)

		guiSubautomata9.newGuiNode(27, 0, 169, 408, 1, 'GoingToBottom')
		guiSubautomata9.newGuiNode(28, 0, 243, 164, 0, 'StabilizingBottom')
		guiSubautomata9.newGuiNode(29, 0, 418, 355, 0, 'GoneToBottom')

		guiSubautomata9.newGuiTransition((169, 408), (243, 164), (206, 286), 20, 27, 28)
		guiSubautomata9.newGuiTransition((243, 164), (418, 355), (330, 259), 21, 28, 29)
		guiSubautomata9.newGuiTransition((418, 355), (169, 408), (293, 381), 22, 29, 27)
		guiSubautomataList.append(guiSubautomata9)

		# Creating subAutomata10
		guiSubautomata10 = GuiSubautomata(10,20, self.automataGui)

		guiSubautomata10.newGuiNode(31, 0, 121, 361, 1, 'GoingToRigth')
		guiSubautomata10.newGuiNode(32, 0, 231, 110, 0, 'StabilizingRigth')
		guiSubautomata10.newGuiNode(33, 0, 371, 331, 0, 'GoneToRigth')

		guiSubautomata10.newGuiTransition((121, 361), (231, 110), (176, 235), 23, 31, 32)
		guiSubautomata10.newGuiTransition((231, 110), (371, 331), (300, 220), 24, 32, 33)
		guiSubautomata10.newGuiTransition((371, 331), (121, 361), (246, 346), 25, 33, 31)
		guiSubautomataList.append(guiSubautomata10)


		return guiSubautomataList

	def shutDown(self):
		self.run1 = False
		self.run2 = False
		self.run3 = False
		self.run4 = False
		self.run5 = False
		self.run6 = False
		self.run8 = False
		self.run9 = False
		self.run10 = False

	def runGui(self):
		app = QtGui.QApplication(sys.argv)
		self.automataGui = AutomataGui()
		self.automataGui.setAutomata(self.createAutomata())
		self.automataGui.loadAutomata()
		self.startThreads()
		self.automataGui.show()
		app.exec_()

	def subautomata1(self):
		run = True
		cycle = 100
		t_activated = False
		t_fin = 0

		self.goneFront = False
		self.squareDone = False
		self.goneBack = False

		while(run):
			totala = time.time() * 1000000

			# Evaluation if
			if(self.sub1 == "TakeOff"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 3.5):
						self.sub1 = "GoFront"
						t_activated = False
						print "From TakeOff to GoFront"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('GoFront')

			elif(self.sub1 == "GoFront"):
				if(self.goneFront):
					self.sub1 = "DoSquare"
					self.goneFront = False
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('DoSquare')

			elif(self.sub1 == "DoSquare"):
				if(self.squareDone):
					self.sub1 = "Landing"
					self.squareDone = False
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('Landing')

			elif(self.sub1 == "Landing"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 2):
						self.sub1 = "END"
						t_activated = False
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('END')

			elif(self.sub1 == "END"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 3):
						self.sub1 = "TakeOff"
						t_activated = False
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('TakeOff')


			# Actuation if
			if(self.sub1 == "Landing"):
				print "landing"
				self.lock.acquire()
				self.extraPrx.land()
				self.lock.release()
			elif(self.sub1 == "END"):
				print "END"

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
		run = True
		cycle = 100
		t_activated = False
		t_fin = 0

		t_TakingOff_max = 2
		t_Stabilizing1_max = 1.7


		while(run):
			totala = time.time() * 1000000

			if(self.sub1 == "TakeOff"):
				if ((self.sub2 == "TakingOff_ghost") or (self.sub2 == "Stabilizing1_ghost")):
					ghostStateIndex = self.StatesSub2.index(self.sub2)
					self.sub2 = self.StatesSub2[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub2 == "TakingOff"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_TakingOff_max):
							self.sub2 = "Stabilizing1"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('Stabilizing1')
							t_TakingOff_max = 2

				elif(self.sub2 == "Stabilizing1"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_Stabilizing1_max):
							self.sub2 = "TakingOff"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('TakingOff')
							t_Stabilizing1_max = 1.7


				# Actuation if
				if(self.sub2 == "TakingOff"):
					print "Taking Off"
					self.lock.acquire()
					self.extraPrx.takeoff()
					self.lock.release()
			else:
				if(self.sub2 == "TakingOff"):
					t_TakingOff_max = 2 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub2.index(self.sub2) + 1
					self.sub2 = self.StatesSub2[ghostStateIndex]
				elif(self.sub2 == "Stabilizing1"):
					t_Stabilizing1_max = 1.7 - (t_fin - t_ini)
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
		run = True
		cycle = 100
		t_activated = False
		t_fin = 0

		t_Stabilizing2_max = 3
		t_goneFront_max = 0.2

		initPos = 0
		pos = 0

		while(run):
			totala = time.time() * 1000000

			if(self.sub1 == "GoFront"):
				if ((self.sub3 == "GoingFront_ghost") or (self.sub3 == "Stabilizing2_ghost") or (self.sub3 == "goneFront_ghost")):
					ghostStateIndex = self.StatesSub3.index(self.sub3)
					self.sub3 = self.StatesSub3[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub3 == "GoingFront"):
					if(pos - initPos > 300):
						self.sub3 = "Stabilizing2"
						print "300m reached"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('Stabilizing2')

				elif(self.sub3 == "Stabilizing2"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_Stabilizing2_max):
							self.sub3 = "goneFront"
							t_activated = False
							print "from stabilizing2 to GoneFront"
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('goneFront')
							t_Stabilizing2_max = 3

				elif(self.sub3 == "goneFront"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_goneFront_max):
							self.sub3 = "GoingFront"
							t_activated = False
							initPos = 0
							pos = 0
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('GoingFront')
							t_goneFront_max = 0.2


				# Actuation if
				if(self.sub3 == "GoingFront"):
					pos = self.pose3dPrx.getPose3DData().x * 100
					
					if initPos == 0:
						initPos = self.pose3dPrx.getPose3DData().x * 100
					
					print "pos:", pos, "init:", initPos
					print "distancia", pos - initPos
					
					cmd = jderobot.CMDVelData()
					cmd.linearX = 1
					cmd.linearY = 0
					cmd.linearZ = 0
					self.lock.acquire()
					self.cmdVelPrx.setCMDVelData(cmd)
					self.lock.release()
				elif(self.sub3 == "Stabilizing2"):
					cmd.linearX = 0
					cmd.linearY = 0
					cmd.linearZ = 0
					self.lock.acquire()
					self.cmdVelPrx.setCMDVelData(cmd)
					self.lock.release()
				elif(self.sub3 == "goneFront"):
					self.goneFront = True
			else:
				if(self.sub3 == "GoingFront"):
					ghostStateIndex = self.StatesSub3.index(self.sub3) + 1
					self.sub3 = self.StatesSub3[ghostStateIndex]
				elif(self.sub3 == "Stabilizing2"):
					t_Stabilizing2_max = 3 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub3.index(self.sub3) + 1
					self.sub3 = self.StatesSub3[ghostStateIndex]
				elif(self.sub3 == "goneFront"):
					t_goneFront_max = 0.2 - (t_fin - t_ini)
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
		run = True
		cycle = 100
		t_activated = False
		t_fin = 0

		t_empty1_max = 0.8
		t_empty2_max = 0.8


		while(run):
			totala = time.time() * 1000000

			if(self.sub3 == "Stabilizing2"):
				if ((self.sub4 == "empty1_ghost") or (self.sub4 == "empty2_ghost")):
					ghostStateIndex = self.StatesSub4.index(self.sub4)
					self.sub4 = self.StatesSub4[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub4 == "empty1"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_empty1_max):
							self.sub4 = "empty2"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('empty2')
							t_empty1_max = 0.8

				elif(self.sub4 == "empty2"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_empty2_max):
							self.sub4 = "empty1"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('empty1')
							t_empty2_max = 0.8


				# Actuation if
			else:
				if(self.sub4 == "empty1"):
					t_empty1_max = 0.8 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub4.index(self.sub4) + 1
					self.sub4 = self.StatesSub4[ghostStateIndex]
				elif(self.sub4 == "empty2"):
					t_empty2_max = 0.8 - (t_fin - t_ini)
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
		run = True
		cycle = 100
		t_activated = False
		t_fin = 0


		self.goneToTop = False
		self.goneToLeft = False
		self.goneToBottom = False
		self.goneToRigth = False

		while(run):
			totala = time.time() * 1000000

			if(self.sub1 == "DoSquare"):
				if ((self.sub5 == "DoingRigthSide_ghost") or (self.sub5 == "DoingTopSide_ghost") or (self.sub5 == "DoingLeftSide_ghost") or (self.sub5 == "DoingBottomSide_ghost")):
					ghostStateIndex = self.StatesSub5.index(self.sub5)
					self.sub5 = self.StatesSub5[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub5 == "DoingRigthSide"):
					if(self.goneToTop):
						self.sub5 = "DoingTopSide"
						print "Rigth Done"
						self.goneToTop = False
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('DoingTopSide')

				elif(self.sub5 == "DoingTopSide"):
					if(self.goneToLeft):
						self.sub5 = "DoingLeftSide"
						print "Left done"
						self.goneToLeft = False
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('DoingLeftSide')

				elif(self.sub5 == "DoingLeftSide"):
					if(self.goneToBottom):
						self.sub5 = "DoingBottomSide"
						print "Left done"
						self.goneToBottom = False
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('DoingBottomSide')

				elif(self.sub5 == "DoingBottomSide"):
					if(self.goneToRigth):
						self.sub5 = "DoingRigthSide"
						
						
						self.squareDone = True
						print "Bottom done"
						self.goneToRigth = False
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('DoingRigthSide')


				# Actuation if
				if(self.sub5 == "DoingRigthSide"):
					print "Doing Rigth Side"
				elif(self.sub5 == "DoingTopSide"):
					print "Doing Top Side"
				elif(self.sub5 == "DoingLeftSide"):
					print "Doing Left Side"
				elif(self.sub5 == "DoingBottomSide"):
					print "Doing Bottom Side"
			else:
				if(self.sub5 == "DoingRigthSide"):
					ghostStateIndex = self.StatesSub5.index(self.sub5) + 1
					self.sub5 = self.StatesSub5[ghostStateIndex]
				elif(self.sub5 == "DoingTopSide"):
					ghostStateIndex = self.StatesSub5.index(self.sub5) + 1
					self.sub5 = self.StatesSub5[ghostStateIndex]
				elif(self.sub5 == "DoingLeftSide"):
					ghostStateIndex = self.StatesSub5.index(self.sub5) + 1
					self.sub5 = self.StatesSub5[ghostStateIndex]
				elif(self.sub5 == "DoingBottomSide"):
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
		run = True
		cycle = 100
		t_activated = False
		t_fin = 0

		t_GoingToTop_max = 3
		t_StabilizingTop_max = 2
		t_GoneToTop_max = 0.1


		while(run):
			totala = time.time() * 1000000

			if(self.sub5 == "DoingRigthSide"):
				if ((self.sub6 == "GoingToTop_ghost") or (self.sub6 == "StabilizingTop_ghost") or (self.sub6 == "GoneToTop_ghost")):
					ghostStateIndex = self.StatesSub6.index(self.sub6)
					self.sub6 = self.StatesSub6[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub6 == "GoingToTop"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_GoingToTop_max):
							self.sub6 = "StabilizingTop"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('StabilizingTop')
							t_GoingToTop_max = 3

				elif(self.sub6 == "StabilizingTop"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_StabilizingTop_max):
							self.sub6 = "GoneToTop"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('GoneToTop')
							t_StabilizingTop_max = 2

				elif(self.sub6 == "GoneToTop"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_GoneToTop_max):
							self.sub6 = "GoingToTop"
							t_activated = False
							self.GoneToTop = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('GoingToTop')
							t_GoneToTop_max = 0.1


				# Actuation if
				if(self.sub6 == "GoingToTop"):
					cmd = jderobot.CMDVelData()
					cmd.linearX = 0.75
					cmd.linearY = 0
					cmd.linearZ = 0
					self.lock.acquire()
					self.cmdVelPrx.setCMDVelData(cmd)
					self.lock.release()
				elif(self.sub6 == "StabilizingTop"):
					cmd.linearX = 0
					cmd.linearY = 0
					cmd.linearZ = 0
					self.lock.acquire()
					self.cmdVelPrx.setCMDVelData(cmd)
					self.lock.release()
				elif(self.sub6 == "GoneToTop"):
					self.goneToTop = True
			else:
				if(self.sub6 == "GoingToTop"):
					t_GoingToTop_max = 3 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub6.index(self.sub6) + 1
					self.sub6 = self.StatesSub6[ghostStateIndex]
				elif(self.sub6 == "StabilizingTop"):
					t_StabilizingTop_max = 2 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub6.index(self.sub6) + 1
					self.sub6 = self.StatesSub6[ghostStateIndex]
				elif(self.sub6 == "GoneToTop"):
					t_GoneToTop_max = 0.1 - (t_fin - t_ini)
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


	def subautomata8(self):
		run = True
		cycle = 100
		t_activated = False
		t_fin = 0

		t_GoingToLeft_max = 3
		t_StabilizingLeft_max = 2
		t_GoneToLeft_max = 0.1


		while(run):
			totala = time.time() * 1000000

			if(self.sub5 == "DoingTopSide"):
				if ((self.sub8 == "GoingToLeft_ghost") or (self.sub8 == "StabilizingLeft_ghost") or (self.sub8 == "GoneToLeft_ghost")):
					ghostStateIndex = self.StatesSub8.index(self.sub8)
					self.sub8 = self.StatesSub8[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub8 == "GoingToLeft"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_GoingToLeft_max):
							self.sub8 = "StabilizingLeft"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('StabilizingLeft')
							t_GoingToLeft_max = 3

				elif(self.sub8 == "StabilizingLeft"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_StabilizingLeft_max):
							self.sub8 = "GoneToLeft"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('GoneToLeft')
							t_StabilizingLeft_max = 2

				elif(self.sub8 == "GoneToLeft"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_GoneToLeft_max):
							self.sub8 = "GoingToLeft"
							t_activated = False
							self.goneToLeft = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('GoingToLeft')
							t_GoneToLeft_max = 0.1


				# Actuation if
				if(self.sub8 == "GoingToLeft"):
					cmd = jderobot.CMDVelData()
					cmd.linearX = 0
					cmd.linearY = 0.75
					cmd.linearZ = 0
					self.lock.acquire()
					self.cmdVelPrx.setCMDVelData(cmd)
					self.lock.release()
				elif(self.sub8 == "StabilizingLeft"):
					cmd = jderobot.CMDVelData()
					cmd.linearX = 0
					cmd.linearY = 0
					cmd.linearZ = 0
					self.lock.acquire()
					self.cmdVelPrx.setCMDVelData(cmd)
					self.lock.release()
				elif(self.sub8 == "GoneToLeft"):
					self.goneToLeft = True
			else:
				if(self.sub8 == "GoingToLeft"):
					t_GoingToLeft_max = 3 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub8.index(self.sub8) + 1
					self.sub8 = self.StatesSub8[ghostStateIndex]
				elif(self.sub8 == "StabilizingLeft"):
					t_StabilizingLeft_max = 2 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub8.index(self.sub8) + 1
					self.sub8 = self.StatesSub8[ghostStateIndex]
				elif(self.sub8 == "GoneToLeft"):
					t_GoneToLeft_max = 0.1 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub8.index(self.sub8) + 1
					self.sub8 = self.StatesSub8[ghostStateIndex]

			totalb = time.time() * 1000000
			msecs = (totalb - totala) / 1000;
			if(msecs < 0 or msecs > cycle):
				msecs = cycle
			else:
				msecs = cycle - msecs

			time.sleep(msecs / 1000)
			if(msecs < 33 ):
				time.sleep(33 / 1000);


	def subautomata9(self):
		run = True
		cycle = 100
		t_activated = False
		t_fin = 0

		t_GoingToBottom_max = 3
		t_StabilizingBottom_max = 2
		t_GoneToBottom_max = 0.1


		while(run):
			totala = time.time() * 1000000

			if(self.sub5 == "DoingLeftSide"):
				if ((self.sub9 == "GoingToBottom_ghost") or (self.sub9 == "StabilizingBottom_ghost") or (self.sub9 == "GoneToBottom_ghost")):
					ghostStateIndex = self.StatesSub9.index(self.sub9)
					self.sub9 = self.StatesSub9[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub9 == "GoingToBottom"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_GoingToBottom_max):
							self.sub9 = "StabilizingBottom"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('StabilizingBottom')
							t_GoingToBottom_max = 3

				elif(self.sub9 == "StabilizingBottom"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_StabilizingBottom_max):
							self.sub9 = "GoneToBottom"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('GoneToBottom')
							t_StabilizingBottom_max = 2

				elif(self.sub9 == "GoneToBottom"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_GoneToBottom_max):
							self.sub9 = "GoingToBottom"
							t_activated = False
							self.goneToBottom = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('GoingToBottom')
							t_GoneToBottom_max = 0.1


				# Actuation if
				if(self.sub9 == "GoingToBottom"):
					cmd = jderobot.CMDVelData()
					cmd.linearX = -0.75
					cmd.linearY = 0
					cmd.linearZ = 0
					self.lock.acquire()
					self.cmdVelPrx.setCMDVelData(cmd)
					self.lock.release()
				elif(self.sub9 == "StabilizingBottom"):
					cmd = jderobot.CMDVelData()
					cmd.linearX = 0
					cmd.linearY = 0
					cmd.linearZ = 0
					self.lock.acquire()
					self.cmdVelPrx.setCMDVelData(cmd)
					self.lock.release()
				elif(self.sub9 == "GoneToBottom"):
					self.goneToBottom = True
			else:
				if(self.sub9 == "GoingToBottom"):
					t_GoingToBottom_max = 3 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub9.index(self.sub9) + 1
					self.sub9 = self.StatesSub9[ghostStateIndex]
				elif(self.sub9 == "StabilizingBottom"):
					t_StabilizingBottom_max = 2 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub9.index(self.sub9) + 1
					self.sub9 = self.StatesSub9[ghostStateIndex]
				elif(self.sub9 == "GoneToBottom"):
					t_GoneToBottom_max = 0.1 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub9.index(self.sub9) + 1
					self.sub9 = self.StatesSub9[ghostStateIndex]

			totalb = time.time() * 1000000
			msecs = (totalb - totala) / 1000;
			if(msecs < 0 or msecs > cycle):
				msecs = cycle
			else:
				msecs = cycle - msecs

			time.sleep(msecs / 1000)
			if(msecs < 33 ):
				time.sleep(33 / 1000);


	def subautomata10(self):
		run = True
		cycle = 100
		t_activated = False
		t_fin = 0

		t_GoingToRigth_max = 3
		t_StabilizingRigth_max = 2
		t_GoneToRigth_max = 0.1


		while(run):
			totala = time.time() * 1000000

			if(self.sub5 == "DoingBottomSide"):
				if ((self.sub10 == "GoingToRigth_ghost") or (self.sub10 == "StabilizingRigth_ghost") or (self.sub10 == "GoneToRigth_ghost")):
					ghostStateIndex = self.StatesSub10.index(self.sub10)
					self.sub10 = self.StatesSub10[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub10 == "GoingToRigth"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_GoingToRigth_max):
							self.sub10 = "StabilizingRigth"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('StabilizingRigth')
							t_GoingToRigth_max = 3

				elif(self.sub10 == "StabilizingRigth"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_StabilizingRigth_max):
							self.sub10 = "GoneToRigth"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('GoneToRigth')
							t_StabilizingRigth_max = 2

				elif(self.sub10 == "GoneToRigth"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_GoneToRigth_max):
							self.sub10 = "GoingToRigth"
							t_activated = False
							self.goneToRigth = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('GoingToRigth')
							t_GoneToRigth_max = 0.1


				# Actuation if
				if(self.sub10 == "GoingToRigth"):
					cmd = jderobot.CMDVelData()
					cmd.linearX = 0
					cmd.linearY = -0.75
					cmd.linearZ = 0
					self.lock.acquire()
					self.cmdVelPrx.setCMDVelData(cmd)
					self.lock.release()
				elif(self.sub10 == "StabilizingRigth"):
					cmd = jderobot.CMDVelData()
					cmd.linearX = 0
					cmd.linearY = 0
					cmd.linearZ = 0
					self.lock.acquire()
					self.cmdVelPrx.setCMDVelData(cmd)
					self.lock.release()
				elif(self.sub10 == "GoneToRigth"):
					self.goneToRigth = True
			else:
				if(self.sub10 == "GoingToRigth"):
					t_GoingToRigth_max = 3 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub10.index(self.sub10) + 1
					self.sub10 = self.StatesSub10[ghostStateIndex]
				elif(self.sub10 == "StabilizingRigth"):
					t_StabilizingRigth_max = 2 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub10.index(self.sub10) + 1
					self.sub10 = self.StatesSub10[ghostStateIndex]
				elif(self.sub10 == "GoneToRigth"):
					t_GoneToRigth_max = 0.1 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub10.index(self.sub10) + 1
					self.sub10 = self.StatesSub10[ghostStateIndex]

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

		# Contact to pose3d
		pose3d = self.ic.propertyToProxy('automata.Pose3D.Proxy')
		if(not pose3d):
			raise Exception('could not create proxy with pose3d')
		self.pose3dPrx = Pose3DPrx.checkedCast(pose3d)
		if(not self.pose3dPrx):
			raise Exception('invalid proxy automata.Pose3D.Proxy')
		print 'pose3d connected'

		# Contact to cmdVel
		cmdVel = self.ic.propertyToProxy('automata.CMDVel.Proxy')
		if(not cmdVel):
			raise Exception('could not create proxy with cmdVel')
		self.cmdVelPrx = CMDVelPrx.checkedCast(cmdVel)
		if(not self.cmdVelPrx):
			raise Exception('invalid proxy automata.CMDVel.Proxy')
		print 'cmdVel connected'

		# Contact to extra
		extra = self.ic.propertyToProxy('automata.ArDroneExtra.Proxy')
		if(not extra):
			raise Exception('could not create proxy with extra')
		self.extraPrx = ArDroneExtraPrx.checkedCast(extra)
		if(not self.extraPrx):
			raise Exception('invalid proxy automata.ArDroneExtra.Proxy')
		print 'extra connected'


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
		self.t4.join()
		self.t5.join()
		self.t6.join()
		self.t8.join()
		self.t9.join()
		self.t10.join()


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
