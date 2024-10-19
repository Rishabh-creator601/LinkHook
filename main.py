
from PyQt5.QtWidgets import QMainWindow, QApplication,QListWidget,QFileDialog,QScrollBar
from PyQt5.uic import loadUi
from PyQt5.QtCore import QEvent,Qt
from PyQt5.QtGui import QIcon
import sys,os,dotenv
from dotenv import load_dotenv
from file_tools import DataSource,splitter,open_app,open_link


ENV_PATH = os.path.join("C:/Users/RISHABH/.Hooks",".env")
load_dotenv(ENV_PATH)
def assets(script="Hook.ui"):
    return os.path.join(os.getenv("ASSETS_PATH"),script)



src = DataSource()





class AddApp(QMainWindow):
    def __init__(self,parent=None,ui=None):
        super(AddApp,self).__init__(parent)
        loadUi(ui,self)
        
        self.setWindowTitle("+Add")
        
        
class ListView(QMainWindow):
    def __init__(self,parent=None,ui=None):
        super(ListView,self).__init__(parent)
        loadUi(ui,self)
        
        self.setWindowTitle("ListView")



class Main(QMainWindow):
    def __init__(self):
        super(Main,self).__init__()
        loadUi(assets(),self)
        
        
        ## Default parameters and Initializers 
        
        
        self.setWindowTitle("LinkHook")
        self.setWindowIcon(QIcon(assets("logo.jpg")))
        self.tabs.setCurrentIndex(0)
        self.flag = None
        self.lists_objs = {self.web_list:"web_apps",self.desktop_list:"desktop_apps",self.lists_list:"lists"}
        self.lists_funcs = {self.web_list:open_link,self.desktop_list:open_app,self.lists_list:self.list_open}
        
        
        
        ##Menu Bar actions
        
        self.add_desktop.triggered.connect(lambda : self.add_init("Desktop App Name","Add Desktop App","desktop_apps"))
        self.add_web.triggered.connect(lambda : self.add_init("Web App Name","Add Web App","web_apps"))
        self.add_list.triggered.connect(lambda : self.add_init("List Name","Add List","lists"))
        
        
        ## New window  : AddApp
        self.add_new = AddApp(self,assets("add_ui.ui"))
        self.add_new.addBtn.clicked.connect(lambda : self.add_things(lists=True))
        self.add_new.refText.installEventFilter(self)
        
        
        ## New Window : ListView 
        self.list_view = ListView(self,assets("list_ui.ui"))
        scroll_bar = QScrollBar(self)
        self.list_view.topic_list.setHorizontalScrollBar(scroll_bar)
        
        ## Three lists connecting to their functions
        for (k,v) in self.lists_objs.items():
            k.addItems(list(src.read_json()[v].keys()))
            k.installEventFilter(self)
        
        
        ## Settings 
        self.assets_path.setText(os.getenv("ASSETS_PATH"))
        self.defBtn.clicked.connect(self.reset_path)
        self.browse_assets.clicked.connect(self.get_path)
        
        
        
        
        QApplication.instance().focusChanged.connect(self.on_focusChanged)
        
    
    def reset_path(self):
        self.assets_path.setText(os.getenv("DEFAULT_ASSETS_PATH"))
        dotenv.set_key(ENV_PATH,"ASSETS_PATH",os.getenv("DEFAULT_ASSETS_PATH"))
    
    def get_path(self):
        path_name = QFileDialog.getExistingDirectory(self,"Select Assest path")
        self.assets_path.setText(path_name)
        dotenv.set_key(ENV_PATH,"ASSETS_PATH",path_name)


    
    def add_init(self,headerText,btnText,flagSet):
        self.add_new.refText.setText("")
        self.add_new.header1.setText(headerText)
        self.add_new.addBtn.setText(btnText)
        self.add_new.show()
        self.flag =flagSet
        
        
        
    # Function to show respective values when clicked on particular Item 
    
    def on_focusChanged(self):
        listItem  = QApplication.focusWidget()
        
        if listItem in self.lists_objs.keys():
            list_obj = self.findChild(QListWidget,listItem.objectName())
            values = src.read_json()[self.lists_objs[list_obj]]
            if self.lists_objs[list_obj] == "lists":
                perform_func = lambda : self.path_header.setText(f"=> {list_obj.currentItem().text()} Contains  {str(len(values[list_obj.currentItem().text()]))} Values")
                list_obj.itemClicked.connect(perform_func)
            else:
                perform_func = lambda : self.path_header.setText(values[list_obj.currentItem().text()])
                list_obj.itemClicked.connect(perform_func)
                

    
    
    def setRef(self,value):
        self.add_new.refText.setText(value)
        
    
    def add_things(self,lists=True):
        
        if self.add_new.appName != "" and self.add_new.refText !="":
            if self.flag in ["desktop_apps","web_apps"]:
                self.add_helper(split=False)
                        
            if self.flag == "lists":
                if lists==True:
                  self.add_helper(split=True)
                else:
                    pass
    
    def add_helper(self,split=True):
        
        appName = self.add_new.appName.text()
        ref  = self.add_new.refText.toPlainText()
        ref = splitter(ref) if split==True else ref
        code = src.add_json(key=self.flag,values={appName:ref})
        self.setRef("Value Already exists") if code==101 else self.setRef("Value Added")
        
                    
                    
    ## All the events like 'enter' and 'delete'
    def eventFilter(self,obj,event):
        if event.type() == QEvent.KeyPress and obj is self.add_new.refText:
            if event.key() == Qt.Key_Return:
                self.add_things(lists=False)
        
        if event.type() == QEvent.KeyPress and obj in self.lists_objs.keys():
            if event.key() == Qt.Key_Delete:
                item=obj.selectedItems()[0]
                text_item = item.text()
                obj.takeItem(obj.row(item))
                src.delete_json(key=self.lists_objs[obj],item=text_item)
                obj.addItem("Item Deleted")
                
            if event.key() == Qt.Key_Return: 
                text = obj.selectedItems()[0].text()
                ref = src.read_json()[self.lists_objs[obj]][text]
                self.lists_funcs[obj](text,ref) if obj==self.lists_list else self.lists_funcs[obj](ref)

        return super().eventFilter(obj, event)
    
    
    def list_open(self,text,ref):
        
        
        
        self.list_view.listItem.setText(text)
        self.list_view.topic_list.clear()
        self.list_view.topic_list.addItems(ref)
        self.list_view.show()
    
            
            
            









app = QApplication(sys.argv)
ui = Main()

ui.show()
app.exec_()