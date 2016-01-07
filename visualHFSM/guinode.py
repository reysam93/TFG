from PyQt4 import QtGui
from PyQt4 import QtCore


#CONST
NODE_WIDTH = 40
INIT_WIDTH = 30
PEN_NORMAL_WIDTH = 1
PEN_FOCUS_WIDTH = 3


class GuiNode():
	class State(QtGui.QGraphicsEllipseItem):
		def __init__(self, state, x, y, width):
			QtGui.QGraphicsEllipseItem.__init__(self, x, y, width, width)
			self.setAcceptHoverEvents(True)
			self.state = state


		def hoverEnterEvent(self, event):
			self.state.setWidth(PEN_FOCUS_WIDTH)


		def hoverLeaveEvent(self, event):
			self.state.setWidth(PEN_NORMAL_WIDTH)


		def mouseDoubleClickEvent(self, event):
			self.state.notifyChangeCurrentSubautomata(self.state.idSubautSon)


	def __init__(self, id, idSubSon, subautomata, x, y, isInit, name):
		self.id = id
		self.idSubautSon = idSubSon
		self.subautomata = subautomata
		self.x = x - NODE_WIDTH/2
		self.y = y - NODE_WIDTH/2
		self.isInit = isInit
		self.name = name

		#CREATE GUI ELEMENTS
		self.ellipse = self.State(self, self.x, self.y, NODE_WIDTH)
		self.text = QtGui.QGraphicsSimpleTextItem(self.name)
		self.text.setPos(self.x, self.y+NODE_WIDTH)
		if self.isInit:
			self.ellipseInit = QtGui.QGraphicsEllipseItem(self.x+5, self.y+5, 
									INIT_WIDTH, INIT_WIDTH)
		self.paint("blue", PEN_NORMAL_WIDTH)


	def getIdFather(self):
		return self.subautomata.idFather

	def show(self):
		self.ellipse.show()
		self.text.show()
		if self.isInit:
			self.ellipseInit.show()


	def hide(self):
		self.ellipse.hide()
		self.text.hide()
		if self.isInit:
			self.ellipseInit.hide()


	def setWidth(self, width):
		pen = QtGui.QPen(QtGui.QColor("black"), width)
		self.ellipse.setPen(pen)
		if self.isInit:
			self.ellipseInit.setPen(pen)


	def setColor(self, color):
		self.paint(color, PEN_NORMAL_WIDTH)


	def paint(self, color, width):
		pen = QtGui.QPen(QtGui.QColor("black"), width)
		brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
		brush.setColor(QtGui.QColor(color))
		self.ellipse.setPen(pen)
		self.ellipse.setBrush(brush)


	def notifyChangeCurrentSubautomata(self, idNewSub):
		if idNewSub != 0:
			self.subautomata.automataGui.changeCurrentSubautomata(idNewSub)
		else:
			print "This node does not have any subautomata son"