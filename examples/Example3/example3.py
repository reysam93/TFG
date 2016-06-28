#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
import sys, signal
import traceback, threading, time
from automatagui import AutomataGui, QtGui
from createAutomata import createAutomata

import iostream

from jderobot import EncodersPrx
from jderobot import MotorsPrx



class Automata():

	def __init__(self):
		self.lock = threading.Lock()
		self.StatesSub1 = [
			"GoFront",
			"GoBack",
			"Turn",
			"Wait",
		]

		self.sub1 = "GoFront"
		self.run1 = True

	def shutDown(self):
		self.run1 = False

	def runGui(self):
		app = QtGui.QApplication(sys.argv)
		self.automataGui = AutomataGui()
		self.automataGui.setAutomata(createAutomata())
		self.automataGui.loadAutomata()
		self.automataGui.show()
		app.exec_()

	def subautomata1(self):
		run = True
		cycle = 100
		t_activated = False

		jderobot::EncodersDataPtr encoders = Encodersprx->getEncodersData();
		float thetapos = 0;
		float angle = 0;

		while(run):
			totala = time.time() * 1000000

			# Evaluation if
			if(self.sub1 == "GoFront"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 2):
						self.sub1 = "GoBack"
						t_activated = False

			elif(self.sub1 == "GoBack"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 2):
						self.sub1 = "Turn"
						t_activated = False

			elif(self.sub1 == "Turn"):
				if(angle > 45):
					self.sub1 = "Wait"


			elif(self.sub1 == "Wait"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 1):
						self.sub1 = "GoFront"
						t_activated = False


			# Actuation if
			if(self.sub1 == "GoFront"):
				Motorsprx->setV(100.0);
				Motorsprx->setW(0.0);
				
				encoders = Encodersprx->getEncodersData();
				thetapos = encoders->robottheta;
			elif(self.sub1 == "GoBack"):
				Motorsprx->setV(-100.0);
				Motorsprx->setW(0.0);
				
				encoders = Encodersprx->getEncodersData();
				thetapos = encoders->robottheta;
			elif(self.sub1 == "Turn"):
				Motorsprx->setV(0.0);
				Motorsprx->setW(-3.0);
				
				encoders = Encodersprx->getEncodersData();
				if (encoders->robottheta > thetapos + 1)
					angle = thetapos - encoders->robottheta + 360;
				else
					angle = thetapos - encoders->robottheta;
				
				std::cout << "angle: " << angle << std::endl;
			elif(self.sub1 == "Wait"):
				Motorsprx->setV(0.0);
				Motorsprx->setW(0.0);
				
				encoders = Encodersprx->getEncodersData();
				thetapos = encoders->robottheta;

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
		self.guiThread = threading.Thread(target=self.runGui)
		self.guiThread.start()

		self.t1 = threading.Thread(target=self.subautomata1)
		self.t1.start()


	def join(self):
		self.guiThread.join()
		self.t1.join()


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
