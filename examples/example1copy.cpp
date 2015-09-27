#include <Ice/Ice.h>
#include <IceUtil/IceUtil.h>
#include "../visualHFSM/automatagui.h"

#include <iostream>

#include <jderobot/encoders.h>
#include <jderobot/motors.h>

typedef enum State_Sub_1 {
	square,
	wait,
} State_Sub_1;

const char* Names_Sub_1[] = {
	"square",
	"wait",
};

typedef enum State_Sub_2 {
	go_up,
	go_up_ghost,
	turn_rigth,
	turn_rigth_ghost,
	go_rigth,
	go_rigth_ghost,
	turn_down,
	turn_down_ghost,
	go_down,
	go_down_ghost,
	turn_left,
	turn_left_ghost,
	go_left,
	go_left_ghost,
	turn_up,
	turn_up_ghost,
} State_Sub_2;

const char* Names_Sub_2[] = {
	"go_up",
	"go_up_ghost",
	"turn_rigth",
	"turn_rigth_ghost",
	"go_rigth",
	"go_rigth_ghost",
	"turn_down",
	"turn_down_ghost",
	"go_down",
	"go_down_ghost",
	"turn_left",
	"turn_left_ghost",
	"go_left",
	"go_left_ghost",
	"turn_up",
	"turn_up_ghost",
};

pthread_t thr_sub_1;
pthread_t thr_sub_2;
pthread_t thr_automatagui;

AutomataGui *automatagui;
bool displayAutomataGui;

State_Sub_1 sub_1 = square;
State_Sub_2 sub_2 = go_up_ghost;

jderobot::EncodersPrx Encodersprx;
jderobot::MotorsPrx Motorsprx;





std::list<GuiSubautomata> createGuiSubAutomataList(){
	std::list<GuiSubautomata> guiSubautomataList;

	GuiSubautomata* guiSubautomata1 = new GuiSubautomata(1, 0);

	guiSubautomata1->newGuiNode(1, 2, 134, 347);
	guiSubautomata1->setIsInitialLastGuiNode(1);
	guiSubautomata1->setNameLastGuiNode("square");

	guiSubautomata1->newGuiNode(2, 0, 534, 349);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("wait");

	Point* origin11 = new Point(134, 347);
	Point* destiny11 = new Point(534, 349);
	Point* midPoint11 = new Point(337, 230);
	guiSubautomata1->newGuiTransition(*origin11, *destiny11, *midPoint11, 1, 1, 2);

	guiSubautomataList.push_back(*guiSubautomata1);

	GuiSubautomata* guiSubautomata2 = new GuiSubautomata(2, 1);

	guiSubautomata2->newGuiNode(5, 0, 168, 559);
	guiSubautomata2->setIsInitialLastGuiNode(1);
	guiSubautomata2->setNameLastGuiNode("go_up");

	guiSubautomata2->newGuiNode(8, 0, 69, 396);
	guiSubautomata2->setIsInitialLastGuiNode(0);
	guiSubautomata2->setNameLastGuiNode("turn_rigth");

	guiSubautomata2->newGuiNode(9, 0, 185, 270);
	guiSubautomata2->setIsInitialLastGuiNode(0);
	guiSubautomata2->setNameLastGuiNode("go_rigth");

	guiSubautomata2->newGuiNode(10, 0, 343, 192);
	guiSubautomata2->setIsInitialLastGuiNode(0);
	guiSubautomata2->setNameLastGuiNode("turn_down");

	guiSubautomata2->newGuiNode(11, 0, 486, 283);
	guiSubautomata2->setIsInitialLastGuiNode(0);
	guiSubautomata2->setNameLastGuiNode("go_down");

	guiSubautomata2->newGuiNode(12, 0, 555, 426);
	guiSubautomata2->setIsInitialLastGuiNode(0);
	guiSubautomata2->setNameLastGuiNode("turn_left");

	guiSubautomata2->newGuiNode(13, 0, 505, 583);
	guiSubautomata2->setIsInitialLastGuiNode(0);
	guiSubautomata2->setNameLastGuiNode("go_left");

	guiSubautomata2->newGuiNode(14, 0, 354, 650);
	guiSubautomata2->setIsInitialLastGuiNode(0);
	guiSubautomata2->setNameLastGuiNode("turn_up");

	Point* origin210 = new Point(168, 559);
	Point* destiny210 = new Point(69, 396);
	Point* midPoint210 = new Point(118, 477);
	guiSubautomata2->newGuiTransition(*origin210, *destiny210, *midPoint210, 10, 5, 8);

	Point* origin212 = new Point(69, 396);
	Point* destiny212 = new Point(185, 270);
	Point* midPoint212 = new Point(127, 333);
	guiSubautomata2->newGuiTransition(*origin212, *destiny212, *midPoint212, 12, 8, 9);

	Point* origin213 = new Point(185, 270);
	Point* destiny213 = new Point(343, 192);
	Point* midPoint213 = new Point(264, 231);
	guiSubautomata2->newGuiTransition(*origin213, *destiny213, *midPoint213, 13, 9, 10);

	Point* origin214 = new Point(343, 192);
	Point* destiny214 = new Point(486, 283);
	Point* midPoint214 = new Point(415, 237);
	guiSubautomata2->newGuiTransition(*origin214, *destiny214, *midPoint214, 14, 10, 11);

	Point* origin215 = new Point(486, 283);
	Point* destiny215 = new Point(555, 426);
	Point* midPoint215 = new Point(525, 348);
	guiSubautomata2->newGuiTransition(*origin215, *destiny215, *midPoint215, 15, 11, 12);

	Point* origin216 = new Point(555, 426);
	Point* destiny216 = new Point(505, 583);
	Point* midPoint216 = new Point(534, 498);
	guiSubautomata2->newGuiTransition(*origin216, *destiny216, *midPoint216, 16, 12, 13);

	Point* origin217 = new Point(505, 583);
	Point* destiny217 = new Point(354, 650);
	Point* midPoint217 = new Point(430, 616);
	guiSubautomata2->newGuiTransition(*origin217, *destiny217, *midPoint217, 17, 13, 14);

	Point* origin218 = new Point(354, 650);
	Point* destiny218 = new Point(168, 559);
	Point* midPoint218 = new Point(261, 604);
	guiSubautomata2->newGuiTransition(*origin218, *destiny218, *midPoint218, 18, 14, 5);

	guiSubautomataList.push_back(*guiSubautomata2);

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
			case square: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) 20) {
						sub_1 = wait;
						t_activated = false;
						if (displayAutomataGui){
							automatagui->setNodeAsActive("wait", true);
							automatagui->setNodeAsActive("square", false);
						}
					}
				}

				break;
			}
			case wait: {
				break;
			}
		}

		// Actuation switch
		switch (sub_1) {
			case square: {
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

void* subautomata_2 ( void* ) {
	struct timeval a, b;
	int cycle = 100;
	long totala, totalb;
	long diff;
	time_t t_ini;
	time_t t_fin;
	double secs;
	bool t_activated;

	float t_go_up_max = 2;
	float t_go_rigth_max = 2;
	float t_go_down_max = 2;
	float t_go_left_max = 2;
	jderobot::EncodersDataPtr encoders = Encodersprx->getEncodersData();
	float thetapos = 0;
	float angle = 0;

	while (true) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		if (sub_1 == square) {
			if ( sub_2 == go_up_ghost || sub_2 == turn_rigth_ghost || sub_2 == go_rigth_ghost || sub_2 == turn_down_ghost || sub_2 == go_down_ghost || sub_2 == turn_left_ghost || sub_2 == go_left_ghost || sub_2 == turn_up_ghost) {
				sub_2 = (State_Sub_2)(sub_2 - 1);
				t_ini = time(NULL);
			}
		// Evaluation switch
		switch (sub_2) {
			case go_up: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_go_up_max) {
						sub_2 = turn_rigth;
						t_activated = false;
						if (displayAutomataGui){
							automatagui->setNodeAsActive("turn_rigth", true);
							automatagui->setNodeAsActive("go_up", false);
						}
						t_go_up_max = 2;
					}
				}

				break;
			}
			case turn_rigth: {
				if (angle > 90) {
					sub_2 = go_rigth;
						if (displayAutomataGui){
							automatagui->setNodeAsActive("go_rigth", true);
							automatagui->setNodeAsActive("turn_rigth", false);
						}
				}

				break;
			}
			case go_rigth: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_go_rigth_max) {
						sub_2 = turn_down;
						t_activated = false;
						if (displayAutomataGui){
							automatagui->setNodeAsActive("turn_down", true);
							automatagui->setNodeAsActive("go_rigth", false);
						}
						t_go_rigth_max = 2;
					}
				}

				break;
			}
			case turn_down: {
				if (angle > 90) {
					sub_2 = go_down;
						if (displayAutomataGui){
							automatagui->setNodeAsActive("go_down", true);
							automatagui->setNodeAsActive("turn_down", false);
						}
				}

				break;
			}
			case go_down: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_go_down_max) {
						sub_2 = turn_left;
						t_activated = false;
						if (displayAutomataGui){
							automatagui->setNodeAsActive("turn_left", true);
							automatagui->setNodeAsActive("go_down", false);
						}
						t_go_down_max = 2;
					}
				}

				break;
			}
			case turn_left: {
				if (angle > 90) {
					sub_2 = go_left;
						if (displayAutomataGui){
							automatagui->setNodeAsActive("go_left", true);
							automatagui->setNodeAsActive("turn_left", false);
						}
				}

				break;
			}
			case go_left: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_go_left_max) {
						sub_2 = turn_up;
						t_activated = false;
						if (displayAutomataGui){
							automatagui->setNodeAsActive("turn_up", true);
							automatagui->setNodeAsActive("go_left", false);
						}
						t_go_left_max = 2;
					}
				}

				break;
			}
			case turn_up: {
				if (angle > 90) {
					sub_2 = go_up;
						if (displayAutomataGui){
							automatagui->setNodeAsActive("go_up", true);
							automatagui->setNodeAsActive("turn_up", false);
						}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_2) {
			case go_up: {
				std::cout << "going up" << std::endl;
				
				Motorsprx->setV(100.0);
				Motorsprx->setW(0.0);
				
				encoders = Encodersprx->getEncodersData();
				thetapos = encoders->robottheta;
				break;
			}
			case turn_rigth: {
				std::cout << "turning right" << std::endl;
				
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
			case go_rigth: {
				std::cout << "going rigth" << std::endl;
				
				Motorsprx->setV(100.0);
				Motorsprx->setW(0.0);
				
				encoders = Encodersprx->getEncodersData();
				thetapos = encoders->robottheta;
				break;
			}
			case turn_down: {
				std::cout << "turning down" << std::endl;
				
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
			case go_down: {
				std::cout << "going down" << std::endl;
				
				Motorsprx->setV(100.0);
				Motorsprx->setW(0.0);
				
				encoders = Encodersprx->getEncodersData();
				thetapos = encoders->robottheta;
				break;
			}
			case turn_left: {
				std::cout << "turning left" << std::endl;
				
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
			case go_left: {
				std::cout << "going left" << std::endl;
				
				Motorsprx->setV(100.0);
				Motorsprx->setW(0.0);
				
				encoders = Encodersprx->getEncodersData();
				thetapos = encoders->robottheta;
				break;
			}
			case turn_up: {
				std::cout << "turning up" << std::endl;
				
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
		}
		} else {
			switch (sub_2) {
				case go_up:
					t_go_up_max = 2 - difftime(t_fin, t_ini);
					sub_2 = (State_Sub_2)(sub_2 + 1);
					break;
				case go_rigth:
					t_go_rigth_max = 2 - difftime(t_fin, t_ini);
					sub_2 = (State_Sub_2)(sub_2 + 1);
					break;
				case go_down:
					t_go_down_max = 2 - difftime(t_fin, t_ini);
					sub_2 = (State_Sub_2)(sub_2 + 1);
					break;
				case go_left:
					t_go_left_max = 2 - difftime(t_fin, t_ini);
					sub_2 = (State_Sub_2)(sub_2 + 1);
					break;
				default:
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
		pthread_create(&thr_sub_2, NULL, &subautomata_2, NULL);

		pthread_join(thr_sub_1, NULL);
		pthread_join(thr_sub_2, NULL);
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
