#this is just a template that can be copied and pasted into garage_helper.py as a start to a new tool.

class Name_Me(Selection_Menu, tk.Frame):
    is_tool = True
    nice_name = "Name Me"
    tool_width = 1 #set in pixels
    tool_height = 1 #set in pixels

    #read in any data used in the tool here

    def __init__(self, parent, controller):
        super().__init__(parent,controller)
        self.tool_frame = tk.Frame(self)
        self.tool_frame.grid(row = 2, column = 0)

        label = tk.Label(self.tool_frame, text=self.nice_name, font=conf["font"]["TOOL_TITLE"])
        label.grid(row=0, column=0, columnspan=2)

        #start adding tool content here to the tool_frame
