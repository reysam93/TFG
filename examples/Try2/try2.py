#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
import sys, signal
sys.path.append('/usr/local/share/jderobot/python/visualHFSM_py')
import traceback, threading, time
from automatagui import AutomataGui, QtGui, GuiSubautomata

class Automata():

	def __init__(self):
		self.lock = threading.Lock()
		self.displayGui = False
		self.StatesSub1 = [
			"PingPong",
			"Numbers",
		]

		self.StatesSub3 = [
			"Ping",
			"Ping_ghost",
			"Pong",
			"Pong_ghost",
		]

		self.StatesSub4 = [
			"1",
			"1_ghost",
			"2",
			"2_ghost",
			"3",
			"3_ghost",
		]

		self.StatesSub5 = [
			"wait2",
			"wait2_ghost",
			"wait1",
			"wait1_ghost",
		]

		self.sub1 = "Numbers"
		self.run1 = True
		self.sub3 = "Ping_ghost"
		self.run3 = True
		self.sub4 = "1_ghost"
		self.run4 = True
		self.sub5 = "wait1_ghost"
		self.run5 = True

	def startThreads(self):
		self.t1 = threading.Thread(target=self.subautomata1)
		self.t1.start()
		self.t3 = threading.Thread(target=self.subautomata3)
		self.t3.start()
		self.t4 = threading.Thread(target=self.subautomata4)
		self.t4.start()
		self.t5 = threading.Thread(target=self.subautomata5)
		self.t5.start()

	def createAutomata(self):
		guiSubautomataList = []

		# Creating subAutomata1
		guiSubautomata1 = GuiSubautomata(1,0, self.automataGui)

		guiSubautomata1.newGuiNode(1, 3, 113, 192, 0, 'PingPong')
		guiSubautomata1.newGuiNode(2, 4, 512, 223, 1, 'Numbers')

		guiSubautomata1.newGuiTransition((512, 223), (113, 192), (302, 378), 1, 2, 1)
		guiSubautomata1.newGuiTransition((113, 192), (512, 223), (322, 127), 2, 1, 2)
		guiSubautomataList.append(guiSubautomata1)

		# Creating subAutomata3
		guiSubautomata3 = GuiSubautomata(3,1, self.automataGui)

		guiSubautomata3.newGuiNode(4, 0, 65, 154, 1, 'Ping')
		guiSubautomata3.newGuiNode(5, 5, 313, 162, 0, 'Pong')

		guiSubautomata3.newGuiTransition((65, 154), (313, 162), (192, 74), 3, 4, 5)
		guiSubautomata3.newGuiTransition((313, 162), (65, 154), (187, 212), 4, 5, 4)
		guiSubautomataList.append(guiSubautomata3)

		# Creating subAutomata4
		guiSubautomata4 = GuiSubautomata(4,2, self.automataGui)

		guiSubautomata4.newGuiNode(6, 0, 161, 158, 1, '1')
		guiSubautomata4.newGuiNode(7, 0, 493, 246, 0, '2')
		guiSubautomata4.newGuiNode(8, 0, 207, 358, 0, '3')

		guiSubautomata4.newGuiTransition((161, 158), (493, 246), (327, 202), 5, 6, 7)
		guiSubautomata4.newGuiTransition((493, 246), (207, 358), (350, 302), 6, 7, 8)
		guiSubautomata4.newGuiTransition((207, 358), (161, 158), (184, 258), 7, 8, 6)
		guiSubautomataList.append(guiSubautomata4)

		# Creating subAutomata5
		guiSubautomata5 = GuiSubautomata(5,5, self.automataGui)

		guiSubautomata5.newGuiNode(9, 0, 257, 221, 0, 'wait2')
		guiSubautomata5.newGuiNode(10, 0, 130, 105, 1, 'wait1')

		guiSubautomata5.newGuiTransition((130, 105), (257, 221), (260, 99), 1, 10, 9)
		guiSubautomata5.newGuiTransition((257, 221), (130, 105), (118, 214), 2, 9, 10)
		guiSubautomataList.append(guiSubautomata5)


		return guiSubautomataList

	def shutDown(self):
		self.run1 = False
		self.run3 = False
		self.run4 = False
		self.run5 = False

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

		self.numbersFinished = False

		while(self.run1):
			totala = time.time() * 1000000

			# Evaluation if
			if(self.sub1 == "PingPong"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 3.5):
						self.sub1 = "Numbers"
						t_activated = False
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('Numbers')

			elif(self.sub1 == "Numbers"):
				if(self.numbersFinished):
					self.sub1 = "PingPong"
					self.numbersFinished = False
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('PingPong')


			# Actuation if
			if(self.sub1 == "PingPong"):
				print "PingPong"
				time.sleep(4)
			elif(self.sub1 == "Numbers"):
				print "Numbers"
				time.sleep(5)

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


		self.ping = False
		self.ping = False

		while(self.run3):
			totala = time.time() * 1000000

			if(self.sub1 == "PingPong"):
				if ((self.sub3 == "Ping_ghost") or (self.sub3 == "Pong_ghost")):
					ghostStateIndex = self.StatesSub3.index(self.sub3)
					self.sub3 = self.StatesSub3[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub3 == "Ping"):
					if(self.ping):
						self.sub3 = "Pong"
						self.ping = False
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('Pong')

				elif(self.sub3 == "Pong"):
					if(self.pong):
						self.sub3 = "Ping"
						self.pong = False
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('Ping')


				# Actuation if
				if(self.sub3 == "Ping"):
					print "    PING"
					time.sleep(0.5)
					self.ping= True
				elif(self.sub3 == "Pong"):
					print "            PONG"
					time.sleep(0.5)
					self.pong = True
			else:
				if(self.sub3 == "Ping"):
					ghostStateIndex = self.StatesSub3.index(self.sub3) + 1
					self.sub3 = self.StatesSub3[ghostStateIndex]
				elif(self.sub3 == "Pong"):
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

		t_1_max = 0.001
		t_2_max = 0.001
		t_3_max = 0.001


		while(self.run4):
			totala = time.time() * 1000000

			if(self.sub1 == "Numbers"):
				if ((self.sub4 == "1_ghost") or (self.sub4 == "2_ghost") or (self.sub4 == "3_ghost")):
					ghostStateIndex = self.StatesSub4.index(self.sub4)
					self.sub4 = self.StatesSub4[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub4 == "1"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_1_max):
							self.sub4 = "2"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('2')
							t_1_max = 0.001

				elif(self.sub4 == "2"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_2_max):
							self.sub4 = "3"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('3')
							t_2_max = 0.001

				elif(self.sub4 == "3"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_3_max):
							self.sub4 = "1"
							t_activated = False
							self.numbersFinished= True
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('1')
							t_3_max = 0.001


				# Actuation if
				if(self.sub4 == "1"):
					print "    1"
					time.sleep(1)
				elif(self.sub4 == "2"):
					print "        2"
					time.sleep(1)
				elif(self.sub4 == "3"):
					print "            3"
					time.sleep(1)
			else:
				if(self.sub4 == "1"):
					t_1_max = 0.001 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub4.index(self.sub4) + 1
					self.sub4 = self.StatesSub4[ghostStateIndex]
				elif(self.sub4 == "2"):
					t_2_max = 0.001 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub4.index(self.sub4) + 1
					self.sub4 = self.StatesSub4[ghostStateIndex]
				elif(self.sub4 == "3"):
					t_3_max = 0.001 - (t_fin - t_ini)
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

		t_wait1_max = 1
		t_wait2_max = 1


		while(self.run5):
			totala = time.time() * 1000000

			if(self.sub3 == "Pong"):
				if ((self.sub5 == "wait2_ghost") or (self.sub5 == "wait1_ghost")):
					ghostStateIndex = self.StatesSub5.index(self.sub5)
					self.sub5 = self.StatesSub5[ghostStateIndex - 1]
					t_ini = time.time()

				# Evaluation if
				if(self.sub5 == "wait2"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_wait2_max):
							self.sub5 = "wait1"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('wait1')
							t_wait2_max = 1

				elif(self.sub5 == "wait1"):
					if(not t_activated):
						t_ini = time.time()
						t_activated = True
					else:
						t_fin = time.time()
						secs = t_fin - t_ini
						if(secs > t_wait1_max):
							self.sub5 = "wait2"
							t_activated = False
							if self.displayGui:
								self.automataGui.notifySetNodeAsActive('wait2')
							t_wait1_max = 1


				# Actuation if
				if(self.sub5 == "wait2"):
					print ""
				elif(self.sub5 == "wait1"):
					print ""
			else:
				if(self.sub5 == "wait2"):
					t_wait2_max = 1 - (t_fin - t_ini)
					ghostStateIndex = self.StatesSub5.index(self.sub5) + 1
					self.sub5 = self.StatesSub5[ghostStateIndex]
				elif(self.sub5 == "wait1"):
					t_wait1_max = 1 - (t_fin - t_ini)
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


	def connectToProxys(self):
		self.ic = Ice.initialize(sys.argv)


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
