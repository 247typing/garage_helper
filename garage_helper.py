import tkinter as tk
import sys, inspect

#returns a list of dicts for each class in this module with attribute is_tool = True
#dicts contain "name": the exact name of the class, "obj": the object itself, "nice_name": used for labeling buttons etc.
def find_all_tools():
    #get a list of all classes in the module
    classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)

    #sort out the name of each class and its attribute of is_tool
    #returns
    tool_classes = [] #??? change to dict with class, name, and nice name ???
    for cls in classes:
        temp_obj = eval(cls[0])

        #string name of class
        print(cls[0])
        #class attribute is_tool
        print(temp_obj.is_tool)
        if temp_obj.is_tool:
            info = {
                "name" : cls[0],
                "obj" : temp_obj,
                "nice_name" : temp_obj.nice_name
            }
            tool_classes.append(info)

    print(tool_classes)
    return tool_classes

#The Control code was derived from this tutorial
#https://pythonprogramming.net/tkinter-depth-tutorial-making-actual-program/
class Control(tk.Tk):
    is_tool = False
    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)

        container.pack()

        self.frames = {}

        frame = Welcome(container, self)
        self.frames[Welcome] = frame
        #frame.pack()
        frame.grid(row=0, column=0, sticky="nsew")

        #test to add all tools
        for i in range(len(selections)):
            temp_obj = selections[i]["obj"]
            frame = temp_obj(container, self)
            self.frames[temp_obj] = frame
            #frame.pack()
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Welcome)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class Selection_Menu(tk.Frame):
    is_tool = False
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Selection_Menu Page")
        label.pack()

        #TODO set the buttons to auto allocate as many as tools
                                                                        #TODO change Test_tool to automatic from selections
        button = tk.Button(self, text=selections[0]["nice_name"], command= lambda: controller.show_frame(Test_Tool))
        button.pack()

        button1 = tk.Button(self, text=selections[1]["nice_name"], command= lambda: controller.show_frame(Test_Two))
        button1.pack()
#class Welcome(tk.Frame):
class Welcome(Selection_Menu, tk.Frame):
    is_tool = False
    def __init__(self, parent, controller):
        super().__init__(parent,controller)
        label = tk.Label(self, text="Welcome Page")
        label.pack()

class Test_Tool(Selection_Menu, tk.Frame):
    is_tool = True
    nice_name = "Test Tool"
    def __init__(self, parent, controller):
        super().__init__(parent,controller)
        label = tk.Label(self, text="Test Tool Page")
        label.pack()

class Test_Two(Selection_Menu, tk.Frame):
    is_tool = True
    nice_name = "Test Tool 2"
    def __init__(self, parent, controller):
        super().__init__(parent,controller)
        label = tk.Label(self, text="Test 2 Tool Page")
        label.pack()


selections = find_all_tools()
print(selections)
print(type(selections))

#launch the app
app = Control()
app.mainloop()
