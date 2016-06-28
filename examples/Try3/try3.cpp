#include <Ice/Ice.h>
#include <IceUtil/IceUtil.h>
#include <jderobot/visualHFSM/automatagui.h>

#include <jderobot>

#include <jderobot/pose3d.h>
#include <jderobot/cmdvel.h>
#include <jderobot/ardroneextra.h>

typedef enum State_Sub_1 {
	TakeOff,
	GoFront,
	DoSquare,
	Landing,
	END,
} State_Sub_1;

const char* Names_Sub_1[] = {
	"TakeOff",
	"GoFront",
	"DoSquare",
	"Landing",
	"END",
};

typedef enum State_Sub_2 {
	TakingOff,
	TakingOff_ghost,
	Stabilizing1,
	Stabilizing1_ghost,
} State_Sub_2;

const char* Names_Sub_2[] = {
	"TakingOff",
	"TakingOff_ghost",
	"Stabilizing1",
	"Stabilizing1_ghost",
};

typedef enum State_Sub_3 {
	GoingFront,
	GoingFront_ghost,
	Stabilizing2,
	Stabilizing2_ghost,
	goneFront,
	goneFront_ghost,
} State_Sub_3;

const char* Names_Sub_3[] = {
	"GoingFront",
	"GoingFront_ghost",
	"Stabilizing2",
	"Stabilizing2_ghost",
	"goneFront",
	"goneFront_ghost",
};

typedef enum State_Sub_4 {
	empty1,
	empty1_ghost,
	empty2,
	empty2_ghost,
} State_Sub_4;

const char* Names_Sub_4[] = {
	"empty1",
	"empty1_ghost",
	"empty2",
	"empty2_ghost",
};

typedef enum State_Sub_5 {
	DoingRigthSide,
	DoingRigthSide_ghost,
	DoingTopSide,
	DoingTopSide_ghost,
	DoingLeftSide,
	DoingLeftSide_ghost,
	DoingBottomSide,
	DoingBottomSide_ghost,
} State_Sub_5;

const char* Names_Sub_5[] = {
	"DoingRigthSide",
	"DoingRigthSide_ghost",
	"DoingTopSide",
	"DoingTopSide_ghost",
	"DoingLeftSide",
	"DoingLeftSide_ghost",
	"DoingBottomSide",
	"DoingBottomSide_ghost",
};

typedef enum State_Sub_6 {
	GoingToTop,
	GoingToTop_ghost,
	StabilizingTop,
	StabilizingTop_ghost,
	GoneToTop,
	GoneToTop_ghost,
} State_Sub_6;

const char* Names_Sub_6[] = {
	"GoingToTop",
	"GoingToTop_ghost",
	"StabilizingTop",
	"StabilizingTop_ghost",
	"GoneToTop",
	"GoneToTop_ghost",
};

typedef enum State_Sub_8 {
	GoingToLeft,
	GoingToLeft_ghost,
	StabilizingLeft,
	StabilizingLeft_ghost,
	GoneToLeft,
	GoneToLeft_ghost,
} State_Sub_8;

const char* Names_Sub_8[] = {
	"GoingToLeft",
	"GoingToLeft_ghost",
	"StabilizingLeft",
	"StabilizingLeft_ghost",
	"GoneToLeft",
	"GoneToLeft_ghost",
};

typedef enum State_Sub_9 {
	GoingToBottom,
	GoingToBottom_ghost,
	StabilizingBottom,
	StabilizingBottom_ghost,
	GoneToBottom,
	GoneToBottom_ghost,
} State_Sub_9;

const char* Names_Sub_9[] = {
	"GoingToBottom",
	"GoingToBottom_ghost",
	"StabilizingBottom",
	"StabilizingBottom_ghost",
	"GoneToBottom",
	"GoneToBottom_ghost",
};

typedef enum State_Sub_10 {
	GoingToRigth,
	GoingToRigth_ghost,
	StabilizingRigth,
	StabilizingRigth_ghost,
	GoneToRigth,
	GoneToRigth_ghost,
} State_Sub_10;

const char* Names_Sub_10[] = {
	"GoingToRigth",
	"GoingToRigth_ghost",
	"StabilizingRigth",
	"StabilizingRigth_ghost",
	"GoneToRigth",
	"GoneToRigth_ghost",
};

pthread_t thr_sub_1;
pthread_t thr_sub_2;
pthread_t thr_sub_3;
pthread_t thr_sub_4;
pthread_t thr_sub_5;
pthread_t thr_sub_6;
pthread_t thr_sub_8;
pthread_t thr_sub_9;
pthread_t thr_sub_10;
pthread_t thr_automatagui;

AutomataGui *automatagui;
bool displayGui = false;

bool run1 = true;
bool run2 = true;
bool run3 = true;
bool run4 = true;
bool run5 = true;
bool run6 = true;
bool run8 = true;
bool run9 = true;
bool run10 = true;

State_Sub_1 sub_1 = TakeOff;
State_Sub_2 sub_2 = TakingOff_ghost;
State_Sub_3 sub_3 = GoingFront_ghost;
State_Sub_4 sub_4 = empty1_ghost;
State_Sub_5 sub_5 = DoingRigthSide_ghost;
State_Sub_6 sub_6 = GoingToTop_ghost;
State_Sub_8 sub_8 = GoingToLeft_ghost;
State_Sub_9 sub_9 = GoingToBottom_ghost;
State_Sub_10 sub_10 = GoingToRigth_ghost;

jderobot::Pose3DPrx pose3dprx;
jderobot::CMDVelPrx cmdVelprx;
jderobot::ArDroneExtraPrx extraprx;

void shutDown(){
	run1 = false;
	run2 = false;
	run3 = false;
	run4 = false;
	run5 = false;
	run6 = false;
	run8 = false;
	run9 = false;
	run10 = false;
	automatagui->close();
}



















std::list<GuiSubautomata> createGuiSubAutomataList(){
	std::list<GuiSubautomata> guiSubautomataList;

	GuiSubautomata* guiSubautomata1 = new GuiSubautomata(1, 0);

	guiSubautomata1->newGuiNode(1, 2, 133, 202);
	guiSubautomata1->setIsInitialLastGuiNode(1);
	guiSubautomata1->setNameLastGuiNode("TakeOff");

	guiSubautomata1->newGuiNode(5, 3, 313, 201);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("GoFront");

	guiSubautomata1->newGuiNode(14, 5, 476, 137);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("DoSquare");

	guiSubautomata1->newGuiNode(15, 0, 479, 336);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("Landing");

	guiSubautomata1->newGuiNode(16, 0, 191, 401);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("END");

	Point* origin12 = new Point(133, 202);
	Point* destiny12 = new Point(313, 201);
	Point* midPoint12 = new Point(230, 277);
	guiSubautomata1->newGuiTransition(*origin12, *destiny12, *midPoint12, 2, 1, 5);

	Point* origin16 = new Point(313, 201);
	Point* destiny16 = new Point(476, 137);
	Point* midPoint16 = new Point(394, 169);
	guiSubautomata1->newGuiTransition(*origin16, *destiny16, *midPoint16, 6, 5, 14);

	Point* origin17 = new Point(476, 137);
	Point* destiny17 = new Point(479, 336);
	Point* midPoint17 = new Point(480, 239);
	guiSubautomata1->newGuiTransition(*origin17, *destiny17, *midPoint17, 7, 14, 15);

	Point* origin18 = new Point(479, 336);
	Point* destiny18 = new Point(191, 401);
	Point* midPoint18 = new Point(335, 369);
	guiSubautomata1->newGuiTransition(*origin18, *destiny18, *midPoint18, 8, 15, 16);

	Point* origin128 = new Point(191, 401);
	Point* destiny128 = new Point(133, 202);
	Point* midPoint128 = new Point(161, 301);
	guiSubautomata1->newGuiTransition(*origin128, *destiny128, *midPoint128, 28, 16, 1);

	guiSubautomataList.push_back(*guiSubautomata1);

	GuiSubautomata* guiSubautomata2 = new GuiSubautomata(2, 1);

	guiSubautomata2->newGuiNode(2, 0, 106, 141);
	guiSubautomata2->setIsInitialLastGuiNode(1);
	guiSubautomata2->setNameLastGuiNode("TakingOff");

	guiSubautomata2->newGuiNode(3, 0, 283, 219);
	guiSubautomata2->setIsInitialLastGuiNode(0);
	guiSubautomata2->setNameLastGuiNode("Stabilizing1");

	Point* origin21 = new Point(106, 141);
	Point* destiny21 = new Point(283, 219);
	Point* midPoint21 = new Point(138, 243);
	guiSubautomata2->newGuiTransition(*origin21, *destiny21, *midPoint21, 1, 2, 3);

	Point* origin226 = new Point(283, 219);
	Point* destiny226 = new Point(106, 141);
	Point* midPoint226 = new Point(244, 116);
	guiSubautomata2->newGuiTransition(*origin226, *destiny226, *midPoint226, 26, 3, 2);

	guiSubautomataList.push_back(*guiSubautomata2);

	GuiSubautomata* guiSubautomata3 = new GuiSubautomata(3, 1);

	guiSubautomata3->newGuiNode(9, 0, 127, 107);
	guiSubautomata3->setIsInitialLastGuiNode(1);
	guiSubautomata3->setNameLastGuiNode("GoingFront");

	guiSubautomata3->newGuiNode(10, 4, 511, 137);
	guiSubautomata3->setIsInitialLastGuiNode(0);
	guiSubautomata3->setNameLastGuiNode("Stabilizing2");

	guiSubautomata3->newGuiNode(11, 0, 298, 291);
	guiSubautomata3->setIsInitialLastGuiNode(0);
	guiSubautomata3->setNameLastGuiNode("goneFront");

	Point* origin32 = new Point(127, 107);
	Point* destiny32 = new Point(511, 137);
	Point* midPoint32 = new Point(319, 123);
	guiSubautomata3->newGuiTransition(*origin32, *destiny32, *midPoint32, 2, 9, 10);

	Point* origin33 = new Point(511, 137);
	Point* destiny33 = new Point(298, 291);
	Point* midPoint33 = new Point(405, 214);
	guiSubautomata3->newGuiTransition(*origin33, *destiny33, *midPoint33, 3, 10, 11);

	Point* origin327 = new Point(298, 291);
	Point* destiny327 = new Point(127, 107);
	Point* midPoint327 = new Point(212, 199);
	guiSubautomata3->newGuiTransition(*origin327, *destiny327, *midPoint327, 27, 11, 9);

	guiSubautomataList.push_back(*guiSubautomata3);

	GuiSubautomata* guiSubautomata4 = new GuiSubautomata(4, 3);

	guiSubautomata4->newGuiNode(12, 0, 232, 178);
	guiSubautomata4->setIsInitialLastGuiNode(1);
	guiSubautomata4->setNameLastGuiNode("empty1");

	guiSubautomata4->newGuiNode(13, 0, 445, 217);
	guiSubautomata4->setIsInitialLastGuiNode(0);
	guiSubautomata4->setNameLastGuiNode("empty2");

	Point* origin44 = new Point(232, 178);
	Point* destiny44 = new Point(445, 217);
	Point* midPoint44 = new Point(357, 129);
	guiSubautomata4->newGuiTransition(*origin44, *destiny44, *midPoint44, 4, 12, 13);

	Point* origin45 = new Point(445, 217);
	Point* destiny45 = new Point(232, 178);
	Point* midPoint45 = new Point(316, 271);
	guiSubautomata4->newGuiTransition(*origin45, *destiny45, *midPoint45, 5, 13, 12);

	guiSubautomataList.push_back(*guiSubautomata4);

	GuiSubautomata* guiSubautomata5 = new GuiSubautomata(5, 1);

	guiSubautomata5->newGuiNode(17, 6, 465, 388);
	guiSubautomata5->setIsInitialLastGuiNode(1);
	guiSubautomata5->setNameLastGuiNode("DoingRigthSide");

	guiSubautomata5->newGuiNode(18, 8, 461, 140);
	guiSubautomata5->setIsInitialLastGuiNode(0);
	guiSubautomata5->setNameLastGuiNode("DoingTopSide");

	guiSubautomata5->newGuiNode(19, 9, 134, 130);
	guiSubautomata5->setIsInitialLastGuiNode(0);
	guiSubautomata5->setNameLastGuiNode("DoingLeftSide");

	guiSubautomata5->newGuiNode(20, 10, 141, 389);
	guiSubautomata5->setIsInitialLastGuiNode(0);
	guiSubautomata5->setNameLastGuiNode("DoingBottomSide");

	Point* origin59 = new Point(465, 388);
	Point* destiny59 = new Point(461, 140);
	Point* midPoint59 = new Point(463, 264);
	guiSubautomata5->newGuiTransition(*origin59, *destiny59, *midPoint59, 9, 17, 18);

	Point* origin510 = new Point(461, 140);
	Point* destiny510 = new Point(134, 130);
	Point* midPoint510 = new Point(298, 136);
	guiSubautomata5->newGuiTransition(*origin510, *destiny510, *midPoint510, 10, 18, 19);

	Point* origin511 = new Point(134, 130);
	Point* destiny511 = new Point(141, 389);
	Point* midPoint511 = new Point(137, 260);
	guiSubautomata5->newGuiTransition(*origin511, *destiny511, *midPoint511, 11, 19, 20);

	Point* origin512 = new Point(141, 389);
	Point* destiny512 = new Point(465, 388);
	Point* midPoint512 = new Point(303, 388);
	guiSubautomata5->newGuiTransition(*origin512, *destiny512, *midPoint512, 12, 20, 17);

	guiSubautomataList.push_back(*guiSubautomata5);

	GuiSubautomata* guiSubautomata6 = new GuiSubautomata(6, 5);

	guiSubautomata6->newGuiNode(21, 0, 352, 452);
	guiSubautomata6->setIsInitialLastGuiNode(1);
	guiSubautomata6->setNameLastGuiNode("GoingToTop");

	guiSubautomata6->newGuiNode(22, 0, 280, 218);
	guiSubautomata6->setIsInitialLastGuiNode(0);
	guiSubautomata6->setNameLastGuiNode("StabilizingTop");

	guiSubautomata6->newGuiNode(23, 0, 448, 105);
	guiSubautomata6->setIsInitialLastGuiNode(0);
	guiSubautomata6->setNameLastGuiNode("GoneToTop");

	Point* origin613 = new Point(352, 452);
	Point* destiny613 = new Point(280, 218);
	Point* midPoint613 = new Point(212, 319);
	guiSubautomata6->newGuiTransition(*origin613, *destiny613, *midPoint613, 13, 21, 22);

	Point* origin614 = new Point(280, 218);
	Point* destiny614 = new Point(448, 105);
	Point* midPoint614 = new Point(350, 132);
	guiSubautomata6->newGuiTransition(*origin614, *destiny614, *midPoint614, 14, 22, 23);

	Point* origin616 = new Point(448, 105);
	Point* destiny616 = new Point(352, 452);
	Point* midPoint616 = new Point(400, 279);
	guiSubautomata6->newGuiTransition(*origin616, *destiny616, *midPoint616, 16, 23, 21);

	guiSubautomataList.push_back(*guiSubautomata6);

	GuiSubautomata* guiSubautomata8 = new GuiSubautomata(8, 5);

	guiSubautomata8->newGuiNode(24, 0, 135, 397);
	guiSubautomata8->setIsInitialLastGuiNode(1);
	guiSubautomata8->setNameLastGuiNode("GoingToLeft");

	guiSubautomata8->newGuiNode(25, 0, 213, 194);
	guiSubautomata8->setIsInitialLastGuiNode(0);
	guiSubautomata8->setNameLastGuiNode("StabilizingLeft");

	guiSubautomata8->newGuiNode(26, 0, 416, 260);
	guiSubautomata8->setIsInitialLastGuiNode(0);
	guiSubautomata8->setNameLastGuiNode("GoneToLeft");

	Point* origin817 = new Point(135, 397);
	Point* destiny817 = new Point(213, 194);
	Point* midPoint817 = new Point(174, 295);
	guiSubautomata8->newGuiTransition(*origin817, *destiny817, *midPoint817, 17, 24, 25);

	Point* origin818 = new Point(213, 194);
	Point* destiny818 = new Point(416, 260);
	Point* midPoint818 = new Point(314, 227);
	guiSubautomata8->newGuiTransition(*origin818, *destiny818, *midPoint818, 18, 25, 26);

	Point* origin819 = new Point(416, 260);
	Point* destiny819 = new Point(135, 397);
	Point* midPoint819 = new Point(275, 328);
	guiSubautomata8->newGuiTransition(*origin819, *destiny819, *midPoint819, 19, 26, 24);

	guiSubautomataList.push_back(*guiSubautomata8);

	GuiSubautomata* guiSubautomata9 = new GuiSubautomata(9, 5);

	guiSubautomata9->newGuiNode(27, 0, 169, 408);
	guiSubautomata9->setIsInitialLastGuiNode(1);
	guiSubautomata9->setNameLastGuiNode("GoingToBottom");

	guiSubautomata9->newGuiNode(28, 0, 243, 164);
	guiSubautomata9->setIsInitialLastGuiNode(0);
	guiSubautomata9->setNameLastGuiNode("StabilizingBottom");

	guiSubautomata9->newGuiNode(29, 0, 418, 355);
	guiSubautomata9->setIsInitialLastGuiNode(0);
	guiSubautomata9->setNameLastGuiNode("GoneToBottom");

	Point* origin920 = new Point(169, 408);
	Point* destiny920 = new Point(243, 164);
	Point* midPoint920 = new Point(206, 286);
	guiSubautomata9->newGuiTransition(*origin920, *destiny920, *midPoint920, 20, 27, 28);

	Point* origin921 = new Point(243, 164);
	Point* destiny921 = new Point(418, 355);
	Point* midPoint921 = new Point(330, 259);
	guiSubautomata9->newGuiTransition(*origin921, *destiny921, *midPoint921, 21, 28, 29);

	Point* origin922 = new Point(418, 355);
	Point* destiny922 = new Point(169, 408);
	Point* midPoint922 = new Point(293, 381);
	guiSubautomata9->newGuiTransition(*origin922, *destiny922, *midPoint922, 22, 29, 27);

	guiSubautomataList.push_back(*guiSubautomata9);

	GuiSubautomata* guiSubautomata10 = new GuiSubautomata(10, 5);

	guiSubautomata10->newGuiNode(31, 0, 121, 361);
	guiSubautomata10->setIsInitialLastGuiNode(1);
	guiSubautomata10->setNameLastGuiNode("GoingToRigth");

	guiSubautomata10->newGuiNode(32, 0, 231, 110);
	guiSubautomata10->setIsInitialLastGuiNode(0);
	guiSubautomata10->setNameLastGuiNode("StabilizingRigth");

	guiSubautomata10->newGuiNode(33, 0, 371, 331);
	guiSubautomata10->setIsInitialLastGuiNode(0);
	guiSubautomata10->setNameLastGuiNode("GoneToRigth");

	Point* origin1023 = new Point(121, 361);
	Point* destiny1023 = new Point(231, 110);
	Point* midPoint1023 = new Point(176, 235);
	guiSubautomata10->newGuiTransition(*origin1023, *destiny1023, *midPoint1023, 23, 31, 32);

	Point* origin1024 = new Point(231, 110);
	Point* destiny1024 = new Point(371, 331);
	Point* midPoint1024 = new Point(300, 220);
	guiSubautomata10->newGuiTransition(*origin1024, *destiny1024, *midPoint1024, 24, 32, 33);

	Point* origin1025 = new Point(371, 331);
	Point* destiny1025 = new Point(121, 361);
	Point* midPoint1025 = new Point(246, 346);
	guiSubautomata10->newGuiTransition(*origin1025, *destiny1025, *midPoint1025, 25, 33, 31);

	guiSubautomataList.push_back(*guiSubautomata10);

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

	self.goneFront = False
	self.squareDone = False

	while (run1) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		// Evaluation switch
		switch (sub_1) {
			case TakeOff: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) 3.5) {
						sub_1 = GoFront;
						t_activated = false;
						print "From TakeOff to GoFront"
						if (displayGui){
							automatagui->notifySetNodeAsActive("GoFront");
						}
					}
				}

				break;
			}
			case GoFront: {
				if (self.goneFront) {
					sub_1 = DoSquare;
						self.goneFront = False
					if(displayGui){
						automatagui->notifySetNodeAsActive("DoSquare");
					}
				}

				break;
			}
			case DoSquare: {
				if (self.squareDone) {
					sub_1 = Landing;
						self.squareDone = False
					if(displayGui){
						automatagui->notifySetNodeAsActive("Landing");
					}
				}

				break;
			}
			case Landing: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) 2) {
						sub_1 = END;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("END");
						}
					}
				}

				break;
			}
			case END: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) 3) {
						sub_1 = TakeOff;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("TakeOff");
						}
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_1) {
			case TakeOff: {
				break;
			}
			case GoFront: {
				break;
			}
			case DoSquare: {
				break;
			}
			case Landing: {
				print "landing"
				self.lock.acquire()
				self.extraPrx.land()
				self.lock.release()
				break;
			}
			case END: {
				print "END"
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

	float t_TakingOff_max = 2;
	float t_Stabilizing1_max = 1.7;

	while (run2) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		if (sub_1 == TakeOff) {
			if ( sub_2 == TakingOff_ghost || sub_2 == Stabilizing1_ghost) {
				sub_2 = (State_Sub_2)(sub_2 - 1);
				t_ini = time(NULL);
			}
		// Evaluation switch
		switch (sub_2) {
			case TakingOff: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_TakingOff_max) {
						sub_2 = Stabilizing1;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("Stabilizing1");
						}
						t_TakingOff_max = 2;
					}
				}

				break;
			}
			case Stabilizing1: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_Stabilizing1_max) {
						sub_2 = TakingOff;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("TakingOff");
						}
						t_Stabilizing1_max = 1.7;
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_2) {
			case TakingOff: {
				print "Taking Off"
				self.lock.acquire()
				self.extraPrx.takeoff()
				self.lock.release()
				break;
			}
			case Stabilizing1: {
				break;
			}
		}
		} else {
			switch (sub_2) {
				case TakingOff:
					t_TakingOff_max = 2 - difftime(t_fin, t_ini);
					sub_2 = (State_Sub_2)(sub_2 + 1);
					break;
				case Stabilizing1:
					t_Stabilizing1_max = 1.7 - difftime(t_fin, t_ini);
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

	float t_Stabilizing2_max = 3;
	float t_goneFront_max = 0.2;
	initPos = 0
	pos = 0

	while (run3) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		if (sub_1 == GoFront) {
			if ( sub_3 == GoingFront_ghost || sub_3 == Stabilizing2_ghost || sub_3 == goneFront_ghost) {
				sub_3 = (State_Sub_3)(sub_3 - 1);
				t_ini = time(NULL);
			}
		// Evaluation switch
		switch (sub_3) {
			case GoingFront: {
				if (pos - initPos > 300) {
					sub_3 = Stabilizing2;
						print "300m reached"
					if(displayGui){
						automatagui->notifySetNodeAsActive("Stabilizing2");
					}
				}

				break;
			}
			case Stabilizing2: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_Stabilizing2_max) {
						sub_3 = goneFront;
						t_activated = false;
						print "from stabilizing2 to GoneFront"
						if (displayGui){
							automatagui->notifySetNodeAsActive("goneFront");
						}
						t_Stabilizing2_max = 3;
					}
				}

				break;
			}
			case goneFront: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_goneFront_max) {
						sub_3 = GoingFront;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("GoingFront");
						}
						t_goneFront_max = 0.2;
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_3) {
			case GoingFront: {
				pos = self.pose3dPrx.getPose3DData().x * 100
				
				if initPos == 0:
					initPos = self.pose3dPrx.getPose3DData().x * 100
				
				print "pos:", pos, "init:", initPos
				print "distancia", pos - initPos
				
				cmd = jderobot.CMDVelData()
				cmd.linearX = 1
				cmd.linearY = 0
				cmd.linearZ = 0
				self.lock.acquire()
				self.cmdVelPrx.setCMDVelData(cmd)
				self.lock.release()
				break;
			}
			case Stabilizing2: {
				cmd.linearX = 0
				cmd.linearY = 0
				cmd.linearZ = 0
				self.lock.acquire()
				self.cmdVelPrx.setCMDVelData(cmd)
				self.lock.release()
				break;
			}
			case goneFront: {
				self.goneFront = True
				break;
			}
		}
		} else {
			switch (sub_3) {
				case GoingFront:
					sub_3 = (State_Sub_3)(sub_3 + 1);
					break;
				case Stabilizing2:
					t_Stabilizing2_max = 3 - difftime(t_fin, t_ini);
					sub_3 = (State_Sub_3)(sub_3 + 1);
					break;
				case goneFront:
					t_goneFront_max = 0.2 - difftime(t_fin, t_ini);
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

void* subautomata_4 ( void* ) {
	struct timeval a, b;
	int cycle = 100;
	long totala, totalb;
	long diff;
	time_t t_ini;
	time_t t_fin;
	double secs;
	bool t_activated;

	float t_empty1_max = 0.8;
	float t_empty2_max = 0.8;

	while (run4) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		if (sub_3 == Stabilizing2) {
			if ( sub_4 == empty1_ghost || sub_4 == empty2_ghost) {
				sub_4 = (State_Sub_4)(sub_4 - 1);
				t_ini = time(NULL);
			}
		// Evaluation switch
		switch (sub_4) {
			case empty1: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_empty1_max) {
						sub_4 = empty2;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("empty2");
						}
						t_empty1_max = 0.8;
					}
				}

				break;
			}
			case empty2: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_empty2_max) {
						sub_4 = empty1;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("empty1");
						}
						t_empty2_max = 0.8;
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_4) {
			case empty1: {
				break;
			}
			case empty2: {
				break;
			}
		}
		} else {
			switch (sub_4) {
				case empty1:
					t_empty1_max = 0.8 - difftime(t_fin, t_ini);
					sub_4 = (State_Sub_4)(sub_4 + 1);
					break;
				case empty2:
					t_empty2_max = 0.8 - difftime(t_fin, t_ini);
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

	float t_DoingTopSide_max = 0;
	float t_DoingLeftSide_max = 0;
	float t_DoingBottomSide_max = 0;
	self.goneToTop = False
	self.goneToLeft = False
	self.goneToBottom = False
	self.goneToRigth = False

	while (run5) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		if (sub_1 == DoSquare) {
			if ( sub_5 == DoingRigthSide_ghost || sub_5 == DoingTopSide_ghost || sub_5 == DoingLeftSide_ghost || sub_5 == DoingBottomSide_ghost) {
				sub_5 = (State_Sub_5)(sub_5 - 1);
				t_ini = time(NULL);
			}
		// Evaluation switch
		switch (sub_5) {
			case DoingRigthSide: {
				if (self.goneToTop) {
					sub_5 = DoingTopSide;
						print "Rigth Done"
					if(displayGui){
						automatagui->notifySetNodeAsActive("DoingTopSide");
					}
				}

				break;
			}
			case DoingTopSide: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_DoingTopSide_max) {
						sub_5 = DoingLeftSide;
						t_activated = false;
						print "Side done"
						if (displayGui){
							automatagui->notifySetNodeAsActive("DoingLeftSide");
						}
						t_DoingTopSide_max = 0;
					}
				}

				break;
			}
			case DoingLeftSide: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_DoingLeftSide_max) {
						sub_5 = DoingBottomSide;
						t_activated = false;
						print "Left done"
						if (displayGui){
							automatagui->notifySetNodeAsActive("DoingBottomSide");
						}
						t_DoingLeftSide_max = 0;
					}
				}

				break;
			}
			case DoingBottomSide: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_DoingBottomSide_max) {
						sub_5 = DoingRigthSide;
						t_activated = false;
						self.squareDone = True
						print "Bottom done"
						if (displayGui){
							automatagui->notifySetNodeAsActive("DoingRigthSide");
						}
						t_DoingBottomSide_max = 0;
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_5) {
			case DoingRigthSide: {
				print "Doing Rigth Side"
				break;
			}
			case DoingTopSide: {
				print "Doing Top Side"
				break;
			}
			case DoingLeftSide: {
				print "Doing Left Side"
				break;
			}
			case DoingBottomSide: {
				print "Doing Bottom Side"
				break;
			}
		}
		} else {
			switch (sub_5) {
				case DoingRigthSide:
					sub_5 = (State_Sub_5)(sub_5 + 1);
					break;
				case DoingTopSide:
					t_DoingTopSide_max = 0 - difftime(t_fin, t_ini);
					sub_5 = (State_Sub_5)(sub_5 + 1);
					break;
				case DoingLeftSide:
					t_DoingLeftSide_max = 0 - difftime(t_fin, t_ini);
					sub_5 = (State_Sub_5)(sub_5 + 1);
					break;
				case DoingBottomSide:
					t_DoingBottomSide_max = 0 - difftime(t_fin, t_ini);
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

void* subautomata_6 ( void* ) {
	struct timeval a, b;
	int cycle = 100;
	long totala, totalb;
	long diff;
	time_t t_ini;
	time_t t_fin;
	double secs;
	bool t_activated;

	float t_GoingToTop_max = 3;
	float t_StabilizingTop_max = 2;
	float t_GoneToTop_max = 0.1;

	while (run6) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		if (sub_5 == DoingRigthSide) {
			if ( sub_6 == GoingToTop_ghost || sub_6 == StabilizingTop_ghost || sub_6 == GoneToTop_ghost) {
				sub_6 = (State_Sub_6)(sub_6 - 1);
				t_ini = time(NULL);
			}
		// Evaluation switch
		switch (sub_6) {
			case GoingToTop: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_GoingToTop_max) {
						sub_6 = StabilizingTop;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("StabilizingTop");
						}
						t_GoingToTop_max = 3;
					}
				}

				break;
			}
			case StabilizingTop: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_StabilizingTop_max) {
						sub_6 = GoneToTop;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("GoneToTop");
						}
						t_StabilizingTop_max = 2;
					}
				}

				break;
			}
			case GoneToTop: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_GoneToTop_max) {
						sub_6 = GoingToTop;
						t_activated = false;
						self.GoneToTop = False
						if (displayGui){
							automatagui->notifySetNodeAsActive("GoingToTop");
						}
						t_GoneToTop_max = 0.1;
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_6) {
			case GoingToTop: {
				cmd = jderobot.CMDVelData()
				cmd.linearX = 0.75
				cmd.linearY = 0
				cmd.linearZ = 0
				self.lock.acquire()
				self.cmdVelPrx.setCMDVelData(cmd)
				self.lock.release()
				break;
			}
			case StabilizingTop: {
				cmd.linearX = 0
				cmd.linearY = 0
				cmd.linearZ = 0
				self.lock.acquire()
				self.cmdVelPrx.setCMDVelData(cmd)
				self.lock.release()
				break;
			}
			case GoneToTop: {
				self.goneToTop = True
				break;
			}
		}
		} else {
			switch (sub_6) {
				case GoingToTop:
					t_GoingToTop_max = 3 - difftime(t_fin, t_ini);
					sub_6 = (State_Sub_6)(sub_6 + 1);
					break;
				case StabilizingTop:
					t_StabilizingTop_max = 2 - difftime(t_fin, t_ini);
					sub_6 = (State_Sub_6)(sub_6 + 1);
					break;
				case GoneToTop:
					t_GoneToTop_max = 0.1 - difftime(t_fin, t_ini);
					sub_6 = (State_Sub_6)(sub_6 + 1);
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

void* subautomata_8 ( void* ) {
	struct timeval a, b;
	int cycle = 100;
	long totala, totalb;
	long diff;
	time_t t_ini;
	time_t t_fin;
	double secs;
	bool t_activated;

	float t_GoingToLeft_max = 3;
	float t_StabilizingLeft_max = 2;
	float t_GoneToLeft_max = 0.1;

	while (run8) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		if (sub_5 == DoingTopSide) {
			if ( sub_8 == GoingToLeft_ghost || sub_8 == StabilizingLeft_ghost || sub_8 == GoneToLeft_ghost) {
				sub_8 = (State_Sub_8)(sub_8 - 1);
				t_ini = time(NULL);
			}
		// Evaluation switch
		switch (sub_8) {
			case GoingToLeft: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_GoingToLeft_max) {
						sub_8 = StabilizingLeft;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("StabilizingLeft");
						}
						t_GoingToLeft_max = 3;
					}
				}

				break;
			}
			case StabilizingLeft: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_StabilizingLeft_max) {
						sub_8 = GoneToLeft;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("GoneToLeft");
						}
						t_StabilizingLeft_max = 2;
					}
				}

				break;
			}
			case GoneToLeft: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_GoneToLeft_max) {
						sub_8 = GoingToLeft;
						t_activated = false;
						self.goneToLeft = False
						if (displayGui){
							automatagui->notifySetNodeAsActive("GoingToLeft");
						}
						t_GoneToLeft_max = 0.1;
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_8) {
			case GoingToLeft: {
				cmd = jderobot.CMDVelData()
				cmd.linearX = 0
				cmd.linearY = -0.75
				cmd.linearZ = 0
				self.lock.acquire()
				self.cmdVelPrx.setCMDVelData(cmd)
				self.lock.release()
				break;
			}
			case StabilizingLeft: {
				cmd = jderobot.CMDVelData()
				cmd.linearX = 0
				cmd.linearY = 0
				cmd.linearZ = 0
				self.lock.acquire()
				self.cmdVelPrx.setCMDVelData(cmd)
				self.lock.release()
				break;
			}
			case GoneToLeft: {
				self.goneToLeft = True
				break;
			}
		}
		} else {
			switch (sub_8) {
				case GoingToLeft:
					t_GoingToLeft_max = 3 - difftime(t_fin, t_ini);
					sub_8 = (State_Sub_8)(sub_8 + 1);
					break;
				case StabilizingLeft:
					t_StabilizingLeft_max = 2 - difftime(t_fin, t_ini);
					sub_8 = (State_Sub_8)(sub_8 + 1);
					break;
				case GoneToLeft:
					t_GoneToLeft_max = 0.1 - difftime(t_fin, t_ini);
					sub_8 = (State_Sub_8)(sub_8 + 1);
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

void* subautomata_9 ( void* ) {
	struct timeval a, b;
	int cycle = 100;
	long totala, totalb;
	long diff;
	time_t t_ini;
	time_t t_fin;
	double secs;
	bool t_activated;

	float t_GoingToBottom_max = 3;
	float t_StabilizingBottom_max = 2;
	float t_GoneToBottom_max = 0.1;

	while (run9) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		if (sub_5 == DoingLeftSide) {
			if ( sub_9 == GoingToBottom_ghost || sub_9 == StabilizingBottom_ghost || sub_9 == GoneToBottom_ghost) {
				sub_9 = (State_Sub_9)(sub_9 - 1);
				t_ini = time(NULL);
			}
		// Evaluation switch
		switch (sub_9) {
			case GoingToBottom: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_GoingToBottom_max) {
						sub_9 = StabilizingBottom;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("StabilizingBottom");
						}
						t_GoingToBottom_max = 3;
					}
				}

				break;
			}
			case StabilizingBottom: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_StabilizingBottom_max) {
						sub_9 = GoneToBottom;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("GoneToBottom");
						}
						t_StabilizingBottom_max = 2;
					}
				}

				break;
			}
			case GoneToBottom: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_GoneToBottom_max) {
						sub_9 = GoingToBottom;
						t_activated = false;
						self.goneToBottom = False
						if (displayGui){
							automatagui->notifySetNodeAsActive("GoingToBottom");
						}
						t_GoneToBottom_max = 0.1;
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_9) {
			case GoingToBottom: {
				cmd = jderobot.CMDVelData()
				cmd.linearX = -0.75
				cmd.linearY = 0
				cmd.linearZ = 0
				self.lock.acquire()
				self.cmdVelPrx.setCMDVelData(cmd)
				self.lock.release()
				break;
			}
			case StabilizingBottom: {
				cmd = jderobot.CMDVelData()
				cmd.linearX = 0
				cmd.linearY = 0
				cmd.linearZ = 0
				self.lock.acquire()
				self.cmdVelPrx.setCMDVelData(cmd)
				self.lock.release()
				break;
			}
			case GoneToBottom: {
				self.goneToBottom = True
				break;
			}
		}
		} else {
			switch (sub_9) {
				case GoingToBottom:
					t_GoingToBottom_max = 3 - difftime(t_fin, t_ini);
					sub_9 = (State_Sub_9)(sub_9 + 1);
					break;
				case StabilizingBottom:
					t_StabilizingBottom_max = 2 - difftime(t_fin, t_ini);
					sub_9 = (State_Sub_9)(sub_9 + 1);
					break;
				case GoneToBottom:
					t_GoneToBottom_max = 0.1 - difftime(t_fin, t_ini);
					sub_9 = (State_Sub_9)(sub_9 + 1);
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

void* subautomata_10 ( void* ) {
	struct timeval a, b;
	int cycle = 100;
	long totala, totalb;
	long diff;
	time_t t_ini;
	time_t t_fin;
	double secs;
	bool t_activated;

	float t_GoingToRigth_max = 3;
	float t_StabilizingRigth_max = 2;
	float t_GoneToRigth_max = 0.1;

	while (run10) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		if (sub_5 == DoingBottomSide) {
			if ( sub_10 == GoingToRigth_ghost || sub_10 == StabilizingRigth_ghost || sub_10 == GoneToRigth_ghost) {
				sub_10 = (State_Sub_10)(sub_10 - 1);
				t_ini = time(NULL);
			}
		// Evaluation switch
		switch (sub_10) {
			case GoingToRigth: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_GoingToRigth_max) {
						sub_10 = StabilizingRigth;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("StabilizingRigth");
						}
						t_GoingToRigth_max = 3;
					}
				}

				break;
			}
			case StabilizingRigth: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_StabilizingRigth_max) {
						sub_10 = GoneToRigth;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("GoneToRigth");
						}
						t_StabilizingRigth_max = 2;
					}
				}

				break;
			}
			case GoneToRigth: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) t_GoneToRigth_max) {
						sub_10 = GoingToRigth;
						t_activated = false;
						self.goneToRigth = False
						if (displayGui){
							automatagui->notifySetNodeAsActive("GoingToRigth");
						}
						t_GoneToRigth_max = 0.1;
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_10) {
			case GoingToRigth: {
				cmd = jderobot.CMDVelData()
				cmd.linearX = 0
				cmd.linearY = 0.75
				cmd.linearZ = 0
				self.lock.acquire()
				self.cmdVelPrx.setCMDVelData(cmd)
				self.lock.release()
				break;
			}
			case StabilizingRigth: {
				cmd = jderobot.CMDVelData()
				cmd.linearX = 0
				cmd.linearY = 0
				cmd.linearZ = 0
				self.lock.acquire()
				self.cmdVelPrx.setCMDVelData(cmd)
				self.lock.release()
				break;
			}
			case GoneToRigth: {
				self.goneToRigth = True
				break;
			}
		}
		} else {
			switch (sub_10) {
				case GoingToRigth:
					t_GoingToRigth_max = 3 - difftime(t_fin, t_ini);
					sub_10 = (State_Sub_10)(sub_10 + 1);
					break;
				case StabilizingRigth:
					t_StabilizingRigth_max = 2 - difftime(t_fin, t_ini);
					sub_10 = (State_Sub_10)(sub_10 + 1);
					break;
				case GoneToRigth:
					t_GoneToRigth_max = 0.1 - difftime(t_fin, t_ini);
					sub_10 = (State_Sub_10)(sub_10 + 1);
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
		readArgs(argc, argv);

		// Contact to pose3d
		Ice::ObjectPrx pose3d = ic->propertyToProxy("automata.pose3d.Proxy");
		if (pose3d == 0)
			throw "Could not create proxy with pose3d";
		pose3dprx = jderobot::Pose3DPrx::checkedCast(pose3d);
		if (pose3dprx == 0)
			throw "Invalid proxy automata.pose3d.Proxy";
		std::cout << "pose3d connected" << std::endl;

		// Contact to cmdVel
		Ice::ObjectPrx cmdVel = ic->propertyToProxy("automata.cmdVel.Proxy");
		if (cmdVel == 0)
			throw "Could not create proxy with cmdVel";
		cmdVelprx = jderobot::CMDVelPrx::checkedCast(cmdVel);
		if (cmdVelprx == 0)
			throw "Invalid proxy automata.cmdVel.Proxy";
		std::cout << "cmdVel connected" << std::endl;

		// Contact to extra
		Ice::ObjectPrx extra = ic->propertyToProxy("automata.extra.Proxy");
		if (extra == 0)
			throw "Could not create proxy with extra";
		extraprx = jderobot::ArDroneExtraPrx::checkedCast(extra);
		if (extraprx == 0)
			throw "Invalid proxy automata.extra.Proxy";
		std::cout << "extra connected" << std::endl;

		if (displayGui){
			automatagui = new AutomataGui(argc, argv);
			displayGui = showAutomataGui();

		pthread_create(&thr_sub_1, NULL, &subautomata_1, NULL);
		pthread_create(&thr_sub_2, NULL, &subautomata_2, NULL);
		pthread_create(&thr_sub_3, NULL, &subautomata_3, NULL);
		pthread_create(&thr_sub_4, NULL, &subautomata_4, NULL);
		pthread_create(&thr_sub_5, NULL, &subautomata_5, NULL);
		pthread_create(&thr_sub_6, NULL, &subautomata_6, NULL);
		pthread_create(&thr_sub_8, NULL, &subautomata_8, NULL);
		pthread_create(&thr_sub_9, NULL, &subautomata_9, NULL);
		pthread_create(&thr_sub_10, NULL, &subautomata_10, NULL);

		pthread_join(thr_sub_1, NULL);
		pthread_join(thr_sub_2, NULL);
		pthread_join(thr_sub_3, NULL);
		pthread_join(thr_sub_4, NULL);
		pthread_join(thr_sub_5, NULL);
		pthread_join(thr_sub_6, NULL);
		pthread_join(thr_sub_8, NULL);
		pthread_join(thr_sub_9, NULL);
		pthread_join(thr_sub_10, NULL);
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
