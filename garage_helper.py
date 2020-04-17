import tkinter as tk
import sys, inspect

#returns int max_tool_width, int max_tool height, and a list of dicts for each class in this module with attribute is_tool = True
#dicts contain "name": the exact name of the class, "obj": the object itself, "nice_name": used for labeling buttons etc.
def find_all_tools():
    #get a list of all classes in the module
    classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)

    #sort out the name of each class and its attribute of is_tool
    tool_classes = []
    max_tool_width = 0
    max_tool_height = 0
    for cls in classes:
        temp_obj = eval(cls[0])

        if temp_obj.is_tool:
            info = {
                "name" : cls[0],
                "obj" : temp_obj,
                "nice_name" : temp_obj.nice_name
            }
            tool_classes.append(info)

            #find largest width
            if temp_obj.tool_width > max_tool_width:
                max_tool_width = temp_obj.tool_width

            #find largest height
            if temp_obj.tool_height > max_tool_height:
                max_tool_height = temp_obj.tool_height

    print("max tool width: " + str(max_tool_width))
    return max_tool_width, max_tool_height, tool_classes

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

#######################################
#should make this its own frame so the buttons are not tied to the rows/cols of tools
###################################################################
class Selection_Menu(tk.Frame):
    is_tool = False
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)


        #create a button for each "tool" class in this module
        buttons = []
        for i in range(len(selections)):
            #the use of j = i lambda is to differentiate which lambda to use so the correct screen is called
            new_button = tk.Button(self, text=selections[i]["nice_name"], command = lambda j = i: controller.show_frame(selections[j]["obj"]))
            new_button.grid(row=1, column=i)

class Welcome(Selection_Menu, tk.Frame):
    is_tool = False
    def __init__(self, parent, controller):
        super().__init__(parent,controller)
        label = tk.Label(self, text="Welcome Page")
        label.grid(row=2, column=0)

class Test_Tool(Selection_Menu, tk.Frame):
    is_tool = True
    nice_name = "Test Tool"
    tool_width = 400
    tool_height = 200
    def __init__(self, parent, controller):
        super().__init__(parent,controller)
        label = tk.Label(self, text="Test Tool Page")
        label.grid(row=2, column=0)

class Test_Two(Selection_Menu, tk.Frame):
    is_tool = True
    nice_name = "Test Tool 2"
    tool_width = 500
    tool_height = 500
    def __init__(self, parent, controller):
        super().__init__(parent,controller)
        label = tk.Label(self, text="Test 2 Tool Page")
        label.grid(row=2, column=0)






#find all classes in this module
max_tool_width, max_tool_height, selections = find_all_tools()

#launch the app
app = Control()
geo = str(max_tool_width) + "x" + str(max_tool_height)
app.geometry(geo)
app.mainloop()
