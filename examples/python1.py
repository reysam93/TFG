#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, Ice, traceback, threading, time
import jderobot

Names_Sub_1 = [
	"state",
]

sub_1 = "state"

if __name__ == '__main__':
	try:
		ic = Ice.initialize(sys.argv)
		properties = ic.getProperties()

		# Contact to Camera
		Camera = ic.propertyToProxy("automata.Camera.Proxy");
		if(not Camera):
			print "ERROR: could not create proxy with Camera"
			#raise Exception
		Cameraprx = CameraPrx.checkedCast(Camera)
		if(not Cameraprx):
			print "ERROR:invalid proxy automata.Camera.Proxy";
			#raise Exception
		print "Camera connected"



		t1 = threading.Thread(target=subautomata_1)
		t1.start()

		t1.join()
	except:
		traceback.print_exc()
		if(ic):
			ic.destroy()
	exit(-1)
