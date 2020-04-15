import tkinter as tk
import sys, inspect


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
        frame.pack()

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

#class Welcome(tk.Frame):
class Welcome(Selection_Menu, tk.Frame):
    is_tool = True
    def __init__(self, parent, controller):
        super().__init__(parent,controller)
        label = tk.Label(self, text="Welcome Page")
        label.pack()

app = Control()
app.mainloop()

#get a list of all classes in the module
classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)

#sort out the name of each class and its attribute of is_tool
#used for getting all tools automaticaly
for cls in classes:
    print(cls[0])
    print(eval(cls[0]).is_tool)



#print(inspect.getmembers(Control))
