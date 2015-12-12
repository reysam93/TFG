class GuiTransition():
	def __init__(self, orig, dest, midp, id, idOrig, idDest):
		self.orig = orig
		self.dest = dest
		self.midp = midp
		self.id = id
		self.idOrig = idOrig
		self.idDest = idDest


	def getId(self):
		return self.id

	def getIdOrigin(self):
		return self.idOrig

	def getIdDestiny(self):
		return self.idDest