#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
import sys, signal
import traceback, threading, time

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
		self.NamesSub1 = [
			"TakeOff",
			"Stabilizing1",
			"GoFront",
			"Stoping",
			"Landing",
			"Stabilizing2",
		]

		self.sub1 = "TakeOff"

	def subautomata1(self):
		cycle = 100
		t_activated = False

		hasTakenOff = False
		hasLanded = False

		while(True):
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


	def connectToProxys(self):
		self.ic = Ice.initialize(sys.argv)

		# Contact to camera
		camera = self.ic.propertyToProxy("automata.Camera.Proxy");
		if(not camera):
			raise Exception("could not create proxy withcamera")
		self.cameraPrx = CameraPrx.checkedCast(camera)
		if(not self.cameraPrx):
			raise Exception("invalid proxy automata.camera.Proxy")
		print "camera connected"

		# Contact to pose3d
		pose3d = self.ic.propertyToProxy("automata.Pose3D.Proxy");
		if(not pose3d):
			raise Exception("could not create proxy withpose3d")
		self.pose3dPrx = Pose3DPrx.checkedCast(pose3d)
		if(not self.pose3dPrx):
			raise Exception("invalid proxy automata.pose3d.Proxy")
		print "pose3d connected"

		# Contact to cmd
		cmd = self.ic.propertyToProxy("automata.CMDVel.Proxy");
		if(not cmd):
			raise Exception("could not create proxy withcmd")
		self.cmdPrx = CMDVelPrx.checkedCast(cmd)
		if(not self.cmdPrx):
			raise Exception("invalid proxy automata.cmd.Proxy")
		print "cmd connected"

		# Contact to extra
		extra = self.ic.propertyToProxy("automata.ArDroneExtra.Proxy");
		if(not extra):
			raise Exception("could not create proxy withextra")
		self.extraPrx = ArDroneExtraPrx.checkedCast(extra)
		if(not self.extraPrx):
			raise Exception("invalid proxy automata.extra.Proxy")
		print "extra connected"

		# Contact to navdata
		navdata = self.ic.propertyToProxy("automata.Navdata.Proxy");
		if(not navdata):
			raise Exception("could not create proxy withnavdata")
		self.navdataPrx = NavdataPrx.checkedCast(navdata)
		if(not self.navdataPrx):
			raise Exception("invalid proxy automata.navdata.Proxy")
		print "navdata connected"


	def destroyIc(self):
		if(self.ic):
			self.ic.destroy()


	def start(self):
		self.t1 = threading.Thread(target=self.subautomata1)
		self.t1.start()


	def join(self):
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
