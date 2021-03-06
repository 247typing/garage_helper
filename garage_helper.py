import tkinter as tk
import sys, inspect
import os
from PIL import Image, ImageTk
import pathlib
import pandas as pd
import webbrowser
import yaml

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

#This method takes a single entry and performs basic error checking and division
#accepted inputs are integers, floats, and fractions with '/' character, as well as mixed numbers
#where an interger is spearated by a space from a fraction ex: 1 1/2 = 1.5
#returns float if acceptable other wise returns "ERROR" or "EMPTY"
def check_entry(entry):
    #check if entry is empty
    if entry:
        #try to convert to float directly
        try:
            solution = float(entry)
            return solution
        except ValueError:
            #check for '#' character indicating a screw size
            if "#" in entry:
                #search screw_dia.csv for match and return float dia 0.XXX format
                df = pd.read_csv(os.path.join(*["static_data", "Drill_Tap_Chart", "number_dia.csv"]))
                try:
                    entry = df.loc[df.screw_num == entry, "dia_in"].iloc[0]
                except IndexError:
                    return "ERROR"
                float("{:.3f}".format(round(entry,3)))
                return entry
            elif "/" in entry:
                whole_num = 0 #initialize whole_num to zero to handle the case of fraction less than 1
                if " " in entry: #the case of mixed numbers
                    seperate = entry.split(' ')
                    if len(seperate) == 2:
                        try: #if first number is not able to convert to float its an error
                            whole_num = float(seperate[0])
                        except ValueError:
                            return "ERROR"
                        entry = seperate[1]

                #if that doesn't work, check for single '/' indicating division
                fraction = entry.split('/')
                if len(fraction) == 2:
                    solution = float(fraction[0]) / float(fraction[1])
                    return solution + whole_num
                else:
                    return "ERROR"
            else:
                return "ERROR"
    return "EMPTY"

#The Control code was derived from this tutorial
#https://pythonprogramming.net/tkinter-depth-tutorial-making-actual-program/
class Control(tk.Tk):
    is_tool = False
    top_frame = None
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
        self.top_frame = cont #allows program to determine which frame is showing
        print(self.top_frame.__name__)
        frame.tkraise()

#This class creates a popup windows that can display contents of a text file if given or a given message.
#The contructor can be called with msg = Popup("This is a popup text message")
#or msg = Popup(os.path.join(*["path","and", "filename.txt"]), is_file=True)
class Popup(tk.Tk):
    is_tool = False

    def __init__(self, input, is_file=False):
        tk.Tk.__init__(self)
        self.iconbitmap(os.path.join(*ICON_PATH))
        #file name passed as input so display text file
        #The files first line should be the title and will be treated as such
        if is_file:
            with open(input, 'r') as f:
                lines = f.readlines()
                heading = lines[0].split('\n')[0] #remove the newline char
                self.title(heading)
                label = tk.Label(self, text=heading, font=conf["font"]["TOOL_TITLE"])
                label.grid(row=0, column=0)

                #print all lines from line 2 to end of the help file
                for i in range(len(lines) - 1):
                    label = tk.Label(self, text=lines[i + 1].split('\n')[0], font=conf["font"]["DEFAULT_TOOL"])
                    label.grid(row=i + 1, column=0, sticky='w')
            i = i + 1; #increment i for button to have correct row


        else:
            i = 0 #i is used for button row determination
            label = tk.Label(self, text=input, font=conf["font"]["DEFAULT_TOOL"])
            label.grid(row=i, column=0, pady = 10, padx = 10)
            self.title("Popup")

        button = tk.Button(self, text = "Close", font=conf["font"]["BUTTON"], command=self.destroy)
        button.grid(row=i+1, column=0, pady = 10)

#This is a special class that contains the top frame that contains buttons to select tools
class Selection_Menu(tk.Frame):
    is_tool = False
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        selection_frame = tk.Frame(self)
        selection_frame.grid(row=1, column=0)

        #create a button for each "tool" class in this module
        buttons = []
        for i in range(len(selections)):
            #the use of j = i lambda is to differentiate which lambda to use so the correct screen is called
            new_button = tk.Button(selection_frame,
                                text=selections[i]["nice_name"],
                                font = conf["font"]["BUTTON"],
                                command = lambda j = i: controller.show_frame(selections[j]["obj"]),
                                anchor="w")

            #used to be self
            new_button.grid(row=1, column=i, padx=10, pady = 10)



        #add a settings/help bar to the top left of the page
        settings_frame = tk.Frame(self, width=max_tool_width)
        settings_frame.grid(row=0, column=0, sticky="ew")
        self.grid_columnconfigure(0, weight=1)



        #add a help button that opens the help page if available
        photo_path = G_H_PATH + ["images", "Main", "question_mark.png"]
        image = Image.open(os.path.join(*photo_path)).resize((25,35))
        photo = ImageTk.PhotoImage(image)
        help_button = tk.Button(settings_frame, image=photo, font=conf["font"]["DEFAULT_TOOL"], command=self.open_help)
        help_button.image = photo
        help_button.pack(side="left", padx=2)

        #settings gear button
        photo_path = G_H_PATH + ["images", "Main", "gear.png"]
        image = Image.open(os.path.join(*photo_path)).resize((35,35))
        photo = ImageTk.PhotoImage(image)
        settings_button = tk.Button(settings_frame, image=photo, font=conf["font"]["DEFAULT_TOOL"], command=self.open_settings)
        settings_button.image = photo
        settings_button.pack(side="left", padx=2)

        git_button = tk.Button(settings_frame, text="GitHub Project", font=conf["font"]["DEFAULT_TOOL"], command=self.open_github)
        git_button.pack(side="left", padx=2)

    #open the settings file for the user to edit
    def open_settings(self):
        total_path_list = G_H_PATH + ["prog_data", "config.yml"]
        os.system(os.path.join(*total_path_list))
        Popup("If you saved any changes please close and restart the program for them to take effect.")

    #open the github page in the default browser
    def open_github(self):
        webbrowser.open("https://github.com/247typing/garage_helper")

    def open_help(self):
        #this opens a page with the help file of the current open page
        help_location = os.path.join(*["tool_help", app.top_frame.__name__ + ".txt"])
        if os.path.exists(help_location): #if no file found show a default message
            help_page = Popup(help_location, is_file=True)
        else:
            no_help_page = Popup("Help page was not found please try another page.")

#special class that doesn't have a button in the selection menu
#this is the welcome screen and cannot be accessed after selecting a tool
class Welcome(Selection_Menu, tk.Frame):
    is_tool = False
    def __init__(self, parent, controller):
        super().__init__(parent,controller)
        tool_frame = tk.Frame(self)
        tool_frame.grid(row = 2, column = 0)
        label = tk.Label(tool_frame, text="Welcome Page", font=conf["font"]["DEFAULT_TOOL"])
        label.grid(row=0, column=0)
        label = tk.Label(tool_frame,
                        text="Select the tool you would like to use from the buttons above",
                        font=conf["font"]["DEFAULT_TOOL"],
                        wraplength=max_tool_width,
                        justify="left")

        label.grid(row=1, column=0)

class Drill_Tap_Chart(Selection_Menu, tk.Frame):
    is_tool = True
    nice_name = "Drill Tap Chart"
    tool_width = 620
    tool_height = 760

    def __init__(self, parent, controller):
        super().__init__(parent,controller)
        self.tool_frame = tk.Frame(self)
        self.tool_frame.grid(row = 2, column = 0)

        label = tk.Label(self.tool_frame, text=self.nice_name, font=conf["font"]["TOOL_TITLE"])
        label.grid(row=0, column=1)

        label = tk.Label(self.tool_frame, text="Pitch (as TPI)", font=conf["font"]["DEFAULT_TOOL"])
        label.grid(row=1, column=1)

        self.tap_TPI_entry = tk.Entry(self.tool_frame, font=conf["font"]["DEFAULT_TOOL"], width=4)
        self.tap_TPI_entry.grid(row=2, column=1)

        label = tk.Label(self.tool_frame, text="Major Diameter", font=conf["font"]["DEFAULT_TOOL"])
        label.grid(row=4, column=0)

        self.major_dia_entry = tk.Entry(self.tool_frame, font=conf["font"]["DEFAULT_TOOL"], width=7)
        self.major_dia_entry.grid(row=5, column=0)

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


        calc_button = tk.Button(self.tool_frame, text="Calculate", font=conf["font"]["DEFAULT_TOOL"], command=self.calculate)
        calc_button.grid(row=10, column=2, sticky="w")

        clear_button = tk.Button(self.tool_frame, text="Clear", font=conf["font"]["DEFAULT_TOOL"], command=self.clear_all)
        clear_button.grid(row=10, column=1, sticky="e")
    def calculate(self):
        TPI = self.tap_TPI_entry.get()
        if TPI:
            #check the entered string is an integer
            if TPI.isdigit():
                try:
                    TPI = int(self.tap_TPI_entry.get())
                except ValueError:
                    TPI = "ERROR"
            else:
                TPI = "ERROR"
        else:
            TPI = "EMPTY"

        #check dia entry for ints, floats, or fractions
        major_dia = check_entry(self.major_dia_entry.get())

        if major_dia == "ERROR" or TPI == "ERROR":
            error_msg = Popup("There was an error in Drill Tap Chart. Click the question mark above for more help.")
            return
        if major_dia == "EMPTY" or TPI == "EMPTY":
            return
        else:
            pitch = 1 / TPI
            tap_drill = major_dia - pitch

            #round to one thousands of an inch
            ########add min and max to precentages##################################

            #3% clearance
            tight_drill = major_dia*1.03
            #8% clearance
            loose_drill = major_dia*1.08


            tap_bit = self.find_drill(tap_drill)
            tight_bit = self.find_drill(tight_drill)
            loose_bit = self.find_drill(loose_drill)
            print(tight_bit)
            #format for output
            tight_drill = "{:.3f}".format(round(tight_drill, 3))
            loose_drill = "{:.3f}".format(round(loose_drill, 3))
            major_dia = "{:.3f}".format(round(major_dia, 3))
            pitch = "{:.3f}".format(round(pitch, 3))
            tap_drill = "{:.3f}".format(round(tap_drill, 3))


        print(tight_drill)
        self.clear_calc() #prevent multiple layers from building up
        self.labels = [] #this list contains all of the labels for the solution
        #this allows for labels to be appended and easily destroyed later to clear the screen
        self.labels.append(tk.Label(self.tool_frame, text="Used: "+pitch+'"', font=conf["font"]["DEFAULT_TOOL"]))
        #assign the last label a position
        self.labels[-1].grid(row=3, column=1)

        self.labels.append(tk.Label(self.tool_frame, text="Used: "+major_dia+'"', font=conf["font"]["DEFAULT_TOOL"]))
        self.labels[-1].grid(row=6, column=0)

        self.labels.append(tk.Label(self.tool_frame, text="Actual: "+tap_drill+'"', font=conf["font"]["DEFAULT_TOOL"]))
        self.labels[-1].grid(row=8, column=0)

        self.labels.append(tk.Label(self.tool_frame, text="Actual: "+tight_drill+'"', font=conf["font"]["DEFAULT_TOOL"]))
        self.labels[-1].grid(row=8, column=1)

        self.labels.append(tk.Label(self.tool_frame, text="Actual: "+loose_drill+'"', font=conf["font"]["DEFAULT_TOOL"]))
        self.labels[-1].grid(row=8, column=2)

        self.labels.append(tk.Label(self.tool_frame, text="Closest Bit: "+tap_bit, font=conf["font"]["DEFAULT_TOOL"]))
        self.labels[-1].grid(row=9, column=0)

        self.labels.append(tk.Label(self.tool_frame, text="Closest Bit: "+tight_bit, font=conf["font"]["DEFAULT_TOOL"]))
        self.labels[-1].grid(row=9, column=1)

        self.labels.append(tk.Label(self.tool_frame, text="Closest Bit: "+loose_bit, font=conf["font"]["DEFAULT_TOOL"]))
        self.labels[-1].grid(row=9, column=2)

    def clear_all(self):
        self.clear_calc()
        self.clear_entry()

    def clear_calc(self):
        try: #handles first clear if no lables created
            #clear all of the label from calculate
            for label in self.labels:
                label.destroy()
        except AttributeError:
            return

    def clear_entry(self):
        #clear the text in the boxes
        self.major_dia_entry.delete(0, 'end')
        self.tap_TPI_entry.delete(0, 'end')

    #takes the drill size and returns the next largest bit size from the csv file
    def find_drill(self, size):
        ######## add a drop down with metric / standard drill bit set ##################

        df = pd.read_csv(os.path.join(*["static_data", "Drill_Tap_Chart", "english_drill_sizes.csv"]))

        for index, row in df.iterrows():
            if size < row["dia_in"]:
                return row["bit"]
        #to handle the case of not large enough drill bit
        return "N/A"

class Lathe_Speeds(Selection_Menu, tk.Frame):
    is_tool = True
    nice_name = "Lathe Feeds and Speeds"
    tool_width = 550
    tool_height = 630

    speeds_df = pd.read_csv(os.path.join(*["static_data", "Lathe_Speeds", "cutting_speeds.csv"]))
    def __init__(self, parent, controller):
        super().__init__(parent,controller)
        self.tool_frame = tk.Frame(self)
        self.tool_frame.grid(row = 2, column = 0)

        label = tk.Label(self.tool_frame, text=self.nice_name, font=conf["font"]["TOOL_TITLE"])
        label.grid(row=0, column=0, columnspan=2)

        label = tk.Label(self.tool_frame, text="Select Material", font=conf["font"]["DEFAULT_TOOL"])
        label.grid(row=1, column=0, columnspan=2)

        materials = self.speeds_df["material"].tolist()

        self.selected_mat = tk.StringVar(self.tool_frame)
        self.selected_mat.set(materials[1])

        drop_down = tk.OptionMenu(self.tool_frame, self.selected_mat, *materials)
        drop_down.configure(font=conf["font"]["DEFAULT_TOOL"])
        drop_down.grid(row=2, column=0, columnspan=2)

        chuck_image = Image.open(os.path.join(*["images", "Lathe_Speeds", "lathe_chuck.png" ]))
        chuck_image = chuck_image.resize((300,300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(chuck_image)
        label = tk.Label(self.tool_frame, image=photo)
        label.image = photo
        label.grid(row=3, column=0, rowspan=3, pady=15)

        label = tk.Label(self.tool_frame, text="Enter Material Diameter", font=conf["font"]["DEFAULT_TOOL"])
        label.grid(row=3, column=1, sticky="s")

        self.material_dia = tk.Entry(self.tool_frame, font=conf["font"]["DEFAULT_TOOL"], width=4)
        self.material_dia.grid(row=4, column=1, sticky="n")

        calc_button = tk.Button(self.tool_frame, text="Calculate", font=conf["font"]["DEFAULT_TOOL"], command=self.calculate)
        calc_button.grid(row=7, column=1, sticky="w")

        clear_button = tk.Button(self.tool_frame, text="Clear", font=conf["font"]["DEFAULT_TOOL"], command=self.clear_all)
        clear_button.grid(row=7, column=0, sticky="e")

    def calculate(self):
        mat_dia = check_entry(self.material_dia.get())
        if mat_dia == "ERROR":
            Popup("There was an error in Lathe Speeds. Click the question mark above for more help.")
            return
        elif mat_dia == "EMPTY":
            return

        material = self.selected_mat.get()
        df = pd.read_csv(os.path.join(*["static_data", "Lathe_Speeds", "cutting_speeds.csv"]))
        cutting_speed = df.loc[df["material"] == material, "surface_feet_per_min"].iloc[0]
        RPM = (cutting_speed * 12) / (3.14 * mat_dia)

        mat_dia = "{:.3f}".format(round(mat_dia, 3))
        RPM = str(int(round(RPM)))

        self.clear_calc() #prevent multiple layers from building up
        self.labels = []

        self.labels.append(tk.Label(self.tool_frame, text="Diameter Used: "+mat_dia+'"', font=conf["font"]["DEFAULT_TOOL"]))
        self.labels[-1].grid(row=5, column=1, sticky="n")

        self.labels.append(tk.Label(self.tool_frame, text="Calculated RPM: "+RPM, font=conf["font"]["DEFAULT_TOOL"]))
        self.labels[-1].grid(row=6, column=0)

    def clear_all(self):
        self.clear_calc()
        self.clear_entry()

    def clear_calc(self):
        try: #handles first clear if no lables created
            #clear all of the label from calculate
            for label in self.labels:
                label.destroy()
        except AttributeError:
            return

    def clear_entry(self):
        #clear the text in the boxes
        self.material_dia.delete(0, 'end')


#######################  WINDOWS SPECIFIC CODE HERE  ########################################
#G_H_PATH is a list of the path to get to garage_helper script ["C:\", "User", "and", "so", "on"]
G_H_PATH = os.path.dirname(os.path.realpath(__file__))
G_H_PATH = G_H_PATH.split("\\")
G_H_PATH[0] = G_H_PATH[0] + "\\" #add the \ back to C:\ or D:\ etc

#read the config file and store it in a dict conf for easy access
total_path = G_H_PATH + ["prog_data", "config.yml"]
with open(os.path.join(*total_path), "r") as f:
    try:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    except yaml.YAMLError as exc:
        print(exc)

#find all classes in this module
max_tool_width, max_tool_height, selections = find_all_tools()

#launch the app
app = Control()
geo = str(max_tool_width) + "x" + str(max_tool_height)
print(geo)
app.geometry(geo)

#add app icon to top left corner
ICON_PATH = G_H_PATH + ["images", "Main", "workbench.ico"]
app.iconbitmap(os.path.join(*ICON_PATH))

#add main title
app.title("Garage Helper")
app.mainloop()
