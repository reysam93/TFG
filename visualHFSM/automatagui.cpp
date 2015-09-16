

#include "automatagui.h"

/*************************************************************
 * CONSTRUCTOR
 *************************************************************/
AutomataGui::AutomataGui(int argc, char** argv){
	this->app = Gtk::Application::create(argc, argv, "jderobot.visualHFSM.automatagui");
}

/*************************************************************
 * DESTRUCTOR
 *************************************************************/
AutomataGui::~AutomataGui(){}


int AutomataGui::init(){
	//Create the builder
	this->refBuilder = Gtk::Builder::create();
	try{
    	refBuilder->add_from_file("../visualHFSM/automatagui.glade");
	}catch (const Glib::FileError& ex){
		std::cerr << "FileError: " << ex.what() << std::endl;
	  	return -1;
	}catch (const Glib::MarkupError& ex){
	  	std::cerr << "MarkupError: " << ex.what() << std::endl;
	  	return -1;
	}catch (const Gtk::BuilderError& ex){
		std::cerr << "BuilderError: " << ex.what() << std::endl;
		return -1;
	}

	//GETTING WIDGETS
	refBuilder->get_widget("scrolledwindow_schema", this->scrolledwindow_schema);
	refBuilder->get_widget("treeview", this->treeView);
	refBuilder->get_widget("up_button", this->pUpButton);

	this->canvas = Gtk::manage(new Goocanvas::Canvas());
	this->canvas->signal_item_created().connect(sigc::mem_fun(*this,
										&AutomataGui::on_item_created));

	this->pUpButton->signal_clicked().connect(sigc::mem_fun(*this,
										&AutomataGui::on_up_button_clicked));

	this->root = Goocanvas::GroupModel::create();
	this->canvas->set_root_item_model(root);
	this->canvas->set_visible(true);
	this->scrolledwindow_schema->add(*(this->canvas));

	this->refTreeModel = Gtk::TreeStore::create(this->m_Columns);
	this->treeView->set_model(this->refTreeModel);
	this->treeView->append_column("ID", this->m_Columns.m_col_id);
	this->treeView->append_column("Name", this->m_Columns.m_col_name);

	refBuilder->get_widget("DialogDerived", guiDialog);
	if(!guiDialog){
		std::cerr << "Error: couldn't get DialogDerived" << std::endl;
		return -1;
	}
	Glib::RefPtr<Gdk::Screen> screen = this->guiDialog->get_screen();
    int width = screen->get_width();
    int height = screen->get_height();

    Goocanvas::Bounds bounds;
    this->canvas->get_bounds(bounds);
    bounds.set_x2(width);
    bounds.set_y2(height * 2);
    this->canvas->set_bounds(bounds);
    return 0;
}


void AutomataGui::run(){			
	this->app->run(*guiDialog);
  	delete guiDialog;
}


void AutomataGui::setGuiSubautomataList (std::list<GuiSubautomata> guiSubList){
	this->guiSubautomataList = guiSubList;
}


GuiSubautomata* AutomataGui::getSubautomataWithIdFather(int id){

	std::list<GuiSubautomata>::iterator subListIt = this->guiSubautomataList.begin();
	while(subListIt != this->guiSubautomataList.end()){
		if(subListIt->getIdFather() == id){
			return &*subListIt;
		}
		subListIt++;
	}
	return NULL;
}


GuiSubautomata* AutomataGui::getSubautomata(int id){
	std::list<GuiSubautomata>::iterator subListIt = this->guiSubautomataList.begin();
	while(subListIt != this->guiSubautomataList.end()){
		if(subListIt->getId() == id){
			return &*subListIt;
		}
		subListIt++;
	}
	return NULL;
}


void AutomataGui::loadGuiSubautomata(){
	std::list<GuiSubautomata>::iterator subListIterator = this->guiSubautomataList.begin();
	while (subListIterator != guiSubautomataList.end()){
		this->currentGuiSubautomata = &(*subListIterator);

		std::list<GuiNode> nodeList = *(subListIterator->getListGuiNodes());
		std::list<GuiNode>::iterator nodeListIterator = nodeList.begin();
		while (nodeListIterator != nodeList.end()){
			this->idGuiNode = nodeListIterator->getId();
			this->create_new_state(&(*nodeListIterator));
			if (nodeListIterator->itIsInitial())
				nodeListIterator->changeColor(ITEM_COLOR_GREEN);
			nodeListIterator++;
		}
		std::list<GuiTransition> transList = *(subListIterator->getListGuiTransitions());
		std::list<GuiTransition>:: iterator transListIterator = transList.begin();
		while (transListIterator != transList.end()){
			int idOrigin = transListIterator->getIdOrigin();
			int idDestiny = transListIterator->getIdDestiny();

			this->create_new_transition(&(*transListIterator));
			transListIterator++;
		}
		if (subListIterator->getIdFather() != 0)
			this->currentGuiSubautomata->hideAll();
		subListIterator++;
	}

	this->currentGuiSubautomata = this->getSubautomataWithIdFather(0);
}


void AutomataGui::create_new_state(GuiNode* gnode){
	
	std::string nodeName = gnode->getName();
	if (this->currentGuiSubautomata->getId() == 1){
		Gtk::TreeModel::Row row = *(this->refTreeModel->append());
		row[m_Columns.m_col_id] = this->idGuiNode;
		row[m_Columns.m_col_name] = nodeName;
	} else {
		this->fillTreeView(nodeName, this->refTreeModel->children(),
			this->getIdNodeFather(this->currentGuiSubautomata->getIdFather()));
	}
	this->type = STATE;
	this->root->add_child(gnode->getEllipse());

	this->type = TEXT;
	this->root->add_child(gnode->getText());

	this->type = INIT;
	this->root->add_child(gnode->getEllipseInitial());

	this->type = NONE;
}


void AutomataGui::create_new_transition(GuiTransition* gtrans){
	int originId = gtrans->getIdOrigin();
	int finalId = gtrans->getIdDestiny();

	if (originId == finalId){	//autotransition
		int transId = gtrans->getId();
		Point origin = *(this->currentGuiSubautomata->getPointPointer(originId));
		Point final = *(this->currentGuiSubautomata->getPointPointer(finalId));

		float xcenter = origin.getX();
		origin.setX(xcenter - RADIUS_NORMAL + 2);
		final.setX(xcenter + RADIUS_NORMAL -2);

		int numberAutotrans = this->currentGuiSubautomata->getNumberOfAutotransitions(origin);

		Point pmidpoint(xcenter, origin.getY() + (2 + 3 * numberAutotrans) * RADIUS_NORMAL);

		GuiTransition transAux(origin, final, pmidpoint, transId);
		this->currentGuiSubautomata->replaceGuiTransition(transAux, transId);

		gtrans = &transAux;
	}
	this->root->add_child(gtrans->getLeftLine());
	this->root->add_child(gtrans->getRightLine());
	this->root->add_child(gtrans->getTextModel());
	this->root->add_child(gtrans->getMidpoint());
}


int AutomataGui::getIdNodeFather ( int subautomataId ) {
    std::list<GuiSubautomata>::iterator subListIterator = this->guiSubautomataList.begin();
    while ( (subListIterator->getId() != subautomataId) &&
            (subListIterator != this->guiSubautomataList.end()) )
    	subListIterator++;
        
    if (subListIterator == this->guiSubautomataList.end())
		return 0;

    std::list<GuiNode>* guiNodeList = subListIterator->getListGuiNodes();
    std::list<GuiNode>::iterator guiNodeListIterator = guiNodeList->begin();
    while ( (guiNodeListIterator->getIdSubautomataSon() != this->currentGuiSubautomata->getId()) 
    		&& (guiNodeListIterator != guiNodeList->end()) )
   		guiNodeListIterator++;

    if (guiNodeListIterator == guiNodeList->end()){
		return 0;
	}else{
		return guiNodeListIterator->getId();
	}
}

bool AutomataGui::fillTreeView ( std::string nameNode, Gtk::TreeModel::Children child, int idNodeFather ) {
    bool cont = true;
    Gtk::TreeModel::Children::iterator iter = child.begin();
    while ( cont && (iter != child.end()) ) {
        Gtk::TreeModel::Row therow = *iter;
        if (therow[m_Columns.m_col_id] == idNodeFather) {
            Gtk::TreeModel::Row row = *(refTreeModel->append(therow.children()));
            row[m_Columns.m_col_id] = this->idGuiNode;
            row[m_Columns.m_col_name] = nameNode;
            cont = false;
        } else {
            cont = this->fillTreeView(nameNode, therow.children(), idNodeFather);
            iter++;
        }
    }
    return cont;
}


int AutomataGui::setNodeAsActive(std::string nodeName){
	/*if (this->activeNode != NULL){
 		this->activeNode->changeColor(ITEM_COLOR_BLUE);
 	}
	this->activeNode = this->getNodeByName(nodeName);
	if (this->activeNode == NULL)
 		return -1;
 	this->activeNode->changeColor(ITEM_COLOR_GREEN);
 	return 0;*/
}


GuiNode* AutomataGui::getNodeByName(std::string name){
	//std::list<GuiNode> nodeList = ;
	std::list<GuiNode>::iterator nodeListIter = this->currentGuiSubautomata->getListGuiNodes()->begin();
	while (nodeListIter != this->currentGuiSubautomata->getListGuiNodes()->end()){
		if (nodeListIter->getName().compare(name) == 0){
			return &(*nodeListIter);
		}
		nodeListIter++;
	}
	return NULL;
}


 int AutomataGui::setNodeAsActive(std::string nodeName, bool active){
 	GuiNode* node = this->getNodeByName(nodeName);
 	if (node == NULL)
 		return -1;
 	if (active){
 		node->changeColor(ITEM_COLOR_GREEN);
 	}else{
 		node->changeColor(ITEM_COLOR_BLUE);
 	}
 	return 0;
 }


 void AutomataGui::on_item_created(const Glib::RefPtr<Goocanvas::Item>& item,
                                   const Glib::RefPtr<Goocanvas::ItemModel>& /* model */){

 	if (this->type == STATE){
 		item->signal_button_press_event().connect(
 			sigc::mem_fun(this, &AutomataGui::on_item_button_press_event));
 		this->selectedItem = item;
 	} else if (this->type == TEXT){
 		this->textItem = item;
 	} else if (this->type == INIT){
 		this->currentGuiSubautomata->setGuiNodeItems(this->idGuiNode, this->selectedItem, 
 														item, this->textItem);
 	}
}


void AutomataGui::showSubautomata(int id){
	this->currentGuiSubautomata->hideAll();
	this->currentGuiSubautomata = this->getSubautomata(id);
	this->currentGuiSubautomata->showAll();
}


bool AutomataGui::on_item_button_press_event(const Glib::RefPtr<Goocanvas::Item>& item,
                                              GdkEventButton* event ){

	if ((event->button == 1) && item){
		if (event->type == GDK_2BUTTON_PRESS){
			int idSubautomataSon = this->currentGuiSubautomata->getIdSubautomataSon(item);
			if (idSubautomataSon != 0){
				this->showSubautomata(idSubautomataSon);
			}else{
				std::cout << "This node doesn't have any son." << std::endl;
			}
		}
		return true;
	}

	return false;
}


void AutomataGui::on_up_button_clicked (){

	int fatherId = this->currentGuiSubautomata->getIdFather();
	if (fatherId != 0){
		this->showSubautomata(fatherId);
	} else {
		std::cout << "This subautomata doesn't have any parent." << std::endl;
	}
	
}