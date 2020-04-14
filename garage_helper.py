import tkinter as tk
import sys, inspect


#The Selection_Menu code was derived from this tutorial
#https://pythonprogramming.net/tkinter-depth-tutorial-making-actual-program/
class Selection_Menu(tk.Tk):
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

class Welcome(tk.Frame):
    is_tool = True
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Welcome Page")
        label.pack()

app = Selection_Menu()
#app.mainloop()

#get a list of all classes in the module
classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)

#sort out the name of each class and its attribute of is_tool
#used for getting all tools automaticaly
for cls in classes:
    print(cls[0])
    print(eval(cls[0]).is_tool)



#print(inspect.getmembers(Selection_Menu))
