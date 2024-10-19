import os,json ,webbrowser
from dotenv import load_dotenv

load_dotenv(os.path.join("C:/Users/RISHABH/.Hooks",".env"))
FILE_NAME = "data.json"





def file():
    return f"{os.getenv('DATA_PATH')}/{FILE_NAME}"




def create_json(data):
    with open(file(),"w") as f:
        json.dump(data,f)


def add_json(values={},key="web_apps"):
    with open(file(),"r") as f:
        d = json.load(f)
        for (k,v) in values.items():
            d[key][k] = v
    create_json(d)
    
    
raw_data = {
    "web_apps":{},
    "desktop_apps":{},
    "lists":{}
}

class DataSource:
    def __init__(self):
        self.file = file()
        self.n_cat = ["web_apps","desktop_apps",]
        
        self.init()
    
    def create_json(self,data):
        with open(self.file,"w") as f:
            json.dump(data,f)
    
    def add_json(self,values={},key="web_apps"):
        if key in self.n_cat:
            d = self.read_json()
            for (k,v) in values.items():
                if k in d[key].keys():
                    return 101
                else:
                    d[key][k] =v 
                    create_json(d)
                    return 102
                    
        
        if key == "lists":
            d = self.read_json()
            for (k,v) in values.items():
                d[key][k] =  v
            create_json(d)
            
            
    
    def read_json(self):
        return json.load(open(self.file,"r"))
    
    def init(self):
        if not os.path.exists(self.file):
            self.create_json(raw_data)
            # print("File not found Created file")
        else:
            pass
            # print("File Already eXIST")
    def re_init(self):
        os.remove(self.file)
        self.init()
    
    def delete_json(self,key="web_apps",item="key"):

            
        if key in [*self.n_cat,"lists"]:
            d = self.read_json()
            if item in d[key].keys():
                d[key].pop(item)
                create_json(d)
                

            


def splitter(value):
    if ";" in value:
        value = value.split(";")
    else:
        value = value.split("\n")
    return value
    

def open_app(app_name):
    os.startfile(app_name)
    
def open_link(link_ref):
    link_ref =  link_ref.replace('\\','\\\\')
    webbrowser.open_new_tab(link_ref)
            
# src = DataSource()

# src.add_json(key="lists",values={"kaggle":["one","two"],"item2":["sample","smaple2"]})
# src.add_json(key="web_apps",values={"kaggle":"value","test":"value"})
# src.add_json(key="desktop_apps",values={"designer":"value","sample":"test"})
 


# src.re_init()

 