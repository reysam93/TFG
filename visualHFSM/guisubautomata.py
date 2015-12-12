from guinode import GuiNode
from guitransition import GuiTransition

class GuiSubautomata():
	def __init__(self, id, idFather):
		self.id = id
		self.idFather = idFather
		self.nodeList = []
		self.transList = []


	#Setters

	#Getters
	def getId(self):
		return self.id


	def getIdFather(self):
		return self.idFather

	def newGuiNode(self, id, idSubSon, x, y, isInit, name):
		gnode = GuiNode(id, idSubSon, x, y, isInit, name)
		self.nodeList.append(gnode)

	def newGuiTransition(self, orig, dest, midp, idTrans, idOrig, idDest):
		transition = GuiTransition(orig, dest, midp, idTrans, idOrig, idDest)
		self.transList.append(transition)
