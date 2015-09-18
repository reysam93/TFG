#ifndef AUTOMATAGUI_H
#define AUTOMATAGUI_H

#include <unistd.h>
#include <iostream>
#include <gtkmm-3.0/gtkmm.h>

#include "../visualHFSM/guisubautomata.h"


typedef enum ItemType {
	NONE,
	STATE,
	INIT,
	TEXT
} ItemType;


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
	Gtk::Button* pUpButton;
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

	ItemType type;

	//IDs for the subautomata created
	int idGuiNode, idGuiTrans;

	//Items for the creation of transition
	//Glib::RefPtr<Goocanvas::Item> lastItem, theOtherItem;

	//Glib::RefPtr<Goocanvas::Item> selectedItem;
	//Glib::RefPtr<Goocanvas::Item> textItem;

	GuiSubautomata* getSubautomataWithIdFather(int id);
	GuiSubautomata* getSubautomata(int id);
	void create_new_state(GuiNode* gnode);
	void create_new_transition(GuiTransition* gtrans);
	int getIdNodeFather(int subautomataId);
	bool fillTreeView(std::string nameNode, Gtk::TreeModel::Children child, int idNodeFather);
	GuiNode* getNodeByName(std::string name);
	void showSubautomata(int id);

	//Handlers
	void on_up_button_clicked ();
	void on_item_created(const Glib::RefPtr<Goocanvas::Item>& item, 
							const Glib::RefPtr<Goocanvas::ItemModel>& model);
	bool on_item_button_press_event(const Glib::RefPtr<Goocanvas::Item>& item,
                            GdkEventButton* event);
	bool on_item_enter_notify_event(const Glib::RefPtr<Goocanvas::Item>& item,
                                              GdkEventCrossing* event);
	bool on_item_leave_notify_event(const Glib::RefPtr<Goocanvas::Item>& item,
                                              GdkEventCrossing* event);
};

#endif // AUTOMATAGUI_H