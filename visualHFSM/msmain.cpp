// automatagui main
// g++ -Wall -g -c automatagui.cpp `pkg-config gtkmm-3.0 --cflags --libs`
// g++ -Wall -g -c xmlparser.cpp
// g++ -Wall -g -c msmain.cpp `pkg-config gtkmm-3.0 --cflags --libs`
// g++ -g automatagui.o xmlparser.o msmain.o -o msmain `pkg-config gtkmm-3.0 --cflags --libs`

//#include <gtkmm.h>

#include <iostream>
#include <pthread.h>

#include "automatagui.h"


pthread_t thr_automatagui;
AutomataGui *automatagui;


std::list<SubAutomata> createSubAutomataList(){
	std::list<SubAutomata> subautomatalist;
	
	SubAutomata subautomata1(1, 0);

	Node node11(1, true);
	node11.setIdAutomataSon(0);
	node11.setName("GO");
	Point* point11 = new Point(163, 201);
	subautomata1->addNode(node11->copy(), point11->copyAsPointer());

	Node node12(2, false);
	node12.setIdAutomataSon(0);
	node12.setName("wait");
	Point* point12 = new Point(539, 238);
	subautomata1->addNode(node12->copy(), point12->copyAsPointer());

	Transition trans11(1, 1, 2);
	Point* transpoint11 = new Point(342, 308);
	subautomata1->addTransition(trans11->copy(), transpoint11->copyAsPointer());

	subautomatalist.push_back(subautomata1);

	return subautomatalist;
}

void* initautomatagui (void*) {
	if (automatagui->init() < 0)
		std::cout << "Could not show automatagui" << std::endl;
}

void showAutomataGui (){
	automatagui->setSubAutomataList (createSubAutomataList());
	pthread_create(&thr_automatagui, NULL, &initautomatagui, NULL);
}

int
main(int argc, char **argv)
{
	automatagui = new AutomataGui(argc, argv);
	showAutomataGui();
	pthread_join(thr_automatagui, NULL);
	
  	return 0;
}
