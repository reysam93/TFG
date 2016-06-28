#!/usr/bin/python
#HEADERS
import Ice
from automatagui import AutomataGui, QtGui, GuiSubautomata
....................
class Automata():
	def __init__(self):
		self.lock = threading.Lock()
		self.displayGui = False
		self.StatesSub1 = [
			"State1",
			"State2",
			"State3",
			"State4",
		]

		self.sub1 = "State1"
		self.run1 = True

	def startThreads(self):
		self.t1 = threading.Thread(target=self.subautomata1)
		self.t1.start()

	def createAutomata(self):
		guiSubautomataList = []

		# Creating subAutomata1
		guiSubautomata1 = GuiSubautomata(1,0, self.automataGui)

		guiSubautomata1.newGuiNode(1, 0, 80, 160, 1, 'State1')
		guiSubautomata1.newGuiNode(2, 0, 473, 164, 0, 'State2')
		guiSubautomata1.newGuiNode(3, 0, 475, 431, 0, 'State3')
		guiSubautomata1.newGuiNode(4, 0, 94, 417, 0, 'State4')

		guiSubautomata1.newGuiTransition((80, 160), (473, 164), (276, 162), 1, 1, 2)
		guiSubautomata1.newGuiTransition((473, 164), (475, 431), (474, 298), 2, 2, 3)
		guiSubautomata1.newGuiTransition((475, 431), (94, 417), (285, 424), 3, 3, 4)
		guiSubautomata1.newGuiTransition((94, 417), (80, 160), (87, 288), 4, 4, 1)
		guiSubautomataList.append(guiSubautomata1)


		return guiSubautomataList

	def shutDown(self):

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

		self.finished = False

		while(self.run1):
			totala = time.time() * 1000000

			# Evaluation if
			if(self.sub1 == "State1"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 2):
						self.sub1 = "State2"
						t_activated = False
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('State2')

			elif(self.sub1 == "State2"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 2):
						self.sub1 = "State3"
						t_activated = False
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('State3')

			elif(self.sub1 == "State3"):
				if(not t_activated):
					t_ini = time.time()
					t_activated = True
				else:
					t_fin = time.time()
					secs = t_fin - t_ini
					if(secs > 2):
						self.sub1 = "State4"
						t_activated = False
						if self.displayGui:
							self.automataGui.notifySetNodeAsActive('State4')

			elif(self.sub1 == "State4"):
				if(self.finished):
					self.sub1 = "State1"
					print "Finished!"
					if self.displayGui:
						self.automataGui.notifySetNodeAsActive('State1')


			# Actuation if
			if(self.sub1 == "State1"):
				print "State1"
				time.sleep(2)
			elif(self.sub1 == "State2"):
				print "State2"
				time.sleep(2)
			elif(self.sub1 == "State3"):
				print "State3"
				time.sleep(2)
			elif(self.sub1 == "State4"):
				print "State4"
				time.sleep(2)
				self.finished = True

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
