#include <Ice/Ice.h>
#include <IceUtil/IceUtil.h>
#include <jderobot/visualHFSM/automatagui.h>

#include <iostream>

#include <jderobot/encoders.h>
#include <jderobot/motors.h>

typedef enum State_Sub_1 {
	GoFront,
	GoBack,
	Turn,
	Wait,
} State_Sub_1;

const char* Names_Sub_1[] = {
	"GoFront",
	"GoBack",
	"Turn",
	"Wait",
};

pthread_t thr_sub_1;
pthread_t thr_automatagui;

AutomataGui *automatagui;
bool displayAutomataGui;

bool run1 = true;

State_Sub_1 sub_1 = GoFront;

jderobot::EncodersPrx Encodersprx;
jderobot::MotorsPrx Motorsprx;

void shutDown(){
	run1 = false;
	automatagui->close();
}



std::list<GuiSubautomata> createGuiSubAutomataList(){
	std::list<GuiSubautomata> guiSubautomataList;

	GuiSubautomata* guiSubautomata1 = new GuiSubautomata(1, 0);

	guiSubautomata1->newGuiNode(1, 0, 60, 124);
	guiSubautomata1->setIsInitialLastGuiNode(1);
	guiSubautomata1->setNameLastGuiNode("GoFront");

	guiSubautomata1->newGuiNode(2, 0, 387, 123);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("GoBack");

	guiSubautomata1->newGuiNode(3, 0, 415, 398);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("Turn");

	guiSubautomata1->newGuiNode(4, 0, 89, 389);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("Wait");

	Point* origin11 = new Point(60, 124);
	Point* destiny11 = new Point(387, 123);
	Point* midPoint11 = new Point(224, 123);
	guiSubautomata1->newGuiTransition(*origin11, *destiny11, *midPoint11, 1, 1, 2);

	Point* origin12 = new Point(387, 123);
	Point* destiny12 = new Point(415, 398);
	Point* midPoint12 = new Point(555, 356);
	guiSubautomata1->newGuiTransition(*origin12, *destiny12, *midPoint12, 2, 2, 3);

	Point* origin13 = new Point(415, 398);
	Point* destiny13 = new Point(89, 389);
	Point* midPoint13 = new Point(252, 393);
	guiSubautomata1->newGuiTransition(*origin13, *destiny13, *midPoint13, 3, 3, 4);

	Point* origin14 = new Point(89, 389);
	Point* destiny14 = new Point(60, 124);
	Point* midPoint14 = new Point(133, 248);
	guiSubautomata1->newGuiTransition(*origin14, *destiny14, *midPoint14, 4, 4, 1);

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

	jderobot::EncodersDataPtr encoders = Encodersprx->getEncodersData();
	float thetapos = 0;
	float angle = 0;

	while (run1) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		// Evaluation switch
		switch (sub_1) {
			case GoFront: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) 2) {
						sub_1 = GoBack;
						t_activated = false;
						automatagui->notifySetNodeAsActive("GoBack");
					}
				}

				break;
			}
			case GoBack: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) 2) {
						sub_1 = Turn;
						t_activated = false;
						automatagui->notifySetNodeAsActive("Turn");
					}
				}

				break;
			}
			case Turn: {
				if (angle > 45) {
					sub_1 = Wait;
					automatagui->notifySetNodeAsActive("Wait");
				}

				break;
			}
			case Wait: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) 1) {
						sub_1 = GoFront;
						t_activated = false;
						automatagui->notifySetNodeAsActive("GoFront");
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_1) {
			case GoFront: {
				Motorsprx->setV(100.0);
				Motorsprx->setW(0.0);
				
				encoders = Encodersprx->getEncodersData();
				thetapos = encoders->robottheta;
				break;
			}
			case GoBack: {
				Motorsprx->setV(-100.0);
				Motorsprx->setW(0.0);
				
				encoders = Encodersprx->getEncodersData();
				thetapos = encoders->robottheta;
				break;
			}
			case Turn: {
				Motorsprx->setV(0.0);
				Motorsprx->setW(-3.0);
				
				encoders = Encodersprx->getEncodersData();
				if (encoders->robottheta > thetapos + 1)
					angle = thetapos - encoders->robottheta + 360;
				else
					angle = thetapos - encoders->robottheta;
				
				std::cout << "angle: " << angle << std::endl;
				break;
			}
			case Wait: {
				Motorsprx->setV(0.0);
				Motorsprx->setW(0.0);
				
				encoders = Encodersprx->getEncodersData();
				thetapos = encoders->robottheta;
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

		// Contact to Encoders
		Ice::ObjectPrx Encoders = ic->propertyToProxy("automata.Encoders.Proxy");
		if (Encoders == 0)
			throw "Could not create proxy with Encoders";
		Encodersprx = jderobot::EncodersPrx::checkedCast(Encoders);
		if (Encodersprx == 0)
			throw "Invalid proxy automata.Encoders.Proxy";
		std::cout << "Encoders connected" << std::endl;

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
