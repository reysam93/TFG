#include <Ice/Ice.h>
#include <IceUtil/IceUtil.h>
#include <jderobot/visualHFSM/automatagui.h>

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

typedef enum State_Sub_3 {
	wait1,
	wait1_ghost,
	wait2,
	wait2_ghost,
} State_Sub_3;

const char* Names_Sub_3[] = {
	"wait1",
	"wait1_ghost",
	"wait2",
	"wait2_ghost",
};

pthread_t thr_sub_1;
pthread_t thr_sub_2;
pthread_t thr_sub_3;
pthread_t thr_automatagui;

AutomataGui *automatagui;
bool displayGui = false;

bool run1 = true;
bool run2 = true;
bool run3 = true;

State_Sub_1 sub_1 = square;
State_Sub_2 sub_2 = go_up_ghost;
State_Sub_3 sub_3 = wait1_ghost;

jderobot::EncodersPrx Encodersprx;
jderobot::MotorsPrx Motorsprx;

void shutDown(){
	run1 = false;
	run2 = false;
	run3 = false;
	automatagui->close();
}







std::list<GuiSubautomata> createGuiSubAutomataList(){
	std::list<GuiSubautomata> guiSubautomataList;

	GuiSubautomata* guiSubautomata1 = new GuiSubautomata(1, 0);

	guiSubautomata1->newGuiNode(1, 2, 134, 346);
	guiSubautomata1->setIsInitialLastGuiNode(1);
	guiSubautomata1->setNameLastGuiNode("square");

	guiSubautomata1->newGuiNode(2, 3, 534, 349);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("wait");

	Point* origin11 = new Point(134, 346);
	Point* destiny11 = new Point(534, 349);
	Point* midPoint11 = new Point(337, 230);
	guiSubautomata1->newGuiTransition(*origin11, *destiny11, *midPoint11, 1, 1, 2);

	Point* origin14 = new Point(534, 349);
	Point* destiny14 = new Point(134, 346);
	Point* midPoint14 = new Point(335, 457);
	guiSubautomata1->newGuiTransition(*origin14, *destiny14, *midPoint14, 4, 2, 1);

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

	GuiSubautomata* guiSubautomata3 = new GuiSubautomata(3, 1);

	guiSubautomata3->newGuiNode(15, 0, 166, 223);
	guiSubautomata3->setIsInitialLastGuiNode(1);
	guiSubautomata3->setNameLastGuiNode("wait1");

	guiSubautomata3->newGuiNode(16, 0, 446, 237);
	guiSubautomata3->setIsInitialLastGuiNode(0);
	guiSubautomata3->setNameLastGuiNode("wait2");

	Point* origin31 = new Point(166, 223);
	Point* destiny31 = new Point(446, 237);
	Point* midPoint31 = new Point(291, 127);
	guiSubautomata3->newGuiTransition(*origin31, *destiny31, *midPoint31, 1, 15, 16);

	Point* origin33 = new Point(446, 237);
	Point* destiny33 = new Point(166, 223);
	Point* midPoint33 = new Point(291, 301);
	guiSubautomata3->newGuiTransition(*origin33, *destiny33, *midPoint33, 3, 16, 15);

	guiSubautomataList.push_back(*guiSubautomata3);

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


	while (run1) {
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
						if (displayGui){
							automatagui->notifySetNodeAsActive("wait");
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
					if (secs > (double) 5) {
						sub_1 = square;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("square");
						}
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_1) {
			case square: {
				break;
			}
			case wait: {
				
				
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

	while (run2) {
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
						if (displayGui){
							automatagui->notifySetNodeAsActive("turn_rigth");
						}
						t_go_up_max = 2;
					}
				}

				break;
			}
			case turn_rigth: {
				if (angle > 90) {
					sub_2 = go_rigth;
					if(displayGui){
						automatagui->notifySetNodeAsActive("go_rigth");
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
						if (displayGui){
							automatagui->notifySetNodeAsActive("turn_down");
						}
						t_go_rigth_max = 2;
					}
				}

				break;
			}
			case turn_down: {
				if (angle > 90) {
					sub_2 = go_down;
					if(displayGui){
						automatagui->notifySetNodeAsActive("go_down");
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
						if (displayGui){
							automatagui->notifySetNodeAsActive("turn_left");
						}
						t_go_down_max = 2;
					}
				}

				break;
			}
			case turn_left: {
				if (angle > 90) {
					sub_2 = go_left;
					if(displayGui){
						automatagui->notifySetNodeAsActive("go_left");
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
						if (displayGui){
							automatagui->notifySetNodeAsActive("turn_up");
						}
						t_go_left_max = 2;
					}
				}

				break;
			}
			case turn_up: {
				if (angle > 90) {
					sub_2 = go_up;
					if(displayGui){
						automatagui->notifySetNodeAsActive("go_up");
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_2) {
			case go_up: {
				
				
				Motorsprx->setV(100.0);
				Motorsprx->setW(0.0);
				
				encoders = Encodersprx->getEncodersData();
				thetapos = encoders->robottheta;
				break;
			}
			case turn_rigth: {
				
				
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
				
				
				Motorsprx->setV(100.0);
				Motorsprx->setW(0.0);
				
				encoders = Encodersprx->getEncodersData();
				thetapos = encoders->robottheta;
				break;
			}
			case turn_down: {
				
				
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
				
				
				Motorsprx->setV(100.0);
				Motorsprx->setW(0.0);
				
				encoders = Encodersprx->getEncodersData();
				thetapos = encoders->robottheta;
				break;
			}
			case turn_left: {
				
				
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
				
				
				Motorsprx->setV(100.0);
				Motorsprx->setW(0.0);
				
				encoders = Encodersprx->getEncodersData();
				thetapos = encoders->robottheta;
				break;
			}
			case turn_up: {
				
				
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
				case turn_rigth:
					sub_2 = (State_Sub_2)(sub_2 + 1);
					break;
				case go_rigth:
					t_go_rigth_max = 2 - difftime(t_fin, t_ini);
					sub_2 = (State_Sub_2)(sub_2 + 1);
					break;
				case turn_down:
					sub_2 = (State_Sub_2)(sub_2 + 1);
					break;
				case go_down:
					t_go_down_max = 2 - difftime(t_fin, t_ini);
					sub_2 = (State_Sub_2)(sub_2 + 1);
					break;
				case turn_left:
					sub_2 = (State_Sub_2)(sub_2 + 1);
					break;
				case go_left:
					t_go_left_max = 2 - difftime(t_fin, t_ini);
					sub_2 = (State_Sub_2)(sub_2 + 1);
					break;
				case turn_up:
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

void* subautomata_3 ( void* ) {
	struct timeval a, b;
	int cycle = 100;
	long totala, totalb;
	long diff;
	time_t t_ini;
	time_t t_fin;
	double secs;
	bool t_activated;

	float t_wait1_max = 2;
	float t_wait2_max = 2.1;

	while (run3) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		if (sub_1 == wait) {
			if ( sub_3 == wait1_ghost || sub_3 == wait2_ghost) {
				sub_3 = (State_Sub_3)(sub_3 - 1);
				t_ini = time(NULL);
			}
		// Evaluation switch
		switch (sub_3) {
			case wait1: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_wait1_max) {
						sub_3 = wait2;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("wait2");
						}
						t_wait1_max = 2;
					}
				}

				break;
			}
			case wait2: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_wait2_max) {
						sub_3 = wait1;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("wait1");
						}
						t_wait2_max = 2.1;
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_3) {
			case wait1: {
				break;
			}
			case wait2: {
				break;
			}
		}
		} else {
			switch (sub_3) {
				case wait1:
					t_wait1_max = 2 - difftime(t_fin, t_ini);
					sub_3 = (State_Sub_3)(sub_3 + 1);
					break;
				case wait2:
					t_wait2_max = 2.1 - difftime(t_fin, t_ini);
					sub_3 = (State_Sub_3)(sub_3 + 1);
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

void readArgs(int *argc, char* argv[]){
	int i;
	std::string splitedArg;

	for(i = 0; i < *argc; i++){
		splitedArg = strtok(argv[i], "=");
		if (splitedArg.compare("--displaygui") == 0){
			splitedArg = strtok(NULL, "=");
			if (splitedArg.compare("true") == 0 || splitedArg.compare("True") == 0){
				displayGui = true;
				std::cout << "displayGui ENABLED" << std::endl;
			}else{
				displayGui = false;
				std::cout << "displayGui DISABLED" << std::endl;
			}
		}
		if(i == *argc -1){
			(*argc)--;
		}
	}
}

int main (int argc, char* argv[]) {
	int status;
	Ice::CommunicatorPtr ic;

	try {
		ic = Ice::initialize(argc, argv);
		readArgs(&argc, argv);


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

		if (displayGui){
			automatagui = new AutomataGui(argc, argv);
			displayGui = showAutomataGui();
		}

		pthread_create(&thr_sub_1, NULL, &subautomata_1, NULL);
		pthread_create(&thr_sub_2, NULL, &subautomata_2, NULL);
		pthread_create(&thr_sub_3, NULL, &subautomata_3, NULL);

		pthread_join(thr_sub_1, NULL);
		pthread_join(thr_sub_2, NULL);
		pthread_join(thr_sub_3, NULL);
		if (displayGui)
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
