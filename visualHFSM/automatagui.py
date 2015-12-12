#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, uic, QtCore
import sys, signal, math
import guisubautomata, point

class AutomataGui(QtGui.QMainWindow):

	

	def __init__(self, parent=None):
		self.RADIUS_DIAMETER = 40;
		self.RADIUS_INIT = 30;
		self.SQUARE_SIDE = 10;
		self.SQUARE_SIDE_MID = self.SQUARE_SIDE / 2;
		QtGui.QMainWindow.__init__(self, parent)
		try:
			uic.loadUi('../visualHFSM/gui/mainGui.ui', self)
		except IOError:
			raise Exception("mainGui.ui doesn't found")
		self.schemaScene = QtGui.QGraphicsScene()
		self.schemaView.setScene(self.schemaScene)
		self.schemaView.show()


	def draw(self):
		self.drawEllipses()
		self.drawTransitions()
		

	def drawEllipses(self):
		print "drawing ellipses example"
		pen = QtGui.QPen(QtGui.QColor("black"))
		pen.setWidth(2)
		brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
		brush.setColor(QtGui.QColor("blue"))
		
		self.schemaScene.addEllipse(50,15,self.RADIUS_DIAMETER,self.RADIUS_DIAMETER, pen, brush)
		self.schemaScene.addSimpleText("State1").setPos(50,60)
		self.schemaScene.addEllipse(50+5,15+5,self.RADIUS_INIT,self.RADIUS_INIT, pen, brush)
		
		self.schemaScene.addEllipse(50,150,self.RADIUS_DIAMETER,self.RADIUS_DIAMETER, pen, brush)
		self.schemaScene.addSimpleText("State2").setPos(50,195)
		
		self.schemaScene.addEllipse(200,15,self.RADIUS_DIAMETER,self.RADIUS_DIAMETER, pen, brush)
		self.schemaScene.addSimpleText("State3").setPos(200,60)


	def calculateGoodArrowPosition(self,x1,y1,x2,y2):
		distance_op = y1 - y2
		distance_ad = x1 - x2

		alpha = math.atan(distance_op/distance_ad)

		poss1_final_x = x1 + self.RADIUS_DIAMETER / 2 + math.cos(alpha)
		poss1_final_y = y1 + self.RADIUS_DIAMETER / 2 + math.sin(alpha)
		d1 = math.sqrt(math.pow(poss1_final_x - x1, 2) + math.pow(poss1_final_y - y1, 2))

		poss2_final_x = x1 - self.RADIUS_DIAMETER / 2 + math.cos(alpha)
		poss2_final_y = y1 + self.RADIUS_DIAMETER / 2 + math.sin(alpha)
		d2 = math.sqrt(math.pow(poss2_final_x - x1, 2) + math.pow(poss2_final_y - y1, 2))

		if(d1 < d2):
			return (poss1_final_x, poss1_final_y)
		else:
			return (poss2_final_x, poss2_final_y) 


	def drawTransition(self, x1,y1,x2,y2,x3,y3):
		print "drawing transitions example"
		pen = QtGui.QPen(QtGui.QColor("black"))
		pen.setWidth(2)

		(orX,orY) = (x1,y1)#self.calculateGoodArrowPosition(x1,y1,x2,y2)
		(desX,desY) = (x3,y3)#self.calculateGoodArrowPosition(x3,y3,x2,y2)

		#left line
		self.schemaScene.addLine(orX,orY,x2,y2,pen)

		#rigth line
		line = self.schemaScene.addLine(x2,y2,desX,desY,pen).line()

		#midpoint		
		brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
		brush.setColor(QtGui.QColor("red"))
		self.schemaScene.addRect(x2-self.SQUARE_SIDE_MID, y2-self.SQUARE_SIDE_MID,
									self.SQUARE_SIDE,self.SQUARE_SIDE, pen, brush)

		#ARROWS 
		arrowSize = 7;
		angle = math.acos(line.dx()/line.length())
		if(line.dy() >=0 ):
			angle=(math.pi*2.0) - angle
		arrowP1 = line.p2() - QtCore.QPointF(math.sin(angle + math.pi / 3.0) * arrowSize,
											math.cos(angle + math.pi / 3) * arrowSize)
		arrowP2 = line.p2() - QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3.0) * arrowSize,
                                        	math.cos(angle + math.pi - math.pi / 3.0) * arrowSize)
		arrowHead = QtGui.QPolygonF()
		for point in [line.p2(), arrowP1, arrowP2]:
			arrowHead.append(point)
		brush.setColor(QtGui.QColor("black"))
		pen.setWidth(1)
		self.schemaScene.addPolygon(arrowHead, pen,brush)


	def drawTransitions(self):
		self.drawTransition(50+20,15+20,40,(15+20 + 150+20)/2, 50+20,150+20)
		self.drawTransition(50+20,15+20,50,-10, 200+20,15+20)
		self.drawTransition(200+20,15+20,100,200, 50+20,150+20)


if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	app = QtGui.QApplication(sys.argv)
	automataGui = AutomataGui(None)
	automataGui.show()
	app.exec_()
