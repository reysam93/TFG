#include <Ice/Ice.h>
#include <IceUtil/IceUtil.h>
#include <jderobot/visualHFSM/automatagui.h>

#include <numpy>
#include <cv2>
#include <jderobot>

#include <jderobot/ardroneextra.h>
#include <jderobot/cmdvel.h>
#include <jderobot/pose3d.h>
#include <jderobot/camera.h>

typedef enum State_Sub_1 {
	TakeOff,
	FollowRoad,
	MonitorArea,
	TurnAround,
	Landing,
} State_Sub_1;

const char* Names_Sub_1[] = {
	"TakeOff",
	"FollowRoad",
	"MonitorArea",
	"TurnAround",
	"Landing",
};

typedef enum State_Sub_3 {
	FindRoad,
	FindRoad_ghost,
	FollowingRoad,
	FollowingRoad_ghost,
} State_Sub_3;

const char* Names_Sub_3[] = {
	"FindRoad",
	"FindRoad_ghost",
	"FollowingRoad",
	"FollowingRoad_ghost",
};

typedef enum State_Sub_5 {
	ToFirstPos,
	ToFirstPos_ghost,
	ToSecondPos,
	ToSecondPos_ghost,
	ToThirdPos,
	ToThirdPos_ghost,
	Return,
	Return_ghost,
} State_Sub_5;

const char* Names_Sub_5[] = {
	"ToFirstPos",
	"ToFirstPos_ghost",
	"ToSecondPos",
	"ToSecondPos_ghost",
	"ToThirdPos",
	"ToThirdPos_ghost",
	"Return",
	"Return_ghost",
};

pthread_t thr_sub_1;
pthread_t thr_sub_3;
pthread_t thr_sub_5;
pthread_t thr_automatagui;

AutomataGui *automatagui;
bool displayGui = false;

bool run1 = true;
bool run3 = true;
bool run5 = true;

State_Sub_1 sub_1 = TakeOff;
State_Sub_3 sub_3 = FindRoad_ghost;
State_Sub_5 sub_5 = ToFirstPos_ghost;

jderobot::ArDroneExtraPrx Extraprx;
jderobot::CMDVelPrx CMDVelprx;
jderobot::Pose3DPrx Pose3Dprx;
jderobot::CameraPrx Cameraprx;

void shutDown(){
	run1 = false;
	run3 = false;
	run5 = false;
	automatagui->close();
}

def getImage(self):
	img = self.CameraPrx.getImageData("RGB8")
	height = img.description.height
	width=img.description.width
	imgPixels = numpy.zeros((height, width, 3), numpy.uint8)
	imgPixels = numpy.frombuffer(img.pixelData, dtype=numpy.uint8)
	imgPixels.shape = height, width, 3
	return imgPixels

def setVelocity(self, vx, vy, vz, yaw):
	cmd = jderobot.CMDVelData()
	cmd.linearX = vy
	cmd.linearY = vx
	cmd.linearZ = vz
	cmd.angularZ = yaw
	cmd.angularX = cmd.angularY = 1.0
	self.CMDVelPrx.setCMDVelData(cmd)

#The factor indicate the margin of the error multipliyin the error for this factor
def droneInPosition(self, pos,factor=1 ):
	return (abs(pos[0] - self.xPos) < self.minDist*factor) and (abs(pos[1] - self.yPos) < self.minDist*factor)

class PID:
	def __init__(self, Epsilon=.01, Kp=1, Ki=1, Kd=1, Imax=300, Imin=-300):
		self.Ep = Epsilon
		self.Kp = Kp
		self.Ki = Ki
		self.Kd = Kd

		self.Imax = Imax
		self.Imin = Imin
		self.lastError = 0
		self.cumulativeError = 0

	def updateCumulativeError(self, error):
		self.cumulativeError += error
		if self.cumulativeError > self.Imax:
			self.cumulativeError = self.Imax
		elif self.cumulativeError < self.Imin:
			self.cumulativeError = self.Imin

	def process(self, error, derivative=None, integral=None):
		if -self.Ep < error < self.Ep:
			return 0, 0, 0

		P = self.Kp * error
		self.updateCumulativeError(error)
		if integral != None:
			I = self.Ki * integral
		else:
			I = self.Ki * self.cumulativeError

		if derivative != None:
			D = self.Kd * derivative
		else:
			D = self.Kd * (error - self.lastError)
		self.lastError = error

		return P, I, D





std::list<GuiSubautomata> createGuiSubAutomataList(){
	std::list<GuiSubautomata> guiSubautomataList;

	GuiSubautomata* guiSubautomata1 = new GuiSubautomata(1, 0);

	guiSubautomata1->newGuiNode(1, 0, 75, 119);
	guiSubautomata1->setIsInitialLastGuiNode(1);
	guiSubautomata1->setNameLastGuiNode("TakeOff");

	guiSubautomata1->newGuiNode(2, 3, 322, 112);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("FollowRoad");

	guiSubautomata1->newGuiNode(6, 5, 514, 303);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("MonitorArea");

	guiSubautomata1->newGuiNode(11, 0, 340, 438);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("TurnAround");

	guiSubautomata1->newGuiNode(12, 0, 531, 51);
	guiSubautomata1->setIsInitialLastGuiNode(0);
	guiSubautomata1->setNameLastGuiNode("Landing");

	Point* origin17 = new Point(322, 112);
	Point* destiny17 = new Point(514, 303);
	Point* midPoint17 = new Point(443, 156);
	guiSubautomata1->newGuiTransition(*origin17, *destiny17, *midPoint17, 7, 2, 6);

	Point* origin113 = new Point(514, 303);
	Point* destiny113 = new Point(340, 438);
	Point* midPoint113 = new Point(443, 364);
	guiSubautomata1->newGuiTransition(*origin113, *destiny113, *midPoint113, 13, 6, 11);

	Point* origin114 = new Point(340, 438);
	Point* destiny114 = new Point(322, 112);
	Point* midPoint114 = new Point(182, 278);
	guiSubautomata1->newGuiTransition(*origin114, *destiny114, *midPoint114, 14, 11, 2);

	Point* origin118 = new Point(75, 119);
	Point* destiny118 = new Point(322, 112);
	Point* midPoint118 = new Point(199, 116);
	guiSubautomata1->newGuiTransition(*origin118, *destiny118, *midPoint118, 18, 1, 2);

	Point* origin119 = new Point(322, 112);
	Point* destiny119 = new Point(531, 51);
	Point* midPoint119 = new Point(426, 81);
	guiSubautomata1->newGuiTransition(*origin119, *destiny119, *midPoint119, 19, 2, 12);

	guiSubautomataList.push_back(*guiSubautomata1);

	GuiSubautomata* guiSubautomata3 = new GuiSubautomata(3, 1);

	guiSubautomata3->newGuiNode(3, 0, 156, 228);
	guiSubautomata3->setIsInitialLastGuiNode(1);
	guiSubautomata3->setNameLastGuiNode("FindRoad");

	guiSubautomata3->newGuiNode(4, 0, 427, 255);
	guiSubautomata3->setIsInitialLastGuiNode(0);
	guiSubautomata3->setNameLastGuiNode("FollowingRoad");

	Point* origin32 = new Point(156, 228);
	Point* destiny32 = new Point(427, 255);
	Point* midPoint32 = new Point(297, 157);
	guiSubautomata3->newGuiTransition(*origin32, *destiny32, *midPoint32, 2, 3, 4);

	Point* origin33 = new Point(427, 255);
	Point* destiny33 = new Point(156, 228);
	Point* midPoint33 = new Point(265, 320);
	guiSubautomata3->newGuiTransition(*origin33, *destiny33, *midPoint33, 3, 4, 3);

	guiSubautomataList.push_back(*guiSubautomata3);

	GuiSubautomata* guiSubautomata5 = new GuiSubautomata(5, 1);

	guiSubautomata5->newGuiNode(7, 0, 86, 275);
	guiSubautomata5->setIsInitialLastGuiNode(1);
	guiSubautomata5->setNameLastGuiNode("ToFirstPos");

	guiSubautomata5->newGuiNode(8, 0, 247, 92);
	guiSubautomata5->setIsInitialLastGuiNode(0);
	guiSubautomata5->setNameLastGuiNode("ToSecondPos");

	guiSubautomata5->newGuiNode(9, 0, 491, 303);
	guiSubautomata5->setIsInitialLastGuiNode(0);
	guiSubautomata5->setNameLastGuiNode("ToThirdPos");

	guiSubautomata5->newGuiNode(10, 0, 281, 455);
	guiSubautomata5->setIsInitialLastGuiNode(0);
	guiSubautomata5->setNameLastGuiNode("Return");

	Point* origin59 = new Point(86, 275);
	Point* destiny59 = new Point(247, 92);
	Point* midPoint59 = new Point(166, 184);
	guiSubautomata5->newGuiTransition(*origin59, *destiny59, *midPoint59, 9, 7, 8);

	Point* origin510 = new Point(247, 92);
	Point* destiny510 = new Point(491, 303);
	Point* midPoint510 = new Point(369, 198);
	guiSubautomata5->newGuiTransition(*origin510, *destiny510, *midPoint510, 10, 8, 9);

	Point* origin511 = new Point(491, 303);
	Point* destiny511 = new Point(281, 455);
	Point* midPoint511 = new Point(386, 379);
	guiSubautomata5->newGuiTransition(*origin511, *destiny511, *midPoint511, 11, 9, 10);

	Point* origin512 = new Point(281, 455);
	Point* destiny512 = new Point(86, 275);
	Point* midPoint512 = new Point(184, 365);
	guiSubautomata5->newGuiTransition(*origin512, *destiny512, *midPoint512, 12, 10, 7);

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

	self.targetX = 125
	self.targetY = 125
	self.targetZ = 2.5
	self.initPos = (-1, -8.5)
	
	#Minimun errors
	self.minError = 10
	self.minActit = 0.5
	self.minAltit = 0.01
	self.minDist = 0.01
	
	#Control Variables
	self.heigh = 0
	self.contours = []
	self.monitorComplet = False
	self.xPos = self.Pose3DPrx.getPose3DData().x
	self.yPos = self.Pose3DPrx.getPose3DData().y
	initAngle = None
	
	#Filter Values
	self.hmin = 90
	self.hmax = 97
	self.vmin = 0
	self.vmax = 50
	self.smin = 45
	self.smax = 80
	
	#Control PID
	self.xPid = PID(Epsilon=self.minError, Kp=0.01, Ki=0.01, Kd=0.003, Imax=5, Imin=-5)
	self.zPid = PID(Epsilon=self.minAltit, Kp=1.00, Ki=0, Kd=0, Imax=5, Imin=-5)
	self.aPid = PID(Epsilon=self.minActit, Kp=0.02, Ki=0.02, Kd=0.003, Imax=5, Imin=-5)

	while (run1) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		// Evaluation switch
		switch (sub_1) {
			case TakeOff: {
				if (abs(self.targetZ - self.heigh) < self.minAltit) {
					sub_1 = FollowRoad;
					if(displayGui){
						automatagui->notifySetNodeAsActive("FollowRoad");
					}
				}

				break;
			}
			case FollowRoad: {
				if ((self.droneInPosition(self.initPos, 200)) and (not self.monitorComplet)) {
					sub_1 = MonitorArea;
					if(displayGui){
						automatagui->notifySetNodeAsActive("MonitorArea");
					}
				}

				if ((self.monitorComplet)) {
					sub_1 = Landing;
						self.setVelocity(0,0,0,0)
					if(displayGui){
						automatagui->notifySetNodeAsActive("Landing");
					}
				}

				break;
			}
			case MonitorArea: {
				if (self.monitorComplet) {
					sub_1 = TurnAround;
						self.setVelocity(0, 0, 0, 0)
					if(displayGui){
						automatagui->notifySetNodeAsActive("TurnAround");
					}
				}

				break;
			}
			case TurnAround: {
				if (!t_activated) {
					t_ini = time(NULL);
					t_activated = true;
				} else {
					t_fin = time(NULL);
					secs = difftime(t_fin, t_ini);
					if (secs > (double) 2.5) {
						sub_1 = FollowRoad;
						t_activated = false;
						if (displayGui){
							automatagui->notifySetNodeAsActive("FollowRoad");
						}
					}
				}

				break;
			}
			case Landing: {
				break;
			}
		}

		// Actuation switch
		switch (sub_1) {
			case TakeOff: {
				#Taking Off
				self.ExtraPrx.takeoff()
				
				#Controling heigh
				self.heigh = self.Pose3DPrx.getPose3DData().z
				zp, zi, zd = self.zPid.process(self.targetZ - self.heigh)
				zVel = zp + zi + zd
				self.setVelocity(0, 0, zVel, 0)
				print "Heigh:", self.heigh
				break;
			}
			case FollowRoad: {
				lastState = "FollowRoad"
				
				#Get and prepare image
				inImg = self.getImage()
				softenedImg = cv2.bilateralFilter(inImg, 9, 75, 75)
				hsvImg = cv2.cvtColor(softenedImg, cv2.COLOR_BGR2HSV)
				
				#Get threshold image
				minValues = numpy.array([self.hmin, self.vmin, self.smin])
				maxValues = numpy.array([self.hmax, self.vmax, self.smax])
				thresholdImg = cv2.inRange(hsvImg, minValues, maxValues)
				
				#Get contours
				self.contours, hierarchy = cv2.findContours(thresholdImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
				
				#Update Heigh
				self.heigh = self.Pose3DPrx.getPose3DData().z
				break;
			}
			case MonitorArea: {
				break;
			}
			case TurnAround: {
				self.setVelocity(0, 0, 0, 1)
				pose= self.Pose3DPrx.getPose3DData()
				print "q0", pose.q0, "q1",pose.q1, "q2",pose.q2, "q3",pose.q3
				break;
			}
			case Landing: {
				print "PENDING"
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


	while (run3) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		if (sub_1 == FollowRoad) {
			if ( sub_3 == FindRoad_ghost || sub_3 == FollowingRoad_ghost) {
				sub_3 = (State_Sub_3)(sub_3 - 1);
				t_ini = time(NULL);
			}
		// Evaluation switch
		switch (sub_3) {
			case FindRoad: {
				if (self.contours) {
					sub_3 = FollowingRoad;
					if(displayGui){
						automatagui->notifySetNodeAsActive("FollowingRoad");
					}
				}

				break;
			}
			case FollowingRoad: {
				if (not self.contours) {
					sub_3 = FindRoad;
					if(displayGui){
						automatagui->notifySetNodeAsActive("FindRoad");
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_3) {
			case FindRoad: {
				self.setVelocity(0, 0, 0.75, 0)
				print "Road lost"
				break;
			}
			case FollowingRoad: {
				contour = max(self.contours, key=cv2.contourArea)
				try:
					(x, y), radius = cv2.minEnclosingCircle(contour)
					center = (int(x), int(y))
					ellipse = cv2.fitEllipse(contour)
					inclination = ellipse[2]
				
					if inclination < 90:
						yAngle = -inclination
					else:
						yAngle = 180 - inclination
				
					ap, ai, ad = self.aPid.process(yAngle)
					xError = self.targetX - center[0]
					xp, xi, xd = self.xPid.process(xError)
					speed = max((self.targetX - pow(1.09, abs(xError)))/125.,0)
				
					xvel = xp + xi +xd
					avel = ap + ai + ad
					
					self.setVelocity(xvel, speed, 0, avel)
				except:
					print "EXCEPTION FOUND"
					self.contours = []
				
				self.xPos = self.Pose3DPrx.getPose3DData().x
				self.yPos = self.Pose3DPrx.getPose3DData().y
				print "Xpos:", self.xPos, "Ypos:", self.yPos
				break;
			}
		}
		} else {
			switch (sub_3) {
				case FindRoad:
					sub_3 = (State_Sub_3)(sub_3 + 1);
					break;
				case FollowingRoad:
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

void* subautomata_5 ( void* ) {
	struct timeval a, b;
	int cycle = 100;
	long totala, totalb;
	long diff;
	time_t t_ini;
	time_t t_fin;
	double secs;
	bool t_activated;

	firstPos = (10, -20)
	secondPos = (5, -30)
	thirdPos = (-10, -20)
	
	#Control PID
	xDistPid = PID(Epsilon=self.minDist, Kp=0.8, Ki=0.0, Kd=0.0, Imax=5, Imin=-5)
	yDistPid = PID(Epsilon=self.minDist, Kp=0.8, Ki=0.0, Kd=0.0, Imax=5, Imin=-5)

	while (run5) {
		gettimeofday(&a, NULL);
		totala = a.tv_sec * 1000000 + a.tv_usec;

		if (sub_1 == MonitorArea) {
			if ( sub_5 == ToFirstPos_ghost || sub_5 == ToSecondPos_ghost || sub_5 == ToThirdPos_ghost || sub_5 == Return_ghost) {
				sub_5 = (State_Sub_5)(sub_5 - 1);
				t_ini = time(NULL);
			}
		// Evaluation switch
		switch (sub_5) {
			case ToFirstPos: {
				if (self.droneInPosition(firstPos)) {
					sub_5 = ToSecondPos;
					if(displayGui){
						automatagui->notifySetNodeAsActive("ToSecondPos");
					}
				}

				break;
			}
			case ToSecondPos: {
				if (self.droneInPosition(secondPos)) {
					sub_5 = ToThirdPos;
					if(displayGui){
						automatagui->notifySetNodeAsActive("ToThirdPos");
					}
				}

				break;
			}
			case ToThirdPos: {
				if (self.droneInPosition(thirdPos)) {
					sub_5 = Return;
					if(displayGui){
						automatagui->notifySetNodeAsActive("Return");
					}
				}

				break;
			}
			case Return: {
				if (self.droneInPosition(self.initPos)) {
					sub_5 = ToFirstPos;
						self.monitorComplet = True
					if(displayGui){
						automatagui->notifySetNodeAsActive("ToFirstPos");
					}
				}

				break;
			}
		}

		// Actuation switch
		switch (sub_5) {
			case ToFirstPos: {
				self.xPos = self.Pose3DPrx.getPose3DData().x
				self.yPos = self.Pose3DPrx.getPose3DData().y
				
				xError = firstPos[0] - self.xPos
				xp, xi, xd = xDistPid.process(xError)
				yError = firstPos[1] - self.yPos
				yp, yi, yd = yDistPid.process(yError)
				print "Xerror:", xError, "Yerror:", yError
				
				xVel = xp + xi + xd
				yVel = yp + yi +yd
				print "Xvel:", xVel, "Yvel:", -yVel
				
				self.setVelocity(xVel, -yVel, 0, 0)
				break;
			}
			case ToSecondPos: {
				self.xPos = self.Pose3DPrx.getPose3DData().x
				self.yPos = self.Pose3DPrx.getPose3DData().y
				
				xError = secondPos[0] - self.xPos
				xp, xi, xd = xDistPid.process(xError)
				yError = secondPos[1] - self.yPos
				yp, yi, yd = yDistPid.process(yError)
				print "xError:",xError, "Yerror:", yError
				
				xVel = xp + xi + xd
				yVel = yp + yi +yd
				print "Xvel:", xVel, "Yvel:", -yVel
				
				self.setVelocity(xVel, -yVel, 0, 0)
				break;
			}
			case ToThirdPos: {
				self.xPos = self.Pose3DPrx.getPose3DData().x
				self.yPos = self.Pose3DPrx.getPose3DData().y
				
				xError = thirdPos[0] - self.xPos
				xp, xi, xd = xDistPid.process(xError)
				yError = thirdPos[1] - self.yPos
				yp, yi, yd = yDistPid.process(yError)
				print "Xerror:", xError, "Yerror:", yError
				
				xVel = xp + xi + xd
				yVel = yp + yi +yd
				print "Xvel:", xVel, "Yvel:", yVel
				print "Xvel:", xVel, "Yvel:", -yVel
				
				self.setVelocity(xVel, -yVel, 0, 0)
				break;
			}
			case Return: {
				self.xPos = self.Pose3DPrx.getPose3DData().x
				self.yPos = self.Pose3DPrx.getPose3DData().y
				
				xError = self.initPos[0] - self.xPos
				xp, xi, xd = xDistPid.process(xError)
				yError = self.initPos[1] - self.yPos
				yp, yi, yd = yDistPid.process(yError)
				print "Xerror:", xError, "Yerror:", yError
				
				xVel = xp + xi + xd
				yVel = yp + yi +yd
				print "Xvel:", xVel, "Yvel:", -yVel
				
				self.setVelocity(xVel, -yVel, 0, 0)
				break;
			}
		}
		} else {
			switch (sub_5) {
				case ToFirstPos:
					sub_5 = (State_Sub_5)(sub_5 + 1);
					break;
				case ToSecondPos:
					sub_5 = (State_Sub_5)(sub_5 + 1);
					break;
				case ToThirdPos:
					sub_5 = (State_Sub_5)(sub_5 + 1);
					break;
				case Return:
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


		// Contact to Extra
		Ice::ObjectPrx Extra = ic->propertyToProxy("automata.Extra.Proxy");
		if (Extra == 0)
			throw "Could not create proxy with Extra";
		Extraprx = jderobot::ArDroneExtraPrx::checkedCast(Extra);
		if (Extraprx == 0)
			throw "Invalid proxy automata.Extra.Proxy";
		std::cout << "Extra connected" << std::endl;

		// Contact to CMDVel
		Ice::ObjectPrx CMDVel = ic->propertyToProxy("automata.CMDVel.Proxy");
		if (CMDVel == 0)
			throw "Could not create proxy with CMDVel";
		CMDVelprx = jderobot::CMDVelPrx::checkedCast(CMDVel);
		if (CMDVelprx == 0)
			throw "Invalid proxy automata.CMDVel.Proxy";
		std::cout << "CMDVel connected" << std::endl;

		// Contact to Pose3D
		Ice::ObjectPrx Pose3D = ic->propertyToProxy("automata.Pose3D.Proxy");
		if (Pose3D == 0)
			throw "Could not create proxy with Pose3D";
		Pose3Dprx = jderobot::Pose3DPrx::checkedCast(Pose3D);
		if (Pose3Dprx == 0)
			throw "Invalid proxy automata.Pose3D.Proxy";
		std::cout << "Pose3D connected" << std::endl;

		// Contact to Camera
		Ice::ObjectPrx Camera = ic->propertyToProxy("automata.Camera.Proxy");
		if (Camera == 0)
			throw "Could not create proxy with Camera";
		Cameraprx = jderobot::CameraPrx::checkedCast(Camera);
		if (Cameraprx == 0)
			throw "Invalid proxy automata.Camera.Proxy";
		std::cout << "Camera connected" << std::endl;

		if (displayGui){
			automatagui = new AutomataGui(argc, argv);
			displayGui = showAutomataGui();
		}

		pthread_create(&thr_sub_1, NULL, &subautomata_1, NULL);
		pthread_create(&thr_sub_3, NULL, &subautomata_3, NULL);
		pthread_create(&thr_sub_5, NULL, &subautomata_5, NULL);

		pthread_join(thr_sub_1, NULL);
		pthread_join(thr_sub_3, NULL);
		pthread_join(thr_sub_5, NULL);
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
