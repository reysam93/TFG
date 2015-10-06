#!/usr/bin/python

import threading, time

array = [1,
		"2",
		"3",]

print array[0]
print array[2]

def subautomata_1():
	print "SOY UN THREAD"

t1 = threading.Thread(target=subautomata_1)
t2 = threading.Thread(target=subautomata_1)
t3 = threading.Thread(target=subautomata_1)
t1.start()
t2.start()
t3.start()
t1.join()
t2.join()
t3.join()

hora1 = time.time()
time.sleep(3)
hora2 = time.time()
print "hora1:", hora1, "hora2:", hora2
print "resta:", (hora2 - hora1)