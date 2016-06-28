#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
import sys, signal
sys.path.append('/usr/local/share/jderobot/python/visualHFSM_py')
import traceback, threading, time
from automatagui import AutomataGui, QtGui, GuiSubautomata

import iostream

from jderobot import EncodersPrx
from jderobot import MotorsPrx







class Automata():

	def __init__(self):
		self.lock = threading.Lock()
		self.displayGui = False
		self.StatesSub1 = [
			"square",
			"wait",
		]

		self.StatesSub2 = [
			"go_up",
			"go_up_ghost",
			"turn_rigth",
			"turn_rigth_ghost",
			"go_rigth",
			"go_rigth_ghost",
			"turn_down",
			"turn_down_ghost",
			"go_down",
			"go_down_ghost",
			"turn_left",
			"turn_left_ghost",
			"go_left",
			"go_left_ghost",
			"turn_up",
			"turn_up_ghost",
		]

		self.StatesSub3 = [
			"wait1",
			"wait1_ghost",
			"wait2",
			"wait2_ghost",
		]

		self.sub1 = "square"
		self.run1 = True
		self.sub2 = "go_up_ghost"
		self.run2 = True
		self.sub3 = "wait1_ghost"
		self.run3 = True

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

		guiSubautomata1.newGuiNode(1, 2, 134, 346, 1, 'square')
		guiSubautomata1.newGuiNode(2, 3, 534, 349, 0, 'wait')

		guiSubautomata1.newGuiTransition((134, 346), (534, 349), (337, 230), 1, 1, 2)
		guiSubautomata1.newGuiTransition((534, 349), (134, 346), (335, 457), 4, 2, 1)
		guiSubautomataList.append(guiSubautomata1)

		# Creating subAutomata2
		guiSubautomata2 = GuiSubautomata(2,1, self.automataGui)

		guiSubautomata2.newGuiNode(5, 0, 168, 559, 1, 'go_up')
		guiSubautomata2.newGuiNode(8, 0, 69, 396, 0, 'turn_rigth')
		guiSubautomata2.newGuiNode(9, 0, 185, 270, 0, 'go_rigth')
		guiSubautomata2.newGuiNode(10, 0, 343, 192, 0, 'turn_down')
		guiSubautomata2.newGuiNode(11, 0, 486, 283, 0, 'go_down')
		guiSubautomata2.newGuiNode(12, 0, 555, 426, 0, 'turn_left')
		guiSubautomata2.newGuiNode(13, 0, 505, 583, 0, 'go_left')
		guiSubautomata2.newGuiNode(14, 0, 354, 650, 0, 'turn_up')

		guiSubautomata2.newGuiTransition((168, 559), (69, 396), (118, 477), 10, 5, 8)
		guiSubautomata2.newGuiTransition((69, 396), (185, 270), (127, 333), 12, 8, 9)
		guiSubautomata2.newGuiTransition((185, 270), (343, 192), (264, 231), 13, 9, 10)
		guiSubautomata2.newGuiTransition((343, 192), (486, 283), (415, 237), 14, 10, 11)
		guiSubautomata2.newGuiTransition((486, 283), (555, 426), (525, 348), 15, 11, 12)
		guiSubautomata2.newGuiTransition((555, 426), (505, 583), (534, 498), 16, 12, 13)
		guiSubautomata2.newGuiTransition((505, 583), (354, 650), (430, 616), 17, 13, 14)
		guiSubautomata2.newGuiTransition((354, 650), (168, 559), (261, 604), 18, 14, 5)
		guiSubautomataList.append(guiSubautomata2)

		# Creating subAutomata3
		guiSubautomata3 = GuiSubautomata(3,2, self.automataGui)

		guiSubautomata3.newGuiNode(15, 0, 166, 223, 1, 'wait1')
		guiSubautomata3.newGuiNode(16, 0, 446, 237, 0, 'wait2')

		guiSubautomata3.newGuiTransition((166, 223), (446, 237), (291, 127), 1, 15, 16)
		guiSubautomata3.newGuiTransition((446, 237), (166, 223), (291, 301), 3, 16, 15)
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
		run = True
		cycle = 100
		t_activated = False
		t_fin = 0


		while(run):
			totala = time.time() * 1000000

			# Evaluation if
			if(self.sub1 == "square"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 20):
						self.sub1 = "wait"
						t_activated = False
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('wait')

			elif(self.sub1 == "wait"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 5):
						self.sub1 = "square"
						t_activated = False
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('square')


			# Actuation if
			if(self.sub1 == "wait"):
				
				
				Motorsprx->setV(0.0);
				Motorsprx->setW(0.0);

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

		t_go_up_max = 2
		t_go_rigth_max = 2
		t_go_down_max = 2
		t_go_left_max = 2

		jderobot::EncodersDataPtr encoders = Encodersprx->getEncodersData();
		float thetapos = 0;
		float angle = 0;

		while(run):
			totala = time.time() * 1000000

			if(self.sub1 == "square"):
				if ((self.sub2 == "go_up_ghost") or (self.sub2 == "turn_rigth_ghost") or (self.sub2 == "go_rigth_ghost") or (self.sub2 == "turn_down_ghost") or (self.sub2 == "go_down_ghost") or (self.sub2 == "turn_left_ghost") or (self.sub2 == "go_left_ghost") or (self.sub2 == "turn_up_ghost")):
					ghostStateIndex = self.StatesSub2.index(self.sub2)
					self.sub2 = self.StatesSub2[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub2 == "go_up"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_go_up_max):
							self.sub2 = "turn_rigth"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('turn_rigth')
							t_go_up_max = 2

				elif(self.sub2 == "turn_rigth"):
					if(angle > 90):
						self.sub2 = "go_rigth"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('go_rigth')

				elif(self.sub2 == "go_rigth"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_go_rigth_max):
							self.sub2 = "turn_down"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('turn_down')
							t_go_rigth_max = 2

				elif(self.sub2 == "turn_down"):
					if(angle > 90):
						self.sub2 = "go_down"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('go_down')

				elif(self.sub2 == "go_down"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_go_down_max):
							self.sub2 = "turn_left"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('turn_left')
							t_go_down_max = 2

				elif(self.sub2 == "turn_left"):
					if(angle > 90):
						self.sub2 = "go_left"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('go_left')

				elif(self.sub2 == "go_left"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_go_left_max):
							self.sub2 = "turn_up"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('turn_up')
							t_go_left_max = 2

				elif(self.sub2 == "turn_up"):
					if(angle > 90):
						self.sub2 = "go_up"
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('go_up')


				# Actuation if
				if(self.sub2 == "go_up"):
					
					
					Motorsprx->setV(100.0);
					Motorsprx->setW(0.0);
					
					encoders = Encodersprx->getEncodersData();
					thetapos = encoders->robottheta;
				elif(self.sub2 == "turn_rigth"):
					
					
					Motorsprx->setV(0.0);
					Motorsprx->setW(-3.0);
					
					encoders = Encodersprx->getEncodersData();
					if (encoders->robottheta > thetapos + 1)
						angle = thetapos - encoders->robottheta + 360;
					else
						angle = thetapos - encoders->robottheta;
					
					std::cout << "angle: " << angle << std::endl;
				elif(self.sub2 == "go_rigth"):
					
					
					Motorsprx->setV(100.0);
					Motorsprx->setW(0.0);
					
					encoders = Encodersprx->getEncodersData();
					thetapos = encoders->robottheta;
				elif(self.sub2 == "turn_down"):
					
					
					Motorsprx->setV(0.0);
					Motorsprx->setW(-3.0);
					
					encoders = Encodersprx->getEncodersData();
					if (encoders->robottheta > thetapos + 1)
						angle = thetapos - encoders->robottheta + 360;
					else
						angle = thetapos - encoders->robottheta;
					
					std::cout << "angle: " << angle << std::endl;
				elif(self.sub2 == "go_down"):
					
					
					Motorsprx->setV(100.0);
					Motorsprx->setW(0.0);
					
					encoders = Encodersprx->getEncodersData();
					thetapos = encoders->robottheta;
				elif(self.sub2 == "turn_left"):
					
					
					Motorsprx->setV(0.0);
					Motorsprx->setW(-3.0);
					
					encoders = Encodersprx->getEncodersData();
					if (encoders->robottheta > thetapos + 1)
						angle = thetapos - encoders->robottheta + 360;
					else
						angle = thetapos - encoders->robottheta;
					
					std::cout << "angle: " << angle << std::endl;
				elif(self.sub2 == "go_left"):
					
					
					Motorsprx->setV(100.0);
					Motorsprx->setW(0.0);
					
					encoders = Encodersprx->getEncodersData();
					thetapos = encoders->robottheta;
				elif(self.sub2 == "turn_up"):
					
					
					Motorsprx->setV(0.0);
					Motorsprx->setW(-3.0);
					
					encoders = Encodersprx->getEncodersData();
					if (encoders->robottheta > thetapos + 1)
						angle = thetapos - encoders->robottheta + 360;
					else
						angle = thetapos - encoders->robottheta;
					
					std::cout << "angle: " << angle << std::endl;
			else:
				if(self.sub2 == "go_up"):
					t_go_up_max = 2 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub2.index(self.sub2) + 1
					self.sub2 = self.StatesSub2[ghostStateIndex]
				elif(self.sub2 == "turn_rigth"):
					ghostStateIndex = self.StatesSub2.index(self.sub2) + 1
					self.sub2 = self.StatesSub2[ghostStateIndex]
				elif(self.sub2 == "go_rigth"):
					t_go_rigth_max = 2 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub2.index(self.sub2) + 1
					self.sub2 = self.StatesSub2[ghostStateIndex]
				elif(self.sub2 == "turn_down"):
					ghostStateIndex = self.StatesSub2.index(self.sub2) + 1
					self.sub2 = self.StatesSub2[ghostStateIndex]
				elif(self.sub2 == "go_down"):
					t_go_down_max = 2 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub2.index(self.sub2) + 1
					self.sub2 = self.StatesSub2[ghostStateIndex]
				elif(self.sub2 == "turn_left"):
					ghostStateIndex = self.StatesSub2.index(self.sub2) + 1
					self.sub2 = self.StatesSub2[ghostStateIndex]
				elif(self.sub2 == "go_left"):
					t_go_left_max = 2 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub2.index(self.sub2) + 1
					self.sub2 = self.StatesSub2[ghostStateIndex]
				elif(self.sub2 == "turn_up"):
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

		t_wait1_max = 2
		t_wait2_max = 2.1


		while(run):
			totala = time.time() * 1000000

			if(self.sub1 == "wait"):
				if ((self.sub3 == "wait1_ghost") or (self.sub3 == "wait2_ghost")):
					ghostStateIndex = self.StatesSub3.index(self.sub3)
					self.sub3 = self.StatesSub3[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub3 == "wait1"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_wait1_max):
							self.sub3 = "wait2"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('wait2')
							t_wait1_max = 2

				elif(self.sub3 == "wait2"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_wait2_max):
							self.sub3 = "wait1"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('wait1')
							t_wait2_max = 2.1


				# Actuation if
			else:
				if(self.sub3 == "wait1"):
					t_wait1_max = 2 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub3.index(self.sub3) + 1
					self.sub3 = self.StatesSub3[ghostStateIndex]
				elif(self.sub3 == "wait2"):
					t_wait2_max = 2.1 - (t_fin - t_ini)
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

		# Contact to Encoders
		Encoders = self.ic.propertyToProxy('automata.Encoders.Proxy')
		if(not Encoders):
			raise Exception('could not create proxy with Encoders')
		self.EncodersPrx = EncodersPrx.checkedCast(Encoders)
		if(not self.EncodersPrx):
			raise Exception('invalid proxy automata.Encoders.Proxy')
		print 'Encoders connected'

		# Contact to Motors
		Motors = self.ic.propertyToProxy('automata.Motors.Proxy')
		if(not Motors):
			raise Exception('could not create proxy with Motors')
		self.MotorsPrx = MotorsPrx.checkedCast(Motors)
		if(not self.MotorsPrx):
			raise Exception('invalid proxy automata.Motors.Proxy')
		print 'Motors connected'


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
