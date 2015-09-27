/*
 *  Copyright (C) 1997-2013 JDERobot Developers Team
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Library General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, see <http://www.gnu.org/licenses/>.
 *
 *  Authors : Borja Menéndez Moreno <b.menendez.moreno@gmail.com>
 *            José María Cañas Plaza <jmplaza@gsyc.es>
 *
 */

#include "generate.h"

/*************************************************************
 * CONSTRUCTOR
 *************************************************************/
Generate::Generate ( std::list<SubAutomata> subautomataList, std::string cpppath,
										std::string cfgpath, std::string cmakepath,
										std::list<IceInterface>* listInterfaces,
										std::map<std::string, std::string> mapInterfacesHeader,
										std::list<std::string> listLibraries ) {
	this->subautomataList = subautomataList;
	this->path = cpppath;
	this->cfgpath = cfgpath;
	this->cmakepath = cmakepath;
	this->listInterfaces = listInterfaces;
	this->mapInterfacesHeader = mapInterfacesHeader;
	this->listLibraries = listLibraries;

	this->mapTab[T_ZERO] = std::string();
	this->mapTab[T_ONE] = std::string("\t");
	this->mapTab[T_TWO] = std::string("\t\t");
	this->mapTab[T_THREE] = std::string("\t\t\t");
	this->mapTab[T_FOUR] = std::string("\t\t\t\t");
	this->mapTab[T_FIVE] = std::string("\t\t\t\t\t");
	this->mapTab[T_SIX] = std::string("\t\t\t\t\t\t");
}

/*************************************************************
 * DESTRUCTOR
 *************************************************************/
Generate::~Generate () {}

/*************************************************************
 * ANOTHER FUNCTIONS
 *************************************************************/
int Generate::init () {
	this->fs.open(this->path.c_str(), std::fstream::out);
	if (this->fs.is_open()) {
		this->generateHeaders();
		this->generateEnums();
		this->generateVariables();
		this->generateFunctions();
		this->generateCreateGuiSubautomataList();
		this->generateSubautomatas();
		this->generateAutomataGui();
		this->generateMain();
		this->fs.close();

		this->fs.open(this->cfgpath.c_str(), std::fstream::out);
		if (this->fs.is_open()) {
			this->generateCfg();
			this->fs.close();
		}
		
		this->fs.open(this->cmakepath.c_str(), std::fstream::out);
		if (this->fs.is_open()) {
			this->generateCmake();
			this->fs.close();
		}
		return 0;
	} else
		return 1;
}

int Generate::init_py (){
	this->fs.open(this->path.c_str(), std::fstream::out);
	if (this->fs.is_open()){
		this->generateHeaders_py();
		this->generateMain_py()
	}
}

void Generate::generateHeaders () {
	this->generateGenericHeaders();
	this->generateSpecificHeaders();
}

void Generate::generateHeaders_py (){
	this->fs << "#!/usr/bin/python" << std::endl;
	this->fs << "# -*- coding: utf-8 -*-" << std::endl;
	this->fs << std::endl;

	this->generateGenericHeaders_py();
	this->generateSpecificHeaders_py();
}

void Generate::generateGenericHeaders () {
	this->fs << "#include <Ice/Ice.h>" << std::endl;
	this->fs << "#include <IceUtil/IceUtil.h>" << std::endl;
	this->fs << "#include \"../visualHFSM/automatagui.h\"" << std::endl;
	this->fs << std::endl;
	for ( std::list<std::string>::iterator listLibsIterator = this->listLibraries.begin();
			listLibsIterator != this->listLibraries.end(); listLibsIterator++ )
		this->fs << "#include <" << *listLibsIterator << ">" << std::endl;
	this->fs << std::endl;
	this->fs.flush();
}

void Generate::generateGenericHeaders_py (){
	this->fs << "import sys, Ice" << std::endl;;
	//AUTOMATAGUI
	this->fs << std::endl;
	for ( std::list<std::string>::iterator listLibsIterator = this->listLibraries.begin();
		listLibsIterator != this->listLibraries.end(); listLibsIterator++ )
		this->fs << "import " << *listLibsIterator << std::endl;
	this->fs << std::endl;
	this->fs.flush();
}

void Generate::generateSpecificHeaders () {
	for ( std::list<IceInterface>::iterator listInterfacesIterator = this->listInterfaces->begin();
			listInterfacesIterator != this->listInterfaces->end(); listInterfacesIterator++ )
		this->fs << "#include <jderobot/" << this->mapInterfacesHeader[listInterfacesIterator->getInterface()] << ".h>" << std::endl;

	this->fs << std::endl;
	this->fs.flush();
}

void Generate::generateSpecificHeaders_py (){
	;
}

void Generate::generateEnums () {
	for ( std::list<SubAutomata>::iterator subListIterator = this->subautomataList.begin();
            subListIterator != this->subautomataList.end(); subListIterator++ ) {
		int id = subListIterator->getId();

		this->fs << "typedef enum State_Sub_" << id << " {" << std::endl;
		std::list<Node> nodeList = subListIterator->getNodeList();
		for ( std::list<Node>::iterator nodeListIterator = nodeList.begin();
				nodeListIterator != nodeList.end(); nodeListIterator++ ) {
			if (id != 1) {
				this->fs << "\t" << nodeListIterator->getName() << "," << std::endl;
				this->fs << "\t" << nodeListIterator->getName() << "_ghost," << std::endl;
			} else
				this->fs << "\t" << nodeListIterator->getName() << "," << std::endl;
		}
		this->fs << "} State_Sub_" << id << ";" << std::endl;
		
		this->fs << std::endl;

		this->fs << "const char* Names_Sub_" << id << "[] = {" << std::endl;
		for ( std::list<Node>::iterator nodeListIterator = nodeList.begin();
				nodeListIterator != nodeList.end(); nodeListIterator++ ) {
			this->fs << "\t\"" << nodeListIterator->getName() << "\"," << std::endl;
			if (id != 1) {
				std::string ghost = std::string(nodeListIterator->getName() + "_ghost");
				this->fs << "\t\"" << ghost << "\"," << std::endl;
			}
		}
		this->fs << "};" << std::endl;

		this->fs << std::endl;
		this->fs.flush();
	}
}

void Generate::generateVariables () {
	for ( std::list<SubAutomata>::iterator subListIterator = this->subautomataList.begin();
            subListIterator != this->subautomataList.end(); subListIterator++ )
		this->fs << "pthread_t thr_sub_" << subListIterator->getId() << ";" << std::endl;
	this->fs << "pthread_t thr_automatagui;" << std::endl;
	this->fs << std::endl;
	this->fs << "AutomataGui *automatagui;" << std::endl;
	this->fs << "bool displayAutomataGui;" << std::endl;
	this->fs << std::endl;
	for ( std::list<SubAutomata>::iterator subListIterator = this->subautomataList.begin();
            subListIterator != this->subautomataList.end(); subListIterator++ ) {
		int id = subListIterator->getId();

		std::list<Node> nodeList = subListIterator->getNodeList();
		std::list<Node>::iterator nodeListIterator = nodeList.begin();
		while ( (!nodeListIterator->isInitial()) &&
				(nodeListIterator != nodeList.end()) )
			nodeListIterator++;

		std::string nameState;
		if (id != 1)
			nameState = std::string(nodeListIterator->getName() + "_ghost");
		else
			nameState = std::string(nodeListIterator->getName());

		this->fs << "State_Sub_" << id << " sub_" << id << " = " << nameState.c_str() << ";" << std::endl;
	}
	this->fs << std::endl;
	this->fs.flush();

	for ( std::list<IceInterface>::iterator listInterfacesIterator = this->listInterfaces->begin();
			listInterfacesIterator != this->listInterfaces->end(); listInterfacesIterator++ )
		this->fs << "jderobot::" << listInterfacesIterator->getInterface() << "Prx " << listInterfacesIterator->getName() << "prx;" << std::endl;
	this->fs << std::endl;
	this->fs.flush();
}
	
void Generate::generateFunctions () {
	for ( std::list<SubAutomata>::iterator subListIterator = this->subautomataList.begin();
            subListIterator != this->subautomataList.end(); subListIterator++ ) {		
		this->fs << subListIterator->getFunctions() << std::endl;
		this->fs << std::endl;
		this->fs.flush();
	}
}

void Generate::generateCreateGuiSubautomataList(){
	this->fs << "std::list<GuiSubautomata> createGuiSubAutomataList(){" << std::endl;
	this->fs << "\tstd::list<GuiSubautomata> guiSubautomataList;" << std::endl;
	this->fs << std::endl;

	for ( std::list<SubAutomata>::iterator subListIterator = this->subautomataList.begin();
		subListIterator != this->subautomataList.end(); subListIterator++ ) {
		int subId = subListIterator->getId();
		int subIdFather = subListIterator->getIdFather();
		std:: stringstream ssub;
		ssub << "guiSubautomata" << subId;
		this->fs << "\tGuiSubautomata* " << ssub.str() << " = new GuiSubautomata(" << subId << ", " << subIdFather << ");" << std::endl;
		this->fs << std::endl;

		std::list<Node> nodeList = subListIterator->getNodeList();
		std::list<Node>::iterator nodeListIterator = nodeList.begin();
		while (nodeListIterator != nodeList.end()){
			int nodeId = nodeListIterator->getId();
			int sonId = nodeListIterator->getIdSubautomataSon();
			Point* point = subListIterator->getNodePoint(nodeId);
			float x = point->getX();
			float y = point->getY();
			bool isInit = nodeListIterator->isInitial();
			std::string nodeName = nodeListIterator->getName();
			this->fs << "\t" << ssub.str() << "->newGuiNode(" << nodeId << ", " << sonId << ", " << x << ", " << y << ");" << std::endl;
			this->fs << "\t" << ssub.str() << "->setIsInitialLastGuiNode(" << isInit << ");" << std::endl;
			this->fs << "\t" << ssub.str() << "->setNameLastGuiNode(\"" << nodeName << "\");" << std::endl;
			this->fs << std::endl;
			nodeListIterator++;
		}

		std::list<Transition> transList = subListIterator->getTransList();
        std::list<Transition>::iterator transListIterator = transList.begin();
        while (transListIterator != transList.end()){
        	int transId = transListIterator->getId();
        	int originId = transListIterator->getIdOrigin();
        	int destinyId = transListIterator->getIdDestiny();
        	Point* origin = subListIterator->getNodePoint(originId);
        	Point* destiny = subListIterator->getNodePoint(destinyId);
        	Point* mid = subListIterator->getTransPoint(transId);
        	std::stringstream sorigin;
        	sorigin << "origin" << subId << transId;
        	std::stringstream sdest;
        	sdest << "destiny" << subId << transId;
        	std::stringstream smid;
        	smid << "midPoint" << subId << transId;
        	this->fs << "\tPoint* " << sorigin.str() << " = new Point(" << origin->getX() << ", " << origin->getY() << ");" << std::endl;
        	this->fs << "\tPoint* " << sdest.str() << " = new Point(" << destiny->getX() << ", " << destiny->getY() << ");" << std::endl;
        	this->fs << "\tPoint* " << smid.str() << " = new Point(" << mid->getX() << ", " << mid->getY() << ");" << std::endl;
			this->fs << "\t" << ssub.str() << "->newGuiTransition(*" << sorigin.str() << ", *" << sdest.str() << ", *" << smid.str() << 
				", " << transId << ", " <<  originId << ", " << destinyId << ");" << std::endl;
			this->fs << std::endl;
			transListIterator++;
		}

		this->fs << "\tguiSubautomataList.push_back(*" << ssub.str() << ");" << std::endl;
        this->fs << std::endl;
	}

	this->fs << "\treturn guiSubautomataList;" << std::endl;
	this->fs << "}" << std::endl;
	this->fs << std::endl;
}


void Generate::generateSubautomatas () {
	for ( std::list<SubAutomata>::iterator subListIterator = this->subautomataList.begin();
            subListIterator != this->subautomataList.end(); subListIterator++ ) {
       	int id = subListIterator->getId();		
		this->fs << "void* subautomata_" << id << " ( void* ) {" << std::endl;
		this->fs << "\tstruct timeval a, b;" << std::endl;
		this->fs << "\tint cycle = " << subListIterator->getTime() << ";" << std::endl;
		this->fs << "\tlong totala, totalb;" << std::endl;
		this->fs << "\tlong diff;" << std::endl;
		this->fs << "\ttime_t t_ini;" << std::endl;
		this->fs << "\ttime_t t_fin;" << std::endl;
		this->fs << "\tdouble secs;" << std::endl;
		this->fs << "\tbool t_activated;" << std::endl;
		this->fs << std::endl;

		int countNodes = 0;
		std::list<Node> nodeList = subListIterator->getNodeList();
		for ( std::list<Node>::iterator nodeListIterator = nodeList.begin();
				nodeListIterator != nodeList.end(); nodeListIterator++ )
			countNodes++;

		std::map<std::string, float> mapNameTime;
		std::list<Transition> transList = subListIterator->getTransList();
		if (id != 1) {
			for ( std::list<Transition>::iterator transListIterator = transList.begin();
					transListIterator != transList.end(); transListIterator++ )	{
				int idorigin = transListIterator->getIdOrigin();
				if (transListIterator->getType().compare("time") == 0) {
					std::list<Node>::iterator nodeListIterator = nodeList.begin();
					while ( (nodeListIterator->getId() != idorigin) &&
							(nodeListIterator != nodeList.end()) )
						nodeListIterator++;

					float ms = atof(transListIterator->getCodeTrans().c_str());
					this->fs << mapTab[T_ONE] << "float t_" << nodeListIterator->getName() << "_max = " << (ms/1000.0) << ";" << std::endl;

					mapNameTime[nodeListIterator->getName()] = ms/1000.0;
				}
			}	
		}

		std::istringstream f(subListIterator->getVariables());
		std::string line;
		while (std::getline(f, line))
			this->fs << "\t" << line << std::endl;
		this->fs << std::endl;

		this->fs << "\twhile (true) {" << std::endl;
		this->fs << "\t\tgettimeofday(&a, NULL);" << std::endl;
		this->fs << "\t\ttotala = a.tv_sec * 1000000 + a.tv_usec;" << std::endl;
		this->fs << std::endl;

		if (id != 1) {
			int idfather = subListIterator->getIdFather();

			std::list<SubAutomata>::iterator subFatherListIterator = this->subautomataList.begin();
			while ( (subFatherListIterator->getId() != idfather) &&
					(subFatherListIterator != this->subautomataList.end()) )
				subFatherListIterator++;
			
			std::list<Node> nodeFatherList = subFatherListIterator->getNodeList();
			std::list<Node>::iterator nodeFatherListIterator = nodeFatherList.begin();
			while ( (nodeFatherListIterator->getIdSubautomataSon() != id) &&
					(nodeFatherListIterator != nodeFatherList.end()) )
				nodeFatherListIterator++;

			this->fs << "\t\tif (sub_" << idfather << " == " << nodeFatherListIterator->getName() << ") {" << std::endl;
			this->fs << "\t\t\tif (";

			int count = 0;
			for ( std::list<Node>::iterator nodeListIterator = nodeList.begin();
					nodeListIterator != nodeList.end(); nodeListIterator++ ) {
				this->fs << " sub_" << id << " == " << nodeListIterator->getName() + "_ghost";
				count++;
				if (count != countNodes) {
					this->fs << " ||";
				}
			}
			this->fs << ") {" << std::endl;

			this->fs << "\t\t\t\tsub_" << id << " = (State_Sub_" << id << ")(sub_" << id << " - 1);" << std::endl;
			this->fs << "\t\t\t\tt_ini = time(NULL);" << std::endl;
			this->fs << "\t\t\t}" << std::endl;
		}

		this->fs << "\t\t// Evaluation switch" << std::endl;
		this->fs << "\t\tswitch (sub_" << id << ") {" << std::endl;
		for ( std::list<Node>::iterator nodeListIterator = nodeList.begin();
				nodeListIterator != nodeList.end(); nodeListIterator++ ) {
			int idNode = nodeListIterator->getId();
			this->fs << "\t\t\tcase " << nodeListIterator->getName() << ": {" << std::endl;
			
			for ( std::list<Transition>::iterator transListIterator = transList.begin();
					transListIterator != transList.end(); transListIterator++ ) {
				if (transListIterator->getIdOrigin() == idNode) {
					int idDestiny = transListIterator->getIdDestiny();
					int idOrigin = transListIterator->getIdOrigin();
					if (transListIterator->getType().compare("condition") == 0) {
						this->fs << "\t\t\t\tif (" << transListIterator->getCodeTrans().c_str() << ") {" << std::endl;
						this->fs << "\t\t\t\t\tsub_" << id << " = " << subListIterator->getNodeName(idDestiny) << ";" << std::endl;
						std::istringstream f(transListIterator->getCode());
						std::string line;
						while (std::getline(f, line))
							this->fs << "\t\t\t\t\t\t" << line << std::endl;
						this->fs << "\t\t\t\t\tautomatagui->setNodeAsActive_Locked(\"" << subListIterator->getNodeName(idOrigin) << "\", false);" << std::endl;
						this->fs << "\t\t\t\t\tautomatagui->setNodeAsActive_Locked(\"" << subListIterator->getNodeName(idDestiny) << "\", true);" << std::endl;
						this->fs << "\t\t\t\t}" << std::endl;
					} else {
						this->fs << "\t\t\t\tif (!t_activated) {" << std::endl;
						this->fs << "\t\t\t\t\tt_ini = time(NULL);" << std::endl;
						this->fs << "\t\t\t\t\tt_activated = true;" << std::endl;
						this->fs << "\t\t\t\t} else {" << std::endl;
						this->fs << "\t\t\t\t\tt_fin = time(NULL);" << std::endl;
						this->fs << "\t\t\t\t\tsecs = difftime(t_fin, t_ini);" << std::endl;
						if (id == 1) {
							float ms = atof(transListIterator->getCodeTrans().c_str());
							this->fs << "\t\t\t\t\tif (secs > (double) " << (ms / 1000.0) << ") {" << std::endl;
						} else
							this->fs << "\t\t\t\t\tif (secs > (double) t_" << subListIterator->getNodeName(idNode) << "_max) {" << std::endl;
						this->fs << "\t\t\t\t\t\tsub_" << id << " = " << subListIterator->getNodeName(idDestiny) << ";" << std::endl;
						this->fs << "\t\t\t\t\t\tt_activated = false;" << std::endl;
						std::istringstream f(transListIterator->getCode());
						std::string line;
						while (std::getline(f, line))
							this->fs << "\t\t\t\t\t\t" << line << std::endl;
						this->fs << "\t\t\t\t\t\tautomatagui->setNodeAsActive_Locked(\"" << subListIterator->getNodeName(idOrigin) << "\", false);" << std::endl;
						this->fs << "\t\t\t\t\t\tautomatagui->setNodeAsActive_Locked(\"" << subListIterator->getNodeName(idDestiny) << "\", true);" << std::endl;
						if (id != 1)
							this->fs << "\t\t\t\t\t\tt_" << subListIterator->getNodeName(idNode) << "_max = " << mapNameTime[subListIterator->getNodeName(idNode)] << ";" << std::endl;
						this->fs << "\t\t\t\t\t}" << std::endl;
						this->fs << "\t\t\t\t}" << std::endl;
					}
					this->fs << std::endl;
				}
			}
			this->fs << "\t\t\t\tbreak;" << std::endl;
			this->fs << "\t\t\t}" << std::endl;
			this->fs.flush();
		}
		this->fs << "\t\t}" << std::endl;
		this->fs << std::endl;

		this->fs << "\t\t// Actuation switch" << std::endl;
		this->fs << "\t\tswitch (sub_" << id << ") {" << std::endl;
		for ( std::list<Node>::iterator nodeListIterator = nodeList.begin();
				nodeListIterator != nodeList.end(); nodeListIterator++ ) {
			this->fs << "\t\t\tcase " << nodeListIterator->getName() << ": {" << std::endl;
			std::istringstream f(nodeListIterator->getCode());
			std::string line;
			while (std::getline(f, line))
				this->fs << "\t\t\t\t" << line << std::endl;
			this->fs << "\t\t\t\tbreak;" << std::endl;
			this->fs << "\t\t\t}" << std::endl;
			this->fs.flush();
		}
		this->fs << "\t\t}" << std::endl;
		if (id != 1) {
			this->fs << "\t\t} else {" << std::endl;
			this->fs << "\t\t\tswitch (sub_" << id << ") {" << std::endl;
			for ( std::list<Node>::iterator nodeListIterator = nodeList.begin();
					nodeListIterator != nodeList.end(); nodeListIterator++ ) {
				if (mapNameTime.find(nodeListIterator->getName()) != mapNameTime.end()) {
					this->fs << "\t\t\t\tcase " << nodeListIterator->getName() << ":" << std::endl;
					this->fs << "\t\t\t\t\tt_" << nodeListIterator->getName() << "_max = " << mapNameTime[nodeListIterator->getName()] << " - difftime(t_fin, t_ini);" << std::endl;
					this->fs << "\t\t\t\t\tsub_" << id << " = (State_Sub_" << id << ")(sub_" << id << " + 1);" << std::endl;
					this->fs << "\t\t\t\t\tbreak;" << std::endl;
				} 
			}
			this->fs << "\t\t\t\tdefault:" << std::endl;
			this->fs << "\t\t\t\t\tbreak;" << std::endl;
			this->fs << "\t\t\t}" << std::endl;
			this->fs << "\t\t}" << std::endl;
		}
		this->fs << std::endl;

		this->fs << "\t\tgettimeofday(&b, NULL);" << std::endl;
		this->fs << "\t\ttotalb = b.tv_sec * 1000000 + b.tv_usec;" << std::endl;
		this->fs << "\t\tdiff = (totalb - totala) / 1000;" << std::endl;
		this->fs << "\t\tif (diff < 0 || diff > cycle)" << std::endl;
		this->fs << "\t\t\tdiff = cycle;" << std::endl;
		this->fs << "\t\telse" << std::endl;
		this->fs << "\t\t\tdiff = cycle - diff;" << std::endl;
		this->fs << std::endl;
		this->fs << "\t\tusleep(diff * 1000);" << std::endl;
		this->fs << "\t\tif (diff < 33 )" << std::endl;
		this->fs << "\t\t\tusleep (33 * 1000);" << std::endl;

		this->fs << "\t}" << std::endl;
		this->fs << "}" << std::endl;

		this->fs << std::endl;
		this->fs.flush();
	}
}

void Generate::generateAutomataGui () {
	this->fs << "void* runAutomatagui (void*) {" << std::endl;
	this->fs << "\tautomatagui->run();" << std::endl;
	this->fs << "}" << std::endl;
	this->fs << std::endl;
	this->fs << "bool showAutomataGui () {" << std::endl;
	this->fs << "\tif (automatagui->init() < 0){" << std::endl;
	this->fs << "\t\tstd::cerr << \"warning: could not show automatagui\" << std::endl;" << std::endl;
	this->fs << "\t\treturn false;" << std::endl;
	this->fs << "\t}" << std::endl;
	this->fs << "\tautomatagui->setGuiSubautomataList(createGuiSubAutomataList());" << std::endl;
	this->fs << "\tpthread_create(&thr_automatagui, NULL, &runAutomatagui, NULL);" << std::endl;
	this->fs << "\tautomatagui->loadGuiSubautomata();" << std::endl;
	this->fs << "\treturn true;" << std::endl;
	this->fs << "}" << std::endl;
	this->fs << std::endl;
}

void Generate::generateMain () {
	this->fs << "int main (int argc, char* argv[]) {" << std::endl;
	this->fs << "\tint status;" << std::endl;
	this->fs << "\tIce::CommunicatorPtr ic;" << std::endl;
	this->fs << std::endl;
	this->fs << "\ttry {" << std::endl;
	this->fs << "\t\tic = Ice::initialize(argc, argv);" << std::endl;
	this->fs << std::endl;

	for ( std::list<IceInterface>::iterator listInterfacesIterator = this->listInterfaces->begin();
			listInterfacesIterator != this->listInterfaces->end(); listInterfacesIterator++ ) {
		this->fs << "\t\t// Contact to " << listInterfacesIterator->getName() << std::endl;
		this->fs << "\t\tIce::ObjectPrx " << listInterfacesIterator->getName() << " = ic->propertyToProxy(\"automata." << listInterfacesIterator->getName() << ".Proxy\");" << std::endl;
		this->fs << "\t\tif (" << listInterfacesIterator->getName() << " == 0)" << std::endl;
		this->fs << "\t\t\tthrow \"Could not create proxy with " << listInterfacesIterator->getName() << "\";" << std::endl;
		this->fs << "\t\t" << listInterfacesIterator->getName() << "prx = jderobot::" << listInterfacesIterator->getInterface() << "Prx::checkedCast(" << listInterfacesIterator->getName() << ");" << std::endl;
		this->fs << "\t\tif (" << listInterfacesIterator->getName() << "prx == 0)" << std::endl;
		this->fs << "\t\t\tthrow \"Invalid proxy automata." << listInterfacesIterator->getName() << ".Proxy\";" << std::endl;
		this->fs << "\t\tstd::cout << \"" << listInterfacesIterator->getName() << " connected\" << std::endl;" << std::endl;
		this->fs << std::endl;
	}
	this->fs << "\t\tautomatagui = new AutomataGui(argc, argv);" << std::endl;
	this->fs << "\t\tdisplayAutomataGui = showAutomataGui();" << std::endl;
	this->fs.flush();

	for ( std::list<SubAutomata>::iterator subListIterator = this->subautomataList.begin();
            subListIterator != this->subautomataList.end(); subListIterator++ ) {
		int id = subListIterator->getId();
		this->fs << "\t\tpthread_create(&thr_sub_" << id << ", NULL, &subautomata_" << id << ", NULL);" << std::endl;
	}
	this->fs << std::endl;

	for ( std::list<SubAutomata>::iterator subListIterator = this->subautomataList.begin();
            subListIterator != this->subautomataList.end(); subListIterator++ ) {
		int id = subListIterator->getId();
		this->fs << "\t\tpthread_join(thr_sub_" << id << ", NULL);" << std::endl;
	}
	this->fs << "\t\tif (displayAutomataGui)" << std::endl;
	this->fs << "\t\t\tpthread_join(thr_automatagui, NULL);" << std::endl;
	this->fs << std::endl;

	this->fs.flush();

	this->fs << this->mapTab[T_ONE] << "} catch ( const Ice::Exception& ex ) {" << std::endl;
	this->fs << this->mapTab[T_TWO] << "std::cerr << ex << std::endl;" << std::endl;
	this->fs << this->mapTab[T_TWO] << "status = 1;" << std::endl;
	this->fs << this->mapTab[T_ONE] << "} catch ( const char* msg ) {" << std::endl;
	this->fs << this->mapTab[T_TWO] << "std::cerr << msg << std::endl;" << std::endl;
	this->fs << this->mapTab[T_TWO] << "status = 1;" << std::endl;
	this->fs << this->mapTab[T_ONE] << "}" << std::endl;
	this->fs << std::endl;
	this->fs << this->mapTab[T_ONE] << "if (ic)" << std::endl;
	this->fs << this->mapTab[T_TWO] << "ic->destroy();" << std::endl;
	this->fs << std::endl;
	this->fs << this->mapTab[T_ONE] << "return status;" << std::endl;
	this->fs << "}" << std::endl;

	this->fs.flush();
}

void Generate::generateMain_py (){
	this->fs << "if __name__ == '__main__':" << std::endl;
	this->fs << "\tprint \"HOLA PYTHON!\"" << std::endl;
}

void Generate::generateCfg () {
	for ( std::list<IceInterface>::iterator listInterfacesIterator = this->listInterfaces->begin();
			listInterfacesIterator != this->listInterfaces->end(); listInterfacesIterator++ )
		this->fs << "automata." << listInterfacesIterator->getName() << ".Proxy=" << listInterfacesIterator->getName() << ":default -h " << listInterfacesIterator->getIp() << " -p " << listInterfacesIterator->getPort() << std::endl;
	this->fs.flush();
}

void Generate::generateCmake () {
	this->fs << "project (AUTOMATA)" << std::endl;
	this->fs << std::endl;
	this->fs << "cmake_minimum_required(VERSION 2.8)" << std::endl;
	this->fs << "include(FindPkgConfig)" << std::endl;
	this->fs << std::endl;
	this->fs << "SET( SOURCE_FILES_AUTOMATA " << std::endl;
	this->fs << "\t" << this->getCppName() << std::endl;
	this->fs << "\t../visualHFSM/automatagui.cpp" << std::endl;
	this->fs << "\t../visualHFSM/point.cpp" << std::endl;
	this->fs << "\t../visualHFSM/node.cpp" << std::endl;
	this->fs << "\t../visualHFSM/transition.cpp" << std::endl;
	this->fs << "\t../visualHFSM/subautomata.cpp" << std::endl;
	this->fs << "\t../visualHFSM/guinode.cpp" << std::endl;
	this->fs << "\t../visualHFSM/guitransition.cpp" << std::endl;
	this->fs << "\t../visualHFSM/guisubautomata.cpp" << std::endl;
	this->fs << "\t../visualHFSM/popups/editnodedialog.cpp" << std::endl;
	this->fs << "\t../visualHFSM/popups/edittransitiondialog.cpp" << std::endl;
	this->fs << "\t../visualHFSM/popups/edittransitioncodedialog.cpp" << std::endl;
	this->fs << "\t../visualHFSM/popups/renamedialog.cpp" << std::endl;
	this->fs << "\t../visualHFSM/popups/renametransitiondialog.cpp" << std::endl;
	this->fs << ")" << std::endl;
	this->fs << std::endl;
	this->fs << "pkg_check_modules(GTKMM REQUIRED gtkmm-3.0)" << std::endl;
	this->fs << std::endl;
	this->fs << "SET( INTERFACES_CPP_DIR /usr/local/include )" << std::endl;
	this->fs << "SET( LIBS_DIR /usr/local/lib )" << std::endl;
	this->fs << std::endl;
	this->fs << "SET( CMAKE_CXX_FLAGS \"-pthread\" ) # Opciones para el compilador" << std::endl;
	this->fs << std::endl;
	this->fs << "SET(EXECUTABLE_OUTPUT_PATH ${CMAKE_CURRENT_SOURCE_DIR})" << std::endl;
	this->fs << std::endl;
	this->fs << "SET(goocanvasmm_INCLUDE_DIRS" << std::endl;
	this->fs << "\t/usr/include/goocanvasmm-2.0" << std::endl;
	this->fs << "\t/usr/lib/goocanvasmm-2.0/include" << std::endl;
	this->fs << "\t/usr/include/goocanvas-2.0" << std::endl;
	this->fs << ")" << std::endl;
	this->fs << std::endl;
	this->fs << "include_directories (" << std::endl;
	this->fs << "\t/usr/local/include/jderobot" << std::endl;
	this->fs << "\t${INTERFACES_CPP_DIR}" << std::endl;
	this->fs << "\t${LIBS_DIR}" << std::endl;
	this->fs << "\t${CMAKE_CURRENT_SOURCE_DIR}" << std::endl;
	this->fs << "\t${GTKMM_INCLUDE_DIRS}" << std::endl;
	this->fs << "\t${goocanvasmm_INCLUDE_DIRS}" << std::endl;
	this->fs << ")" << std::endl;
	this->fs << std::endl;
	this->fs << "link_directories(${GTKMM_LIBRARY_DIRS})" << std::endl;
	this->fs << std::endl;
	this->fs << "add_executable (automata ${SOURCE_FILES_AUTOMATA})" << std::endl;
	this->fs << std::endl;
	this->fs << "SET(goocanvasmm_LIBRARIES goocanvasmm-2.0 goocanvas-2.0)" << std::endl;
	this->fs << std::endl;
	this->fs << "TARGET_LINK_LIBRARIES ( automata " << std::endl;
	this->fs << "\t${GTKMM_LIBRARIES}" << std::endl;
	this->fs << "\t${goocanvasmm_LIBRARIES}" <<std::endl;
	this->fs << "\t${LIBS_DIR}/jderobot/libJderobotInterfaces.so" << std::endl;
	this->fs << "\t${LIBS_DIR}/jderobot/libjderobotutil.so" << std::endl;
	this->fs << "\tIce" << std::endl;
	this->fs << "\tIceUtil" << std::endl;
	this->fs << ")" << std::endl;
	
	this->fs.flush();
}

std::string Generate::getCppName () {
	size_t last_pos = this->path.find_last_of(std::string("/"));
	if (last_pos == std::string::npos)
        return NULL;

    return this->path.substr(last_pos + 1, std::string::npos);
}
