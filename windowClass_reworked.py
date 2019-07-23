import tkinter

class Scrollframe():

    def scroll(self, event):
        self.parts["canvas"].configure(scrollregion=self.parts["canvas"].bbox("all"),width=400,height=580)

    def repopulate_scrollframe(self, data, new = False):
        for x in range(0,5):
            self.parts["labels"][x].grid(row=1, column=x+1)
        
        if not new:
            for item in self.buttons:
                for widget in item:
                    widget.destroy()

        for x in range(0, len(data.axes[0])):
            self.add_multibutton(data.iloc[x], new)
        self.parts["master"].update_idletasks()

    def add_multibutton(self, item_data, new = True):
        id=int(item_data["id"])
        if new:
            self.buttonvals.append((tkinter.BooleanVar(),tkinter.IntVar(),tkinter.StringVar(),tkinter.StringVar(),tkinter.StringVar()))
            self.buttonvals[-1][1].set(1)
            self.buttonvals[-1][2].set(str(item_data["name"]))
            self.buttonvals[-1][3].set(str(item_data["weight"]))
            self.buttonvals[-1][4].set(str(item_data["xp_cost"]))

        print(id)
        self.buttons.append(
            [
                tkinter.Checkbutton(self.parts["frame"], var=self.buttonvals[id][0]),
                tkinter.Spinbox(self.parts["frame"], from_ = 1, to = 10, width = 3, textvariable=self.buttonvals[id][1]),
                tkinter.Label(self.parts["frame"], textvariable=self.buttonvals[id][2]),
                tkinter.Label(self.parts["frame"], textvariable=self.buttonvals[id][3]),
                tkinter.Label(self.parts["frame"], textvariable=self.buttonvals[id][4])
            ]
        )
        for x in range(0,5):
            self.buttons[-1][x].grid(row=len(self.buttons)+1, column=x+1)

    def sort(self, var):
        self.repopulate_scrollframe(data = self.data.sort_values(var), new = False)

    def __init__(self, root, data):
        self.root = root
        self.data = data
        self.parts = {"master" : tkinter.Frame(self.root, relief=tkinter.GROOVE, width=400, height=580, bd=1)}
        self.parts["canvas"] = tkinter.Canvas(self.parts["master"])
        self.parts["frame"] = tkinter.Frame(self.parts["canvas"])
        self.parts["scrollbar"] = tkinter.Scrollbar(self.parts["master"], orient="vertical",command=self.parts["canvas"].yview)

        self.parts["canvas"].configure(yscrollcommand=self.parts["scrollbar"].set)        
        self.parts["canvas"].pack(side="left")
        self.parts["scrollbar"].pack(side="right", fill="y")
        
        self.parts["canvas"].create_window((0,0),window=self.parts["frame"])
        self.parts["frame"].bind("<Configure>",self.scroll)

        self.parts["labels"] = (
            tkinter.Label(self.parts["frame"], text="Use"),
            tkinter.Label(self.parts["frame"], text="Quantity"),
            tkinter.Button(self.parts["frame"], text="Name", command = lambda: self.sort("name")),
            tkinter.Button(self.parts["frame"], text="Weight", command = lambda: self.sort("weight")),
            tkinter.Button(self.parts["frame"], text="XP cost", command = lambda: self.sort("xp_cost"))
        )

        self.buttonvals = []
        self.buttons = []
        self.repopulate_scrollframe(self.data, new = True)
        self.parts["master"].place(x=0, y=0)

class Staticframe():

    def place_params(self):
        self.footer = (
            (
                tkinter.Label(self.parts["master"], text="Per-item XP cost modifier: "),
                tkinter.Spinbox(self.parts["master"], from_=-10, to=10, textvariable=self.vars["xpmod"], width=3)
            ),
            (
                tkinter.Label(self.parts["master"], text="Calculated weight: "),
                tkinter.Label(self.parts["master"], textvariable=self.vars["totalweight"])
            ),
            (
                tkinter.Label(self.parts["master"], text="Calculated XP cost: "),
                tkinter.Label(self.parts["master"], textvariable=self.vars["totalcost"])
            ),
            (
                tkinter.Button(self.parts["master"], text="Recalculate", command = lambda: self.recalculate()),
                tkinter.Button(self.parts["master"], text="Add standard loadout", command = lambda: self.stdload()),
                tkinter.Button(self.parts["master"], text="Reset", command = lambda: self.reset())
            )
            )
        for y in range(0, len(self.footer)-1):
            self.footer[y][0].grid(row=y, column=1)
            self.footer[y][1].grid(row=y, column=2)
        self.footer[-1][0].grid(row=3, column=1)
        self.footer[-1][1].grid(row=4, column=1)
        self.footer[-1][2].grid(row=5, column=1)

    def reset_vars(self):
        self.vars["xpmod"].set(0)
        self.vars["totalweight"].set(0)
        self.vars["totalcost"].set(0)

    def __init__(self, root):
        self.root = root

        self.vars = {
            "xpmod" : tkinter.IntVar(),
            "totalweight" : tkinter.IntVar(),
            "totalcost" : tkinter.IntVar()
        }
        self.reset_vars()

        self.parts = {"master": tkinter.Frame(self.root, relief=tkinter.GROOVE, width=390, height=580)}
        self.parts["master"].place(x=430,y=10)
        self.place_params()

class Window():

    def __init__(self, windowName, itemdata):
        self.window = tkinter.Tk()            
        self.window.wm_geometry("800x600+0+0")
        self.window.title(str(windowName))
        self.itemdata = itemdata

        self.itemView = Scrollframe(self.window, self.itemdata)
        self.optionsView = Staticframe(self.window)

    def recalculate(self):
        wt=0
        xp=0
        xp_mod=int(self.xpmod.get())
        for index in range(0,len(self.buttons)):
            if self.buttonvals[index][0].get():
                item_wt = int(self.buttons[index][3]["text"])
                item_xp = int(self.buttons[index][4]["text"])
                item_num = int(self.buttons[index][1].get())
                wt += item_wt*item_num
                if item_xp>0 and item_xp+xp_mod > 0:
                    xp+=(item_xp+xp_mod)*item_num
        self.totalweight.set(wt)
        self.totalxpcost.set(xp)

    def reset(self):
        self.totalweight.set(0)
        self.totalxpcost.set(0)
        self.xpmod.set(0)
        for index in range(0, len(self.buttons)):
            self.buttonvals[index][0].set(0)
            self.buttonvals[index][1].set(1)

    def stdload(self):
        self.recalculate()

    def render(self):
        self.window.mainloop()
