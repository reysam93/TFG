from guinode import GuiNode
from guitransition import GuiTransition

class GuiSubautomata():
	def __init__(self, id, idFather, automataGui):
		self.id = id
		self.idFather = idFather
		self.automataGui = automataGui
		self.activeNode = ""
		self.nodeList = []
		self.transList = []


	def newGuiNode(self, id, idSubSon, x, y, isInit, name):
		gnode = GuiNode(id, idSubSon, self, x, y, isInit, name)
		self.nodeList.append(gnode)


	def newGuiTransition(self, orig, dest, midp, idTrans, idOrig, idDest):
		transition = GuiTransition(orig, dest, midp, idTrans, idOrig, idDest)
		self.transList.append(transition)


	def show(self):
		for node in self.nodeList:
			node.show()

		for transition in self.transList:
			transition.show()


	def hide(self):
		for node in self.nodeList:
			node.hide()

		for transition in self.transList:
			transition.hide()


	def getNode(self, id):
		for node in self.nodeList:
			if node.id == id:
				return node
		return None


	def getNodeByName(self, name):
		for node in self.nodeList:
			if node.name == name:
				return node
		return None