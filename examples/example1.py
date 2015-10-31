#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
import sys, signal
import traceback, threading, time

import iostream

from jderobot import EncodersPrx
from jderobot import MotorsPrx

void shutDown(){
	run1 = false;
	run2 = false;
	run3 = false;
}







class Automata():

	def __init__(self):
		self.lock = threading.Lock()
		self.StatesSub1 = [
			"square",
			"wait",
			"state",
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

	def shutDown(self):
		self.run1 = False
		self.run2 = False
		self.run3 = False

	def subautomata1(self):
		run = True
		cycle = 100
		t_activated = False


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

elif(self.sub1 == "square"):
elif(self.sub1 == "square"):
				if(true):
					self.sub1 = "state"


			elif(self.sub1 == "wait"):
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

elif(self.sub1 == "wait"):
			elif(self.sub1 == "state"):
elif(self.sub1 == "state"):
elif(self.sub1 == "state"):

			# Actuation if
			if(self.sub1 == "wait"):
				
				
				Motorsprx->setV(0.0);
				Motorsprx->setW(0.0);
			elif(self.sub1 == "state"):
				shutDown();

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
							t_go_up_max = 2

elif(self.sub2 == "go_up"):
elif(self.sub2 == "go_up"):
elif(self.sub2 == "go_up"):
elif(self.sub2 == "go_up"):
elif(self.sub2 == "go_up"):
elif(self.sub2 == "go_up"):
elif(self.sub2 == "go_up"):
				elif(self.sub2 == "turn_rigth"):
elif(self.sub2 == "turn_rigth"):
					if(angle > 90):
						self.sub2 = "go_rigth"


elif(self.sub2 == "turn_rigth"):
elif(self.sub2 == "turn_rigth"):
elif(self.sub2 == "turn_rigth"):
elif(self.sub2 == "turn_rigth"):
elif(self.sub2 == "turn_rigth"):
elif(self.sub2 == "turn_rigth"):
				elif(self.sub2 == "go_rigth"):
elif(self.sub2 == "go_rigth"):
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
							t_go_rigth_max = 2

elif(self.sub2 == "go_rigth"):
elif(self.sub2 == "go_rigth"):
elif(self.sub2 == "go_rigth"):
elif(self.sub2 == "go_rigth"):
elif(self.sub2 == "go_rigth"):
				elif(self.sub2 == "turn_down"):
elif(self.sub2 == "turn_down"):
elif(self.sub2 == "turn_down"):
elif(self.sub2 == "turn_down"):
					if(angle > 90):
						self.sub2 = "go_down"


elif(self.sub2 == "turn_down"):
elif(self.sub2 == "turn_down"):
elif(self.sub2 == "turn_down"):
elif(self.sub2 == "turn_down"):
				elif(self.sub2 == "go_down"):
elif(self.sub2 == "go_down"):
elif(self.sub2 == "go_down"):
elif(self.sub2 == "go_down"):
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
							t_go_down_max = 2

elif(self.sub2 == "go_down"):
elif(self.sub2 == "go_down"):
elif(self.sub2 == "go_down"):
				elif(self.sub2 == "turn_left"):
elif(self.sub2 == "turn_left"):
elif(self.sub2 == "turn_left"):
elif(self.sub2 == "turn_left"):
elif(self.sub2 == "turn_left"):
elif(self.sub2 == "turn_left"):
					if(angle > 90):
						self.sub2 = "go_left"


elif(self.sub2 == "turn_left"):
elif(self.sub2 == "turn_left"):
				elif(self.sub2 == "go_left"):
elif(self.sub2 == "go_left"):
elif(self.sub2 == "go_left"):
elif(self.sub2 == "go_left"):
elif(self.sub2 == "go_left"):
elif(self.sub2 == "go_left"):
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
							t_go_left_max = 2

elif(self.sub2 == "go_left"):
				elif(self.sub2 == "turn_up"):
elif(self.sub2 == "turn_up"):
elif(self.sub2 == "turn_up"):
elif(self.sub2 == "turn_up"):
elif(self.sub2 == "turn_up"):
elif(self.sub2 == "turn_up"):
elif(self.sub2 == "turn_up"):
elif(self.sub2 == "turn_up"):
					if(angle > 90):
						self.sub2 = "go_up"



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
				if(sub2):
					if(sub2 == "go_up"):
						t_go_up_max = 2 - (t_fin - t_ini)
						ghostStateIndex = self.StateSub2.index(self.sub2) + 1
						sub2 = self.StatesSub2[ghostStateIndex]
			else:
				if(sub2):
					if(sub2 == "go_rigth"):
						t_go_rigth_max = 2 - (t_fin - t_ini)
						ghostStateIndex = self.StateSub2.index(self.sub2) + 1
						sub2 = self.StatesSub2[ghostStateIndex]
			else:
				if(sub2):
					if(sub2 == "go_down"):
						t_go_down_max = 2 - (t_fin - t_ini)
						ghostStateIndex = self.StateSub2.index(self.sub2) + 1
						sub2 = self.StatesSub2[ghostStateIndex]
			else:
				if(sub2):
					if(sub2 == "go_left"):
						t_go_left_max = 2 - (t_fin - t_ini)
						ghostStateIndex = self.StateSub2.index(self.sub2) + 1
						sub2 = self.StatesSub2[ghostStateIndex]

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
							t_wait1_max = 2

elif(self.sub3 == "wait1"):
				elif(self.sub3 == "wait2"):
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
							t_wait2_max = 2.1


				# Actuation if
			else:
				if(sub3):
					if(sub3 == "wait1"):
						t_wait1_max = 2 - (t_fin - t_ini)
						ghostStateIndex = self.StateSub3.index(self.sub3) + 1
						sub3 = self.StatesSub3[ghostStateIndex]
			else:
				if(sub3):
					if(sub3 == "wait2"):
						t_wait2_max = 2.1 - (t_fin - t_ini)
						ghostStateIndex = self.StateSub3.index(self.sub3) + 1
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


	def connectToProxys(self):
		self.ic = Ice.initialize(sys.argv)

		# Contact to Encoders
		Encoders = self.ic.propertyToProxy("automata.Encoders.Proxy");
		if(not Encoders):
			raise Exception("could not create proxy withEncoders")
		self.EncodersPrx = EncodersPrx.checkedCast(Encoders)
		if(not self.EncodersPrx):
			raise Exception("invalid proxy automata.Encoders.Proxy")
		print "Encoders connected"

		# Contact to Motors
		Motors = self.ic.propertyToProxy("automata.Motors.Proxy");
		if(not Motors):
			raise Exception("could not create proxy withMotors")
		self.MotorsPrx = MotorsPrx.checkedCast(Motors)
		if(not self.MotorsPrx):
			raise Exception("invalid proxy automata.Motors.Proxy")
		print "Motors connected"


	def destroyIc(self):
		if(self.ic):
			self.ic.destroy()


	def start(self):
		self.t1 = threading.Thread(target=self.subautomata1)
		self.t1.start()
		self.t2 = threading.Thread(target=self.subautomata2)
		self.t2.start()
		self.t3 = threading.Thread(target=self.subautomata3)
		self.t3.start()


	def join(self):
		self.t1.join()
		self.t2.join()
		self.t3.join()


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
