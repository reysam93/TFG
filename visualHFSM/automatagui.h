#ifndef AUTOMATAGUI_H
#define AUTOMATAGUI_H

#include <unistd.h>
#include <iostream>
#include <gtkmm-3.0/gtkmm.h>

#include "../visualHFSM/guisubautomata.h"


//Class definition
class AutomataGui {
public:

	AutomataGui(int argc, char** argv);

	virtual ~AutomataGui();

	int init();
	void setGuiSubautomataList(std::list<GuiSubautomata> guiSubList);
	void loadGuiSubautomata();
	void run();
	int setNodeAsActive(std::string nodeName);
	int setNodeAsActive(std::string nodeName, bool active);

private:
	Glib::RefPtr<Gtk::Builder> refBuilder;
	Gtk::Dialog *guiDialog;
	Glib::RefPtr<Gtk::Application> app;

	//Main window
	Goocanvas::Canvas* canvas;
	Gtk::ScrolledWindow* scrolledwindow_schema;

	Glib::RefPtr<Goocanvas::ItemModel> root;

	class ModelColumns : public Gtk::TreeModel::ColumnRecord{
	public:
		ModelColumns () {
			add(m_col_id);
			add(m_col_name);
		}

		Gtk::TreeModelColumn<int> m_col_id;
		Gtk::TreeModelColumn<Glib::ustring> m_col_name;
	};
	ModelColumns m_Columns;

	Gtk::TreeView* treeView;
	Glib::RefPtr<Gtk::TreeStore> refTreeModel;

	std::list<GuiSubautomata> guiSubautomataList;
	GuiSubautomata* currentGuiSubautomata;

	GuiNode* activeNode;

	//where the mouse is
	float event_x, event_y;

	//IDs for the subautomata created
	int idGuiNode, idGuiTrans;

	//Items for the creation of transition
	Glib::RefPtr<Goocanvas::Item> lastItem, theOtherItem;

	void create_new_state(GuiNode* gnode);
	void create_new_transition(GuiTransition* gtrans);
	int getIdNodeFather(int subautomataId);
	bool fillTreeView(std::string nameNode, Gtk::TreeModel::Children child, int idNodeFather);
	GuiNode* getNodeByName(std::string name);
};

#endif // AUTOMATAGUI_H