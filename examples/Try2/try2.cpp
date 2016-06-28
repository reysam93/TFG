#include <Ice/Ice.h>
#include <IceUtil/IceUtil.h>
#include <jderobot/visualHFSM/automatagui.h>

typedef enum State_Sub_1 {
	PingPong,
	Numbers,
} State_Sub_1;

const char* Names_Sub_1[] = {
	"PingPong",
	"Numbers",
};

typedef enum State_Sub_3 {
	Ping,
	Ping_ghost,
	Pong,
	Pong_ghost,
} State_Sub_3;

const char* Names_Sub_3[] = {
	"Ping",
	"Ping_ghost",
	"Pong",
	"Pong_ghost",
};

typedef enum State_Sub_4 {
	1,
	1_ghost,
	2,
	2_ghost,
	3,
	3_ghost,
} State_Sub_4;

const char* Names_Sub_4[] = {
	"1",
	"1_ghost",
	"2",
	"2_ghost",
	"3",
	"3_ghost",
};

typedef enum State_Sub_5 {
	wait1,
	wait1_ghost,
	wait2,
	wait2_ghost,
} State_Sub_5;

const char* Names_Sub_5[] = {
	"wait1",
	"wait1_ghost",
	"wait2",
	"wait2_ghost",
};

pthread_t thr_sub_1;
pthread_t thr_sub_3;
pthread_t thr_sub_4;
pthread_t thr_sub_5;
pthread_t thr_automatagui;

AutomataGui *automatagui;
bool displayGui = false;

bool run1 = true;
bool run3 = true;
bool run4 = true;
bool run5 = true;

State_Sub_1 sub_1 = PingPong;
State_Sub_3 sub_3 = Ping_ghost;
State_Sub_4 sub_4 = 1_ghost;
State_Sub_5 sub_5 = wait1_ghost;


void shutDown(){
	run1 = false;
	run3 = false;
	run4 = false;
	run5 = false;
	automatagui->close();
}









std::list<GuiSubautomata> createGuiSubAutomataList(){
	std::list<GuiSubautomata> guiSubautomataList;

	GuiSubautomata* guiSubautomata1 = new GuiSubautomata(1, 0);

	guiSubautomata1->newGuiNode(1, 3, 113, 192);
	guiSubautomata1->setIsInitialLastGuiNode(1);
	guiSubautomata1->setNameLastGuiNode("PingPong");

	guiSubautomata1->newGuiNode(2, 4, 512, 223);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("Numbers");

	Point* origin11 = new Point(512, 223);
	Point* destiny11 = new Point(113, 192);
	Point* midPoint11 = new Point(302, 378);
	guiSubautomata1->newGuiTransition(*origin11, *destiny11, *midPoint11, 1, 2, 1);

	Point* origin12 = new Point(113, 192);
	Point* destiny12 = new Point(512, 223);
	Point* midPoint12 = new Point(322, 127);
	guiSubautomata1->newGuiTransition(*origin12, *destiny12, *midPoint12, 2, 1, 2);

	guiSubautomataList.push_back(*guiSubautomata1);

	GuiSubautomata* guiSubautomata3 = new GuiSubautomata(3, 1);

	guiSubautomata3->newGuiNode(4, 0, 65, 154);
	guiSubautomata3->setIsInitialLastGuiNode(1);
	guiSubautomata3->setNameLastGuiNode("Ping");

	guiSubautomata3->newGuiNode(5, 5, 313, 162);
	guiSubautomata3->setIsInitialLastGuiNode(0);
	guiSubautomata3->setNameLastGuiNode("Pong");

	Point* origin33 = new Point(65, 154);
	Point* destiny33 = new Point(313, 162);
	Point* midPoint33 = new Point(192, 74);
	guiSubautomata3->newGuiTransition(*origin33, *destiny33, *midPoint33, 3, 4, 5);

	Point* origin34 = new Point(313, 162);
	Point* destiny34 = new Point(65, 154);
	Point* midPoint34 = new Point(187, 212);
	guiSubautomata3->newGuiTransition(*origin34, *destiny34, *midPoint34, 4, 5, 4);

	guiSubautomataList.push_back(*guiSubautomata3);

	GuiSubautomata* guiSubautomata4 = new GuiSubautomata(4, 1);

	guiSubautomata4->newGuiNode(6, 0, 161, 158);
	guiSubautomata4->setIsInitialLastGuiNode(1);
	guiSubautomata4->setNameLastGuiNode("1");

	guiSubautomata4->newGuiNode(7, 0, 493, 246);
	guiSubautomata4->setIsInitialLastGuiNode(0);
	guiSubautomata4->setNameLastGuiNode("2");

	guiSubautomata4->newGuiNode(8, 0, 207, 358);
	guiSubautomata4->setIsInitialLastGuiNode(0);
	guiSubautomata4->setNameLastGuiNode("3");

	Point* origin45 = new Point(161, 158);
	Point* destiny45 = new Point(493, 246);
	Point* midPoint45 = new Point(327, 202);
	guiSubautomata4->newGuiTransition(*origin45, *destiny45, *midPoint45, 5, 6, 7);

	Point* origin46 = new Point(493, 246);
	Point* destiny46 = new Point(207, 358);
	Point* midPoint46 = new Point(350, 302);
	guiSubautomata4->newGuiTransition(*origin46, *destiny46, *midPoint46, 6, 7, 8);

	Point* origin47 = new Point(207, 358);
	Point* destiny47 = new Point(161, 158);
	Point* midPoint47 = new Point(184, 258);
	guiSubautomata4->newGuiTransition(*origin47, *destiny47, *midPoint47, 7, 8, 6);

	guiSubautomataList.push_back(*guiSubautomata4);

	GuiSubautomata* guiSubautomata5 = new GuiSubautomata(5, 3);

	guiSubautomata5->newGuiNode(8, 0, 121, 121);
	guiSubautomata5->setIsInitialLastGuiNode(1);
	guiSubautomata5->setNameLastGuiNode("wait1");

	guiSubautomata5->newGuiNode(9, 0, 259, 225);
	guiSubautomata5->setIsInitialLastGuiNode(0);
	guiSubautomata5->setNameLastGuiNode("wait2");

	Point* origin51 = new Point(121, 121);
	Point* destiny51 = new Point(259, 225);
	Point* midPoint51 = new Point(281, 112);
	guiSubautomata5->newGuiTransition(*origin51, *destiny51, *midPoint51, 1, 8, 9);

	Point* origin52 = new Point(259, 225);
	Point* destiny52 = new Point(121, 121);
	Point* midPoint52 = new Point(130, 203);
	guiSubautomata5->newGuiTransition(*origin52, *destiny52, *midPoint52, 2, 9, 8);

	guiSubautomataList.push_back(*guiSubautomata5);

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

	self.numbersFinished = False

	while (run1) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		// Evaluation switch
		switch (sub_1) {
			case PingPong: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) 3.5) {
						sub_1 = Numbers;
						t_activated = false;
						automatagui->notifySetNodeAsActive("Numbers");
					}
				}

				break;
			}
			case Numbers: {
				if (self.numbersFinished) {
					sub_1 = PingPong;
						self.numbersFinished = False
					automatagui->notifySetNodeAsActive("PingPong");
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_1) {
			case PingPong: {
				print "PingPong"
				time.sleep(4)
				break;
			}
			case Numbers: {
				print "Numbers"
				time.sleep(5)
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

	self.ping = False
	self.ping = False

	while (run3) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		if (sub_1 == PingPong) {
			if ( sub_3 == Ping_ghost || sub_3 == Pong_ghost) {
				sub_3 = (State_Sub_3)(sub_3 - 1);
				t_ini = time(NULL);
			}
		// Evaluation switch
		switch (sub_3) {
			case Ping: {
				if (self.ping) {
					sub_3 = Pong;
						self.ping = False
					automatagui->notifySetNodeAsActive("Pong");
				}

				break;
			}
			case Pong: {
				if (self.pong) {
					sub_3 = Ping;
						self.pong = False
					automatagui->notifySetNodeAsActive("Ping");
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_3) {
			case Ping: {
				print "    PING"
				time.sleep(0.5)
				self.ping= True
				break;
			}
			case Pong: {
				print "            PONG"
				time.sleep(0.5)
				self.pong = True
				break;
			}
		}
		} else {
			switch (sub_3) {
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

void* subautomata_4 ( void* ) {
	struct timeval a, b;
	int cycle = 100;
	long totala, totalb;
	long diff;
	time_t t_ini;
	time_t t_fin;
	double secs;
	bool t_activated;

	float t_1_max = 0.001;
	float t_2_max = 0.001;
	float t_3_max = 0.001;

	while (run4) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		if (sub_1 == Numbers) {
			if ( sub_4 == 1_ghost || sub_4 == 2_ghost || sub_4 == 3_ghost) {
				sub_4 = (State_Sub_4)(sub_4 - 1);
				t_ini = time(NULL);
			}
		// Evaluation switch
		switch (sub_4) {
			case 1: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_1_max) {
						sub_4 = 2;
						t_activated = false;
						automatagui->notifySetNodeAsActive("2");
						t_1_max = 0.001;
					}
				}

				break;
			}
			case 2: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_2_max) {
						sub_4 = 3;
						t_activated = false;
						automatagui->notifySetNodeAsActive("3");
						t_2_max = 0.001;
					}
				}

				break;
			}
			case 3: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_3_max) {
						sub_4 = 1;
						t_activated = false;
						self.numbersFinished= True
						automatagui->notifySetNodeAsActive("1");
						t_3_max = 0.001;
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_4) {
			case 1: {
				print "    1"
				time.sleep(1)
				break;
			}
			case 2: {
				print "        2"
				time.sleep(1)
				break;
			}
			case 3: {
				print "            3"
				time.sleep(1)
				break;
			}
		}
		} else {
			switch (sub_4) {
				case 1:
					t_1_max = 0.001 - difftime(t_fin, t_ini);
					sub_4 = (State_Sub_4)(sub_4 + 1);
					break;
				case 2:
					t_2_max = 0.001 - difftime(t_fin, t_ini);
					sub_4 = (State_Sub_4)(sub_4 + 1);
					break;
				case 3:
					t_3_max = 0.001 - difftime(t_fin, t_ini);
					sub_4 = (State_Sub_4)(sub_4 + 1);
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

void* subautomata_5 ( void* ) {
	struct timeval a, b;
	int cycle = 100;
	long totala, totalb;
	long diff;
	time_t t_ini;
	time_t t_fin;
	double secs;
	bool t_activated;

	float t_wait1_max = 1;
	float t_wait2_max = 1;

	while (run5) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		if (sub_3 == Pong) {
			if ( sub_5 == wait1_ghost || sub_5 == wait2_ghost) {
				sub_5 = (State_Sub_5)(sub_5 - 1);
				t_ini = time(NULL);
			}
		// Evaluation switch
		switch (sub_5) {
			case wait1: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_wait1_max) {
						sub_5 = wait2;
						t_activated = false;
						automatagui->notifySetNodeAsActive("wait2");
						t_wait1_max = 1;
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
						sub_5 = wait1;
						t_activated = false;
						automatagui->notifySetNodeAsActive("wait1");
						t_wait2_max = 1;
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_5) {
			case wait1: {
				print
				break;
			}
			case wait2: {
				print ""
				break;
			}
		}
		} else {
			switch (sub_5) {
				case wait1:
					t_wait1_max = 1 - difftime(t_fin, t_ini);
					sub_5 = (State_Sub_5)(sub_5 + 1);
					break;
				case wait2:
					t_wait2_max = 1 - difftime(t_fin, t_ini);
					sub_5 = (State_Sub_5)(sub_5 + 1);
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

	void readArgs(int argc, char* argv){
		int i;
		char* splitedArg;

		for(i = 0; i < argc; i++)
			splitedArg = strtok(argv[i], "=");
			if (splitedArg.compare("--displaygui" == 0)){
				splitedArg = strtok(NULL, "=");
				if (splitedArg.compare("true") == 0 || splitedArg.compare("True") == 0){
					displayGui = true;
					std::cout << "displayGui ENABLED" << std::endl;
				}else{\n\
					displayGui = false
					std::cout << "displayGui DISABLED" << std::endl;
				}
			}
		}



int main (int argc, char* argv[]) {
	int status;
	Ice::CommunicatorPtr ic;

	try {
		ic = Ice::initialize(argc, argv);
		readArgs(argc, argv);
		if(){
			automatagui = new AutomataGui(argc, argv);
			displayAutomataGui = showAutomataGui();
		}
		
		pthread_create(&thr_sub_1, NULL, &subautomata_1, NULL);
		pthread_create(&thr_sub_3, NULL, &subautomata_3, NULL);
		pthread_create(&thr_sub_4, NULL, &subautomata_4, NULL);
		pthread_create(&thr_sub_5, NULL, &subautomata_5, NULL);

		pthread_join(thr_sub_1, NULL);
		pthread_join(thr_sub_3, NULL);
		pthread_join(thr_sub_4, NULL);
		pthread_join(thr_sub_5, NULL);
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
