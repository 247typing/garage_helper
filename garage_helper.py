import tkinter as tk
import sys, inspect
import os
from PIL import Image, ImageTk
import pathlib

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

#This funciton takes a single entry and performs basic error checking and division
#accepted inputs are integers, floats, and fractions with '/' character
#returns float if acceptable other wise returns "ERROR"
def check_entry(entry):
    #check if entry is empty
    if entry:
        #try to convert to float directly
        try:
            solution = float(entry)
            return solution
        except ValueError:
            #if that doesn't work, check for single '/' indicating division
            fraction = entry.split('/')
            if len(fraction) == 2:
                solution = float(fraction[0]) / float(fraction[1])
                return solution
        solution = "ERROR"
    else:
        print("empty")
    return "ERROR"

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

#This is a special class that contains the top frame that contains buttons to select tools
class Selection_Menu(tk.Frame):
    is_tool = False
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        selection_frame = tk.Frame(self)
        selection_frame.grid(row=0, column=0)

        #create a button for each "tool" class in this module
        buttons = []
        for i in range(len(selections)):
            #the use of j = i lambda is to differentiate which lambda to use so the correct screen is called
            new_button = tk.Button(selection_frame,
                                text=selections[i]["nice_name"],
                                font = BUTTON_FONT,
                                command = lambda j = i: controller.show_frame(selections[j]["obj"]),
                                anchor="w")

            #used to be self
            new_button.grid(row=0, column=i, padx=10, pady = 10)

#special class that doesn't have a button in the selection menu
#this is the welcome screen and cannot be accessed after selecting a tool
class Welcome(Selection_Menu, tk.Frame):
    is_tool = False
    def __init__(self, parent, controller):
        super().__init__(parent,controller)
        tool_frame = tk.Frame(self)
        tool_frame.grid(row = 1, column = 0)
        label = tk.Label(tool_frame, text="Welcome Page", font=DEFAULT_TOOL_FONT)
        label.grid(row=0, column=0)
        label = tk.Label(tool_frame,
                        text="Select the tool you would like to use from the buttons above",
                        font=DEFAULT_TOOL_FONT,
                        wraplength=max_tool_width,
                        justify="left")

        label.grid(row=1, column=0)

class Drill_Tap_Chart(Selection_Menu, tk.Frame):
    is_tool = True
    nice_name = "Drill Tap Chart"
    tool_width = 400
    tool_height = 1000

    def __init__(self, parent, controller):
        super().__init__(parent,controller)
        self.tool_frame = tk.Frame(self)
        self.tool_frame.grid(row = 1, column = 0)

        label = tk.Label(self.tool_frame, text=self.nice_name, font=TOOL_TITLE_FONT)
        label.grid(row=0, column=1)

        label = tk.Label(self.tool_frame, text="Pitch (as TPI)", font=DEFAULT_TOOL_FONT)
        label.grid(row=1, column=1)

        self.tap_TPI_entry = tk.Entry(self.tool_frame, font=DEFAULT_TOOL_FONT, width=4)
        self.tap_TPI_entry.grid(row=2, column=1)

        label = tk.Label(self.tool_frame, text="Major Diameter", font=DEFAULT_TOOL_FONT)
        label.grid(row=4, column=0)

        self.tap_dia_entry = tk.Entry(self.tool_frame, font=DEFAULT_TOOL_FONT, width=7)
        self.tap_dia_entry.grid(row=5, column=0)

        screw_image = Image.open("images\\Drill_Tap_Chart\\input_image.png")
        photo = ImageTk.PhotoImage(screw_image)
        label = tk.Label(self.tool_frame, image=photo)
        label.image = photo
        label.grid(row=4, column=1, rowspan=3, pady=15)

        screw_plate = Image.open("images\\Drill_Tap_Chart\\hole_sizes.png")
        photo = ImageTk.PhotoImage(screw_plate)
        label = tk.Label(self.tool_frame, image=photo)
        label.image = photo
        label.grid(row=7, column=0, columnspan=3, pady=15)


        calc_button = tk.Button(self.tool_frame, text="Calculate", font=DEFAULT_TOOL_FONT, command=self.get_entries)
        calc_button.grid(row=10, column=2)

    def get_entries(self):
        print(self.tap_dia_entry.get())
        print(self.tap_TPI_entry.get())

        tap_dia = check_entry(self.tap_dia_entry.get())
        if tap_dia == "ERROR":
            pass #change to popup message indicating error

        #clear the text in the boxes
        self.tap_dia_entry.delete(0, 'end')
        self.tap_TPI_entry.delete(0, 'end')

        #######Needs a grid forget used in a clear function ########################'
        #might be able to use self.label_X to forget "hide" each one or might try destroy
        label_1 = tk.Label(self.tool_frame, text="Used: ", font=DEFAULT_TOOL_FONT)
        label_1.grid(row=3, column=1)
        
        label = tk.Label(self.tool_frame, text="Used: ", font=DEFAULT_TOOL_FONT)
        label.grid(row=6, column=0)

        label = tk.Label(self.tool_frame, text="Actual: ", font=DEFAULT_TOOL_FONT)
        label.grid(row=8, column=0)

        label = tk.Label(self.tool_frame, text="Actual: ", font=DEFAULT_TOOL_FONT)
        label.grid(row=8, column=1)

        label = tk.Label(self.tool_frame, text="Actual: ", font=DEFAULT_TOOL_FONT)
        label.grid(row=8, column=2)

        label = tk.Label(self.tool_frame, text="Closest: ", font=DEFAULT_TOOL_FONT)
        label.grid(row=9, column=0)

        label = tk.Label(self.tool_frame, text="Closest: ", font=DEFAULT_TOOL_FONT)
        label.grid(row=9, column=1)

        label = tk.Label(self.tool_frame, text="Closest: ", font=DEFAULT_TOOL_FONT)
        label.grid(row=9, column=2)


class Test_Two(Selection_Menu, tk.Frame):
    is_tool = True
    nice_name = "Test Tool 2"
    tool_width = 800
    tool_height = 500
    def __init__(self, parent, controller):
        super().__init__(parent,controller)
        tool_frame = tk.Frame(self)
        tool_frame.grid(row = 1, column = 0)
        label = tk.Label(tool_frame, text="Test 2 Tool Page", font=TOOL_TITLE_FONT)
        label.grid(row=2, column=0)

#TODO needs to be moved to a config file #####################
BUTTON_FONT = ("arial", 18)
DEFAULT_TOOL_FONT = ("arial", 16)
TOOL_TITLE_FONT = ("arial bold", 24)


#find all classes in this module
max_tool_width, max_tool_height, selections = find_all_tools()


#launch the app
app = Control()
geo = str(max_tool_width) + "x" + str(max_tool_height)
print(geo)
app.geometry(geo)
app.mainloop()
