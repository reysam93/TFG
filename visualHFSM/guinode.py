from PyQt4 import QtGui
from PyQt4 import QtCore


#CONST
NODE_WIDTH = 40
INIT_WIDTH = 30


class GuiNode:
	def __init__(self, id, idSubSon, x, y, isInit, name):
		self.id = id
		self.idSubautSon = idSubSon
		self.x = x - NODE_WIDTH/2
		self.y = y - NODE_WIDTH/2
		self.isInit = isInit
		self.name = name

		#CREATE GUI ELEMENTS
		self.pen = QtGui.QPen(QtGui.QColor("black"))
		self.brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
		self.brush.setColor(QtGui.QColor("blue"))

		self.ellipse = QtGui.QGraphicsEllipseItem(self.x, self.y, 
									NODE_WIDTH, NODE_WIDTH)

		self.text = QtGui.QGraphicsSimpleTextItem(self.name, self.ellipse)
		self.text.setPos(self.x, self.y+NODE_WIDTH)

		if self.isInit:
			self.ellipseInit = QtGui.QGraphicsEllipseItem(self.x+5, self.y+5, 
									INIT_WIDTH, INIT_WIDTH)