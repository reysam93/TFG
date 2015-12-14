from PyQt4 import QtGui
from PyQt4 import QtCore
import math


#CONST
SQUARE_SIDE = 10
ARROW_SIZE = 7


class GuiTransition():
	def __init__(self, orig, dest, midp, id, idOrig, idDest):
		self.orig = orig
		self.dest = dest
		self.midp = midp
		self.id = id
		self.idOrig = idOrig
		self.idDest = idDest

		#CREATE GUI ELEMENTS
		self.pen = QtGui.QPen(QtGui.QColor("black"))
		self.squareBrush = QtGui.QBrush(QtCore.Qt.SolidPattern)
		self.squareBrush.setColor(QtGui.QColor("red"))
		self.arrowBrush = QtGui.QBrush(QtCore.Qt.SolidPattern)
		self.arrowBrush.setColor(QtGui.QColor("black"))

		self.leftLine = QtCore.QLineF(orig.x, orig.y, midp.x, midp.y)
		self.rigthLine = QtCore.QLineF(midp.x, midp.y, dest.x, dest.y)
		self.square = QtCore.QRectF(midp.x - SQUARE_SIDE/2, midp.y - SQUARE_SIDE/2,
											SQUARE_SIDE, SQUARE_SIDE)

		#ARROW
		angle = math.acos(self.rigthLine.dx()/self.rigthLine.length())
		if (self.rigthLine.dy() >= 0):
			angle = (math.pi*2.0) - angle

		arrowP1 = self.rigthLine.p2() - QtCore.QPointF(math.sin(angle + math.pi / 3.0) * ARROW_SIZE,
											math.cos(angle + math.pi / 3) * ARROW_SIZE)
		arrowP2 = self.rigthLine.p2() - QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3.0) * ARROW_SIZE,
                                        	math.cos(angle + math.pi - math.pi / 3.0) * ARROW_SIZE)
		self.arrow = QtGui.QPolygonF()
		
		for point in [self.rigthLine.p2(), arrowP1, arrowP2]:
			self.arrow.append(point)