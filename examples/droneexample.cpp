#include <Ice/Ice.h>
#include <IceUtil/IceUtil.h>
#include "../visualHFSM/automatagui.h"

#include <iostream>

#include <jderobot/camera.h>
#include <jderobot/cmdvel.h>

typedef enum State_Sub_1 {
	DoNothing,
} State_Sub_1;

const char* Names_Sub_1[] = {
	"DoNothing",
};

pthread_t thr_sub_1;
pthread_t thr_automatagui;

AutomataGui *automatagui;
bool displayAutomataGui;

State_Sub_1 sub_1 = DoNothing;

jderobot::CameraPrx Cameraprx;
jderobot::CMDVelPrx CMDVelprx;



std::list<GuiSubautomata> createGuiSubAutomataList(){
	std::list<GuiSubautomata> guiSubautomataList;

	GuiSubautomata* guiSubautomata1 = new GuiSubautomata(1, 0);

	guiSubautomata1->newGuiNode(1, 0, 324, 277);
	guiSubautomata1->setIsInitialLastGuiNode(1);
	guiSubautomata1->setNameLastGuiNode("DoNothing");

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
			case DoNothing: {
				break;
			}
		}

		// Actuation switch
		switch (sub_1) {
			case DoNothing: {
				std::cout << "DOING NOTHING" << std::endl;
				
				CMDVelprx->setCMDVelData((1,0,0,0,0,0));
				
				
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

		// Contact to Camera
		Ice::ObjectPrx Camera = ic->propertyToProxy("automata.Camera.Proxy");
		if (Camera == 0)
			throw "Could not create proxy with Camera";
		Cameraprx = jderobot::CameraPrx::checkedCast(Camera);
		if (Cameraprx == 0)
			throw "Invalid proxy automata.Camera.Proxy";
		std::cout << "Camera connected" << std::endl;

		// Contact to CMDVel
		Ice::ObjectPrx CMDVel = ic->propertyToProxy("automata.CMDVel.Proxy");
		if (CMDVel == 0)
			throw "Could not create proxy with CMDVel";
		CMDVelprx = jderobot::CMDVelPrx::checkedCast(CMDVel);
		if (CMDVelprx == 0)
			throw "Invalid proxy automata.CMDVel.Proxy";
		std::cout << "CMDVel connected" << std::endl;

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
