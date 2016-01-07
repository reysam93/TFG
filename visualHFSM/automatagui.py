#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, uic, QtCore
from treeModel import TreeModel
import sys, signal, math
from guisubautomata import GuiSubautomata
from point import Point


class AutomataGui(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		try:
			uic.loadUi('../visualHFSM/gui/mainGui.ui', self)
		except IOError:
			raise Exception("mainGui.ui doesn't found")

		self.subautomataList = []
		self.currentSubautomata = None

		self.schemaScene = QtGui.QGraphicsScene()
		self.schemaView.setScene(self.schemaScene)

		#Tree view
		self.treeModel = TreeModel()
		self.treeView.setModel(self.treeModel)

		QtCore.QObject.connect(self.upButton, QtCore.SIGNAL("clicked()"), self.upButtonClicked)
		QtCore.QObject.connect(self.treeView, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.rowClicked)


	def setAutomata(self, subautomataList):
		self.subautomataList = subautomataList


	def isFirstActiveNode(self, node):
		nodeAux = node
		subAux = self.currentSubautomata

		while nodeAux != None:
			if not nodeAux.isInit:
				return False
			idNodeFather = nodeAux.subautomata.idFather
			nodeAux = self.getNode(idNodeFather)

		return True


	def loadAutomata(self):
		self.myView = QtGui.QGraphicsView(self.schemaScene)
		for subautomata in self.subautomataList:
			self.currentSubautomata = subautomata

			for node in subautomata.nodeList:
				if node.isInit:
					self.currentSubautomata.activeNode = node.name

				if self.isFirstActiveNode(node):
					color = "green"
					node.setColor(color)
					#setActiveTreeView
				else:
					color = "white"
				self.createNewState(node, color)

			transList = subautomata.transList
			for trans in transList:
				self.createNewTransition(trans)
			
			if subautomata.idFather != 0:
				subautomata.hide()

		if self.currentSubautomata.idFather != 0:
			self.currentSubautomata = self.getRootSubautomata()


	def createNewState(self, node, color):
		if self.currentSubautomata.id == 1:
			self.treeModel.insertState(node, color)
		else:
			self.fillTreeView(node, self.treeModel.getChildren(), color)

		self.schemaScene.addItem(node.ellipse)
		self.schemaScene.addItem(node.text)
		if node.isInit:
			self.schemaScene.addItem(node.ellipseInit)


	def createNewTransition(self, trans):
		#TODO    AUTOTRANSICIONES  

		self.schemaScene.addItem(trans.leftLine)
		self.schemaScene.addItem(trans.rigthLine)
		self.schemaScene.addItem(trans.square)
		self.schemaScene.addItem(trans.arrow)


	def fillTreeView(self, node, children, color):
		added = False
		for child in children:
			if node.getIdFather() == child.id:
				self.treeModel.insertState(node, color, child)
				added = True
			else:
				added = self.fillTreeView(node, child.childItems, color)
			if added:
				break
		return added


	def getSubautomata(self, id):
		for subautomata in self.subautomataList:
			if subautomata.id == id:
				return subautomata
		return None


	def getSubautomataWithNode(self, nodeName):
		for subautomata in self.subautomataList:
			for node in subautomata.nodeList:
				if node.name == nodeName:
					return subautomata
		return None


	def getRootSubautomata(self):
		for subautomata in self.subautomataList:
			if subautomata.idFather == 0:
				return subautomata


	def getNode(self, nodeId):
		for subautomata in self.subautomataList:
			for node in subautomata.nodeList:
				if nodeId == node.id:
					return node

		return None


	def changeCurrentSubautomata(self, id):
		self.currentSubautomata.hide()
		self.currentSubautomata = self.getSubautomata(id)
		self.currentSubautomata.show()


	def upButtonClicked(self):
		fatherId = self.currentSubautomata.idFather 
		if fatherId != 0:
			nodeFather = self.getNode(fatherId)
			self.changeCurrentSubautomata(nodeFather.subautomata.id)
		else:
			print "This subautomata does not have any parent"


	def rowClicked(self, index):
		node = self.getNode(index.internalPointer().id)
		if self.currentSubautomata.id != node.subautomata.id:
			self.changeCurrentSubautomata(node.subautomata.id)


	def setActiveTreeView(self, node, isActive, children):
		finded = False

		for child in children:
			if finded:
				break

			if child.name == node.name:
				if isActive:
					child.color = "green"
				else:
					child.color = "pink"
				finded = True
			
			else:
				finded = self.setActiveTreeView(node, isActive, child.getChildren())

				#TODO  AUTOFOCUS!!!



	def setNodeAsActive(self, node, subautomata, isActive):
		#CONDICIONES DE CARRERA!!
		if isActive:
			subautomata.activeNode = node.name
			node.setColor("green")
		else:
			node.setColor("pink")
			
		self.setActiveTreeView(node, isActive, self.treeModel.getChildren())

		if node.idSubautSon != 0:
			subSon = self.getSubautomata(node.idSubautSon)
			lastActiveNode = subSon.getNodeByName(subSon.activeNode)
			self.setNodeAsActive(lastActiveNode, subSon, isActive)


	def notifySetNodeAsActive(self, nodeName):
		subAux = self.getSubautomataWithNode(nodeName)
		nodeAux = subAux.getNodeByName(subAux.activeNode)		

		if nodeAux != None:
			self.setNodeAsActive(nodeAux, subAux, False)

		nodeAux = subAux.getNodeByName(nodeName)
		self.setNodeAsActive(nodeAux, subAux, True)



















