class GuiNode:
	def __init__(self, id, idSubSon, x, y, isInit, name):
		self.id = id
		self.idSubautSon = idSubSon
		self.x = x
		self.y = y
		self.isInit = isInit
		self.name = name
		#Creat it and draw it


	#Getters
	def getId(self):
		return self.id

	def getIdSubautomataSon(self):
		return self.idSubautSon