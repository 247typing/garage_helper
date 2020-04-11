import tkinter as tk

class Main_Window:

    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text="Hello")
        self.button1.grid(column=0, row=0)
        self.button2 = tk.Button(self.frame, text="World")
        self.button2.grid(column=1, row=0)
        self.button3 = tk.Button(self.frame, text="Test")
        self.button3.grid(column=2, row=0)
        self.master.title("Garage Helper")
        self.master.geometry('800x700')




        self.frame.pack()

class Testing:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text="Testing")
        self.button1.grid(column=0, row=0)
        self.button2 = tk.Button(self.frame, text="Again")
        self.button2.grid(column=1, row=0)
        self.button3 = tk.Button(self.frame, text="Tested")
        self.button3.grid(column=2, row=0)
        self.frame.pack()

root = tk.Tk()
app = Main_Window(root)
app2 = Testing(root)

root.mainloop()
