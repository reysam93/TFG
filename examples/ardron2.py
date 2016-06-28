#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
import sys, signal
import traceback, threading, time
import jderobot

from jderobot import CMDVelPrx
from jderobot import ArDroneExtraPrx







class Automata():

	def __init__(self):
		self.lock = threading.Lock()
		self.StatesSub1 = [
			"TakeOff",
			"GoFront",
			"Turn",
			"Land",
			"Finish",
		]

		self.StatesSub2 = [
			"TakingOff",
			"TakingOff_ghost",
			"Stabilizing",
			"Stabilizing_ghost",
			"ENDSUBAUTOMATA",
			"ENDSUBAUTOMATA_ghost",
		]

		self.StatesSub3 = [
			"GoingFront",
			"GoingFront_ghost",
			"Stabilizing",
			"Stabilizing_ghost",
			"ENDSUBAUTOMATA",
			"ENDSUBAUTOMATA_ghost",
		]

		self.sub1 = "TakeOff"
		self.run1 = True
		self.sub2 = "TakingOff_ghost"
		self.run2 = True
		self.sub3 = "GoingFront_ghost"
		self.run3 = True

	def shutDown(self):
		self.run1 = False
		self.run2 = False
		self.run3 = False

	def runGui(self):
		app = QtGui.QApplication(sys.argv)
		self.automataGui = AutomataGui()
		self.automataGui.draw()
		self.automataGui.show()
		app.exec_()
		

	def subautomata1(self):
		run = True
		cycle = 100
		t_activated = False

		self.endTakeOff = False
		self.endGoFront = False
		hasLanded = False

		while(run):
			totala = time.time() * 1000000

			# Evaluation if
			if(self.sub1 == "TakeOff"):
				if(self.endTakeOff):
					self.sub1 = "GoFront"


			elif(self.sub1 == "GoFront"):
				if(self.endGoFront):
					self.sub1 = "Turn"


			elif(self.sub1 == "Turn"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 0.5):
						self.sub1 = "Land"
						t_activated = False

			elif(self.sub1 == "Land"):
				if(hasLanded):
					self.sub1 = "Finish"



			# Actuation if
			if(self.sub1 == "GoFront"):
				print "Going Front"
			elif(self.sub1 == "Turn"):
				print "Do nothing yet"
			elif(self.sub1 == "Land"):
				self.lock.acquire()
				self.extraPrx.land()
				self.lock.release()
				hasLanded = True
			elif(self.sub1 == "Finish"):
				print "Finished!"

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

		t_Stabilizing_max = 2.5

		hasTakenOff = False

		while(run):
			totala = time.time() * 1000000

			if(self.sub1 == "TakeOff"):
				if ((self.sub2 == "TakingOff_ghost") or (self.sub2 == "Stabilizing_ghost") or (self.sub2 == "ENDSUBAUTOMATA_ghost")):
					ghostStateIndex = self.StatesSub2.index(self.sub2)
					self.sub2 = self.StatesSub2[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub2 == "TakingOff"):
					if(hasTakenOff):
						self.sub2 = "Stabilizing"


				elif(self.sub2 == "Stabilizing"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_Stabilizing_max):
							self.sub2 = "ENDSUBAUTOMATA"
							t_activated = False
							t_Stabilizing_max = 2.5


				# Actuation if
				if(self.sub2 == "TakingOff"):
					self.lock.acquire()
					self.extraPrx.takeoff()
					self.lock.release()
					hasTakenOff = True
					print "TakingOff"
				elif(self.sub2 == "Stabilizing"):
					print "Stabilizing after taking off"
				elif(self.sub2 == "ENDSUBAUTOMATA"):
					if(not self.endTakeOff):
						print "TakeOff ended"
					self.endTakeOff = True
			else:
				if(self.sub2 == "Stabilizing"):
					t_Stabilizing_max = 2.5 - (t_fin - t_ini)
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

		t_GoingFront_max = 4
		t_Stabilizing_max = 3


		while(run):
			totala = time.time() * 1000000

			if(self.sub1 == "GoFront"):
				if ((self.sub3 == "GoingFront_ghost") or (self.sub3 == "Stabilizing_ghost") or (self.sub3 == "ENDSUBAUTOMATA_ghost")):
					ghostStateIndex = self.StatesSub3.index(self.sub3)
					self.sub3 = self.StatesSub3[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub3 == "GoingFront"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_GoingFront_max):
							self.sub3 = "Stabilizing"
							t_activated = False
							t_GoingFront_max = 4

				elif(self.sub3 == "Stabilizing"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_Stabilizing_max):
							self.sub3 = "ENDSUBAUTOMATA"
							t_activated = False
							t_Stabilizing_max = 3


				# Actuation if
				if(self.sub3 == "GoingFront"):
					cmd = jderobot.CMDVelData()
					cmd.linearX = 1
					cmd.linearY = 0
					cmd.linearZ = 0
					self.lock.acquire()
					self.cmdPrx.setCMDVelData(cmd)
					self.lock.release()
				elif(self.sub3 == "ENDSUBAUTOMATA"):
					self.endGoFront = True
			else:
				if(self.sub3 == "GoingFront"):
					t_GoingFront_max = 4 - (t_fin - t_ini)
					ghostStateIndex = self.StateSub3.index(self.sub3) + 1
					sub3 = self.StatesSub3[ghostStateIndex]
				elif(self.sub3 == "Stabilizing"):
					t_Stabilizing_max = 3 - (t_fin - t_ini)
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
	

	def destroyIc(self):
		if(self.ic):
			self.ic.destroy()


	def start(self):
		self.guiThread = threading.Thread(target=self.runGui)
		self.guiThread.start()

		self.t1 = threading.Thread(target=self.subautomata1)
		#self.t1.start()
		self.t2 = threading.Thread(target=self.subautomata2)
		#self.t2.start()
		self.t3 = threading.Thread(target=self.subautomata3)
		#self.t3.start()



	def join(self):
		self.guiThread.join()
		self.t1.join()
		self.t2.join()
		self.t3.join()


if __name__ == '__main__':
		sys.path.append("/home/samuelvm/TFG/visualHFSM")
		from automatagui import AutomataGui, QtGui
		print sys.path
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
	