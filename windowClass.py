import tkinter

class Scrollframe():

    def scroll(self, event):
        self.parts["canvas"].configure(scrollregion=self.parts["canvas"].bbox("all"),width=530,height=535)

    def repopulate_scrollframe(self, data, new = False):
        for item in ["frame","scrollbar","canvas"]:
            try:
                if self.parts[item]:
                    self.parts[item].destroy()
            except KeyError:
                pass

        self.parts["canvas"] = tkinter.Canvas(self.parts["down_row"])
        self.parts["frame"] = tkinter.Canvas(self.parts["canvas"], width = 540, height = 30*len(data.axes[0]))
        self.parts["scrollbar"] = tkinter.Scrollbar(self.parts["down_row"], orient="vertical",command=self.parts["canvas"].yview)
        self.parts["canvas"].configure(yscrollcommand=self.parts["scrollbar"].set)        
        self.parts["canvas"].pack(side="left")
        self.parts["scrollbar"].pack(side="right", fill="y")        
        self.parts["canvas"].create_window((5,40),window=self.parts["frame"])
        self.parts["frame"].bind("<Configure>",self.scroll)

        for i in range(0,6):
            self.parts["labels"][i].place(x=self.xval[i], y=self.yval[i])
        
        if not new:
            for item in self.multibuttons["buttons"]:
                for widget in item:
                    widget.destroy()
        
        self.multibuttons["buttons"]=[]
        self.multibuttons["buttonframes"]=[]

        for x in range(0, len(data.axes[0])):
            self.add_multibutton(data.iloc[x], new)
        
        for i in range(0, len(self.multibuttons["buttonframes"])):
            self.multibuttons["buttonframes"][i].place(x=0, y=i*30)
        
        self.parts["canvas"].update_idletasks()

    def add_multibutton(self, item_data, new = True):
        id=int(item_data["id"])
        xmod = [15, 15, 5, 10, 35, 35]
        if new:
            self.multibuttons["buttonvals"].append((tkinter.BooleanVar(),tkinter.IntVar(),tkinter.StringVar(),tkinter.StringVar(),tkinter.IntVar(),tkinter.IntVar()))
            self.multibuttons["buttonvals"][-1][1].set(1)
            self.multibuttons["buttonvals"][-1][2].set(str(item_data["name"]))
            self.multibuttons["buttonvals"][-1][3].set(str(item_data["type"]))
            self.multibuttons["buttonvals"][-1][4].set(str(item_data["weight"]))
            self.multibuttons["buttonvals"][-1][5].set(str(item_data["xp_cost"]))

       # print(id)
        self.multibuttons["buttonframes"].append(tkinter.Frame(self.parts["frame"], width=530, height=30))
        self.multibuttons["buttons"].append(
            [
                tkinter.Checkbutton(self.multibuttons["buttonframes"][-1], var=self.multibuttons["buttonvals"][id][0]),
                tkinter.Spinbox(self.multibuttons["buttonframes"][-1], from_ = 1, to = 10, width = 3, textvariable=self.multibuttons["buttonvals"][id][1]),
                tkinter.Label(self.multibuttons["buttonframes"][-1], textvariable=self.multibuttons["buttonvals"][id][2]),
                tkinter.Label(self.multibuttons["buttonframes"][-1], textvariable=self.multibuttons["buttonvals"][id][3]),
                tkinter.Label(self.multibuttons["buttonframes"][-1], textvariable=self.multibuttons["buttonvals"][id][4]),
                tkinter.Label(self.multibuttons["buttonframes"][-1], textvariable=self.multibuttons["buttonvals"][id][5])
            ]
        )
        for i in range(0,6):
            self.multibuttons["buttons"][-1][i].place(x=(self.xval[i]+xmod[i]), y=3)

    def sort(self, var):
        if self.sortedby[0] == var:
            self.repopulate_scrollframe(data = self.data.sort_values(var, ascending = 1-self.sortedby[1]), new = False)
            self.sortedby = (var, 1-self.sortedby[1])
        else:
            self.repopulate_scrollframe(data = self.data.sort_values(var, ascending = 1), new = False)
            self.sortedby = (var, 1)


    def __init__(self, root, data, new=True):
        self.root = root
        self.data = data

        self.xval = [5, 45, 110, 300, 400, 470]
        self.yval = [5, 5, 0, 0, 0, 0]

        self.parts = {"master" : tkinter.Frame(self.root, relief=tkinter.GROOVE, width=550, height=590)}
        self.parts["upper_row"] = tkinter.Frame(self.parts["master"],relief=tkinter.GROOVE, width = 545, height = 30, bd = 1)
        self.parts["down_row"] = tkinter.Frame(self.parts["master"], relief = tkinter.GROOVE, width=540, height = 535, bd = 1)


        self.parts["upper_row"].place(x=5, y=5)
        self.parts["down_row"].place(x=5, y=40)

        self.parts["labels"] = (
            tkinter.Label(self.parts["upper_row"], text="Use"),
            tkinter.Label(self.parts["upper_row"], text="Quantity"),
            tkinter.Button(self.parts["upper_row"], text="Name", command = lambda: self.sort("name")),
            tkinter.Button(self.parts["upper_row"], text="Type", command = lambda: self.sort("type")),
            tkinter.Button(self.parts["upper_row"], text="Weight", command = lambda: self.sort("weight")),
            tkinter.Button(self.parts["upper_row"], text="XP cost", command = lambda: self.sort("xp_cost"))
        )

        self.multibuttons = {
            "buttonframes" : [],
            "buttons" : [],
            "buttonvals" : []
        }

        self.repopulate_scrollframe(self.data, new = True)
        self.sortedby = ("none", 1)

        self.parts["master"].place(x=0, y=0)

class Window():

    def __init__(self, windowName, itemdata):
        self.window = tkinter.Tk()            
        self.window.wm_geometry("800x600+0+0")
        self.window.title(str(windowName))

        self.itemdata = itemdata
        self.stdload = self.itemdata[self.itemdata["std"]==1]["id"]
        print(self.stdload)

        self.itemView = Scrollframe(self.window, self.itemdata)

        self.optionsView = tkinter.Frame(self.window, relief=tkinter.GROOVE, width=225, height=300)
        self.optionsView.place(x=575,y=100)
        
        self.vars = {
            "xpmod" : tkinter.IntVar(),
            "totalweight" : tkinter.IntVar(),
            "totalcost" : tkinter.IntVar()
        }
        
        self.place_params()
        self.place_filters()
        self.reset_vars()

    def place_params(self):
        self.footer = (
            (
                tkinter.Label(self.optionsView, text="Per-item XP cost modifier: "),
                tkinter.Spinbox(self.optionsView, from_=-10, to=10, textvariable=self.vars["xpmod"], width=3)
            ),
            (
                tkinter.Label(self.optionsView, text="Calculated weight: "),
                tkinter.Label(self.optionsView, textvariable=self.vars["totalweight"])
            ),
            (
                tkinter.Label(self.optionsView, text="Calculated XP cost: "),
                tkinter.Label(self.optionsView, textvariable=self.vars["totalcost"])
            ),
            (
                tkinter.Button(self.optionsView, text="Recalculate", command = self.recalculate),
                tkinter.Button(self.optionsView, text="Reset to standard loadout", command = lambda: self.reset_vars(std_eq=1)),
                tkinter.Button(self.optionsView, text="Reset to no items", command=lambda: self.reset_vars(std_eq=0)),
                tkinter.Button(self.optionsView, text="Apply filters", command=self.filter),
                tkinter.Button(self.optionsView, text="Select all", command=lambda: self.allfilter(1)),
                tkinter.Button(self.optionsView, text="Deselect all", command=lambda: self.allfilter(0))
            )
            )
        for y in range(0, len(self.footer)-1):
            self.footer[y][0].grid(row=y, column=1)
            self.footer[y][1].grid(row=y, column=2)
        self.footer[-1][0].grid(row=3, column=1)
        self.footer[-1][1].grid(row=4, column=1)
        self.footer[-1][2].grid(row=5, column=1)
        self.footer[-1][3].grid(row=6, column=1)
        self.footer[-1][4].grid(row=7, column=1)
        self.footer[-1][5].grid(row=8, column=1)
        
    def place_filters(self):
        self.filters = []
        self.filterFrame=tkinter.Canvas(self.window, width=240, height=300)

        for itemtype in set(self.itemdata.loc[:,"type"]):
            print(itemtype)
            self.filters.append([
                itemtype,
                tkinter.BooleanVar()
            ])
            self.filters[-1].append(tkinter.Checkbutton(self.filterFrame, var=self.filters[-1][1], text=itemtype))
            self.filters[-1][1].set(1)

        for filter_no in range(0,len(self.filters)):
            self.filters[filter_no][2].place(y=(filter_no//2)*17, x=(filter_no%2)*120)
        self.filterFrame.place(x=560, y=350)

    def reset_vars(self, std_eq=0):
        self.vars["xpmod"].set(0)
        self.vars["totalweight"].set(0)
        self.vars["totalcost"].set(0)

        for button_val in self.itemView.multibuttons["buttonvals"]:
            button_val[0].set(0)
            button_val[1].set(1)
        
        if std_eq==1:
            for item_id in self.stdload:
                self.itemView.multibuttons["buttonvals"][item_id][0].set(1)
        
        self.recalculate()
    
    def recalculate(self):
        xp_modifier=self.vars["xpmod"].get()
        total_wt=0
        total_xp=0
        for button_val in self.itemView.multibuttons["buttonvals"]:
            if button_val[0].get():
                total_wt+=button_val[1].get()*button_val[4].get()
                if button_val[5].get() > 0 and (button_val[5].get()+xp_modifier) > 0 :
                    total_xp += (button_val[5].get() + xp_modifier) * button_val[1].get()
        self.vars["totalweight"].set(total_wt)
        self.vars["totalcost"].set(total_xp)

    def filter(self):
        selected = []
        for filt in self.filters:
            if filt[1].get():
                selected.append(filt[0])
        selected_rows=[]
        for i in range(0,len(self.itemdata.axes[0])):
            selected_rows.append(self.itemdata.iloc[i,2] in selected)
        self.itemView.data = self.itemdata[selected_rows]
        self.itemView.repopulate_scrollframe(self.itemView.data, new=False)

    def allfilter(self, selection_mode):
        for filt in self.filters:
            filt[1].set(selection_mode)
        self.filter()