#include <Ice/Ice.h>
#include <IceUtil/IceUtil.h>
#include "../visualHFSM/automatagui.h"

#include <iostream>

#include <jderobot/motors.h>

typedef enum State_Sub_1 {
	GO,
	wait,
} State_Sub_1;

const char* Names_Sub_1[] = {
	"GO",
	"wait",
};

pthread_t thr_sub_1;
pthread_t thr_automatagui;

AutomataGui *automatagui;
bool displayAutomataGui;

State_Sub_1 sub_1 = GO;

jderobot::MotorsPrx Motorsprx;



std::list<GuiSubautomata> createGuiSubAutomataList(){
	std::list<GuiSubautomata> guiSubautomataList;

	GuiSubautomata* guiSubautomata1 = new GuiSubautomata(1, 0);

	guiSubautomata1->newGuiNode(1, 0, 163, 201);
	guiSubautomata1->setIsInitialLastGuiNode(1);
	guiSubautomata1->setNameLastGuiNode("GO");

	guiSubautomata1->newGuiNode(2, 0, 539, 238);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("wait");

	Point* origin11 = new Point(163, 201);
	Point* destiny11 = new Point(539, 238);
	Point* midPoint11 = new Point(357, 116);
	guiSubautomata1->newGuiTransition(*origin11, *destiny11, *midPoint11, 1, 1, 2);

	Point* origin12 = new Point(539, 238);
	Point* destiny12 = new Point(163, 201);
	Point* midPoint12 = new Point(342, 308);
	guiSubautomata1->newGuiTransition(*origin12, *destiny12, *midPoint12, 2, 2, 1);

	guiSubautomataList.push_back(*guiSubautomata1);

	return guiSubautomataList;
}

void* subautomata_1 ( void* ) {
	struct timeval a, b;
	int cycle = 100;
	long totala, totalb;
	long diff;
	time_t t_ini;
	time_t t_fin;
	double secs;
	bool t_activated;


	while (true) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		// Evaluation switch
		switch (sub_1) {
			case GO: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) 3) {
						sub_1 = wait;
						t_activated = false;
						if (displayAutomataGui){
							automatagui->setNodeAsActive("wait", true);
							automatagui->setNodeAsActive("GO", false);
						}
					}
				}

				break;
			}
			case wait: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) 2) {
						sub_1 = GO;
						t_activated = false;
						if (displayAutomataGui){
							automatagui->setNodeAsActive("GO", true);
							automatagui->setNodeAsActive("wait", false);
						}
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_1) {
			case GO: {
				std::cout << "going up" << std::endl;
				
				Motorsprx->setV(100.0);
				Motorsprx->setW(0.0);
				break;
			}
			case wait: {
				std::cout << "waiting" << std::endl;
				
				Motorsprx->setV(0.0);
				Motorsprx->setW(0.0);
				break;
			}
		}

		gettimeofday(&b, NULL);
		totalb = b.tv_sec * 1000000 + b.tv_usec;
		diff = (totalb - totala) / 1000;
		if (diff < 0 || diff > cycle)
			diff = cycle;
		else
			diff = cycle - diff;

		usleep(diff * 1000);
		if (diff < 33 )
			usleep (33 * 1000);
	}
}

void* runAutomatagui (void*) {
	automatagui->run();
}

bool showAutomataGui () {
	if (automatagui->init() < 0){
		std::cerr << "warning: could not show automatagui" << std::endl;
		return false;
	}
	automatagui->setGuiSubautomataList(createGuiSubAutomataList());
	pthread_create(&thr_automatagui, NULL, &runAutomatagui, NULL);
	automatagui->loadGuiSubautomata();
	return true;
}

int main (int argc, char* argv[]) {
	int status;
	Ice::CommunicatorPtr ic;

	try {
		ic = Ice::initialize(argc, argv);

		// Contact to Motors
		Ice::ObjectPrx Motors = ic->propertyToProxy("automata.Motors.Proxy");
		if (Motors == 0)
			throw "Could not create proxy with Motors";
		Motorsprx = jderobot::MotorsPrx::checkedCast(Motors);
		if (Motorsprx == 0)
			throw "Invalid proxy automata.Motors.Proxy";
		std::cout << "Motors connected" << std::endl;

		automatagui = new AutomataGui(argc, argv);
		displayAutomataGui = showAutomataGui();
		pthread_create(&thr_sub_1, NULL, &subautomata_1, NULL);

		pthread_join(thr_sub_1, NULL);
		if (displayAutomataGui)
			pthread_join(thr_automatagui, NULL);

	} catch ( const Ice::Exception& ex ) {
		std::cerr << ex << std::endl;
		status = 1;
	} catch ( const char* msg ) {
		std::cerr << msg << std::endl;
		status = 1;
	}

	if (ic)
		ic->destroy();

	return status;
}
