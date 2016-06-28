#include <Ice/Ice.h>
#include <IceUtil/IceUtil.h>
#include <jderobot/visualHFSM/automatagui.h>

#include <jderobot>

#include <jderobot/camera.h>
#include <jderobot/pose3d.h>
#include <jderobot/cmdvel.h>
#include <jderobot/ardroneextra.h>
#include <jderobot/navdata.h>

typedef enum State_Sub_1 {
	TakeOff,
	Stabilizing1,
	GoFront,
	Stoping,
	Landing,
	Stabilizing2,
} State_Sub_1;

const char* Names_Sub_1[] = {
	"TakeOff",
	"Stabilizing1",
	"GoFront",
	"Stoping",
	"Landing",
	"Stabilizing2",
};

pthread_t thr_sub_1;
pthread_t thr_automatagui;

AutomataGui *automatagui;
bool displayAutomataGui;

bool run1 = true;

State_Sub_1 sub_1 = TakeOff;

jderobot::CameraPrx cameraprx;
jderobot::Pose3DPrx pose3dprx;
jderobot::CMDVelPrx cmdprx;
jderobot::ArDroneExtraPrx extraprx;
jderobot::NavdataPrx navdataprx;

void shutDown(){
	run1 = false;
	automatagui->close();
}

def finished():
	print "FINISHED!"

std::list<GuiSubautomata> createGuiSubAutomataList(){
	std::list<GuiSubautomata> guiSubautomataList;

	GuiSubautomata* guiSubautomata1 = new GuiSubautomata(1, 0);

	guiSubautomata1->newGuiNode(1, 0, 61, 101);
	guiSubautomata1->setIsInitialLastGuiNode(1);
	guiSubautomata1->setNameLastGuiNode("TakeOff");

	guiSubautomata1->newGuiNode(2, 0, 283, 75);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("Stabilizing1");

	guiSubautomata1->newGuiNode(3, 0, 497, 130);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("GoFront");

	guiSubautomata1->newGuiNode(4, 0, 488, 320);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("Stoping");

	guiSubautomata1->newGuiNode(5, 0, 250, 408);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("Landing");

	guiSubautomata1->newGuiNode(6, 0, 66, 283);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("Stabilizing2");

	Point* origin11 = new Point(61, 101);
	Point* destiny11 = new Point(283, 75);
	Point* midPoint11 = new Point(49, 191);
	guiSubautomata1->newGuiTransition(*origin11, *destiny11, *midPoint11, 1, 1, 2);

	Point* origin12 = new Point(283, 75);
	Point* destiny12 = new Point(497, 130);
	Point* midPoint12 = new Point(413, 79);
	guiSubautomata1->newGuiTransition(*origin12, *destiny12, *midPoint12, 2, 2, 3);

	Point* origin13 = new Point(497, 130);
	Point* destiny13 = new Point(488, 320);
	Point* midPoint13 = new Point(570, 239);
	guiSubautomata1->newGuiTransition(*origin13, *destiny13, *midPoint13, 3, 3, 4);

	Point* origin14 = new Point(488, 320);
	Point* destiny14 = new Point(250, 408);
	Point* midPoint14 = new Point(410, 411);
	guiSubautomata1->newGuiTransition(*origin14, *destiny14, *midPoint14, 4, 4, 5);

	Point* origin16 = new Point(250, 408);
	Point* destiny16 = new Point(66, 283);
	Point* midPoint16 = new Point(152, 338);
	guiSubautomata1->newGuiTransition(*origin16, *destiny16, *midPoint16, 6, 5, 6);

	Point* origin11 = new Point(66, 283);
	Point* destiny11 = new Point(61, 101);
	Point* midPoint11 = new Point(49, 191);
	guiSubautomata1->newGuiTransition(*origin11, *destiny11, *midPoint11, 1, 6, 1);

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

	hasTakenOff = False
	hasLanded = False

	while (run1) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		// Evaluation switch
		switch (sub_1) {
			case TakeOff: {
				if (hasTakenOff) {
					sub_1 = Stabilizing1;
						print "Going to Stabilizing"
					automatagui->notifySetNodeAsActive("Stabilizing1");
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
					if (secs > (double) 1.5) {
						sub_1 = GoFront;
						t_activated = false;
						print "going to GoFront"
						automatagui->notifySetNodeAsActive("GoFront");
					}
				}

				break;
			}
			case GoFront: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) 3) {
						sub_1 = Stoping;
						t_activated = false;
						print "going to Stoping"
						automatagui->notifySetNodeAsActive("Stoping");
					}
				}

				break;
			}
			case Stoping: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) 3.5) {
						sub_1 = Landing;
						t_activated = false;
						print "going to Land"
						automatagui->notifySetNodeAsActive("Landing");
					}
				}

				break;
			}
			case Landing: {
				if (hasLanded) {
					sub_1 = Stabilizing2;
					automatagui->notifySetNodeAsActive("Stabilizing2");
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
					if (secs > (double) 3) {
						sub_1 = TakeOff;
						t_activated = false;
						print "Restarting"
						automatagui->notifySetNodeAsActive("TakeOff");
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_1) {
			case TakeOff: {
				print "Taking Off"
				self.lock.acquire()
				self.extraPrx.takeoff()
				self.lock.release()
				hasTakenOff = True
				break;
			}
			case Stabilizing1: {
				print "Stabilizing"
				break;
			}
			case GoFront: {
				cmd = jderobot.CMDVelData()
				cmd.linearX = 1
				cmd.linearY = 0
				cmd.linearZ = 0
				self.lock.acquire()
				self.cmdPrx.setCMDVelData(cmd)
				self.lock.release()
				break;
			}
			case Stoping: {
				cmd = jderobot.CMDVelData()
				cmd.linearX = 0
				cmd.linearY = 0
				cmd.linearZ = 0
				self.lock.acquire()
				self.cmdPrx.setCMDVelData(cmd)
				self.lock.release()
				print "Stoping"
				break;
			}
			case Landing: {
				print "Landing"
				self.lock.acquire()
				self.extraPrx.land()
				self.lock.release()
				hasLanded = True
				break;
			}
			case Stabilizing2: {
				finished()
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

		// Contact to camera
		Ice::ObjectPrx camera = ic->propertyToProxy("automata.camera.Proxy");
		if (camera == 0)
			throw "Could not create proxy with camera";
		cameraprx = jderobot::CameraPrx::checkedCast(camera);
		if (cameraprx == 0)
			throw "Invalid proxy automata.camera.Proxy";
		std::cout << "camera connected" << std::endl;

		// Contact to pose3d
		Ice::ObjectPrx pose3d = ic->propertyToProxy("automata.pose3d.Proxy");
		if (pose3d == 0)
			throw "Could not create proxy with pose3d";
		pose3dprx = jderobot::Pose3DPrx::checkedCast(pose3d);
		if (pose3dprx == 0)
			throw "Invalid proxy automata.pose3d.Proxy";
		std::cout << "pose3d connected" << std::endl;

		// Contact to cmd
		Ice::ObjectPrx cmd = ic->propertyToProxy("automata.cmd.Proxy");
		if (cmd == 0)
			throw "Could not create proxy with cmd";
		cmdprx = jderobot::CMDVelPrx::checkedCast(cmd);
		if (cmdprx == 0)
			throw "Invalid proxy automata.cmd.Proxy";
		std::cout << "cmd connected" << std::endl;

		// Contact to extra
		Ice::ObjectPrx extra = ic->propertyToProxy("automata.extra.Proxy");
		if (extra == 0)
			throw "Could not create proxy with extra";
		extraprx = jderobot::ArDroneExtraPrx::checkedCast(extra);
		if (extraprx == 0)
			throw "Invalid proxy automata.extra.Proxy";
		std::cout << "extra connected" << std::endl;

		// Contact to navdata
		Ice::ObjectPrx navdata = ic->propertyToProxy("automata.navdata.Proxy");
		if (navdata == 0)
			throw "Could not create proxy with navdata";
		navdataprx = jderobot::NavdataPrx::checkedCast(navdata);
		if (navdataprx == 0)
			throw "Invalid proxy automata.navdata.Proxy";
		std::cout << "navdata connected" << std::endl;

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
