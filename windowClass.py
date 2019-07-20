import tkinter

class Window():
    def myfunction(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=400,height=580)

    def __init__(self, windowName):
        self.window_tk = tkinter.Tk()            
        self.window_tk.wm_geometry("800x600+0+0")
        self.masterframe = tkinter.Frame(self.window_tk, relief=tkinter.GROOVE, width=400, height=580, bd=1)
        self.masterframe.place(x=10,y=10)   
        self.footerframe = tkinter.Frame(self.window_tk, relief=tkinter.GROOVE, width=390, height=580)
        self.footerframe.place(x=430,y=10)

        self.canvas=tkinter.Canvas(self.masterframe)
        self.frame = tkinter.Frame(self.canvas)
        self.scrollbar=tkinter.Scrollbar(self.masterframe,orient="vertical",command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left")
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.create_window((0,0),window=self.frame)
        self.frame.bind("<Configure>",self.myfunction)

        self.footercanvas=tkinter.Canvas(self.footerframe)
        self.footerframe=tkinter.Frame(self.footercanvas)
        self.footercanvas.place(x=0, y=0)

        self.footercanvas.create_window((200,200),window=self.footerframe)
        self.footercanvas.configure(width=400,height=580)    

        self.window_tk.title(str(windowName))
        self.labels = (
            tkinter.Label(self.frame, text="Use"),
            tkinter.Label(self.frame, text="Quantity"),
            tkinter.Label(self.frame, text="Name"),
            tkinter.Label(self.frame, text="Weight"),
            tkinter.Label(self.frame, text="XP cost")
            )

        for x in range(0,5):
            self.labels[x].grid(row=1, column=x+1)

        self.buttons = []
        self.buttonvals = []
        self.totalweight = tkinter.IntVar()
        self.totalxpcost = tkinter.IntVar()
        self.xpmod = tkinter.IntVar()
        self.xpmod.set(0)
        self.totalweight.set(0)
        self.totalxpcost.set(0)


    def add_multibutton(self, item_data):
        self.buttonvals.append((tkinter.BooleanVar(),tkinter.IntVar()))
        self.buttonvals[-1][1].set(1)
        self.buttons.append(
            [
                tkinter.Checkbutton(self.frame, var=self.buttonvals[len(self.buttonvals)-1][0]),
                tkinter.Spinbox(self.frame, from_ = 1, to = 10, width = 3, textvariable=self.buttonvals[len(self.buttonvals)-1][1]),
                tkinter.Label(self.frame, text=str(item_data[0])),
                tkinter.Label(self.frame, text=str(item_data[2])),
                tkinter.Label(self.frame, text=str(item_data[3]))
            ]
        )
        for x in range(0,5):
            self.buttons[-1][x].grid(row=len(self.buttons)+1, column=x+1)

    def make_footer(self):
        self.footer = (
            (
                tkinter.Label(self.footerframe, text="Per-item XP cost modifier: "),
                tkinter.Spinbox(self.footerframe, from_=-10, to=10, textvariable=self.xpmod, width=3)
            ),
            (
                tkinter.Label(self.footerframe, text="Calculated weight: "),
                tkinter.Label(self.footerframe, textvariable=self.totalweight)
            ),
            (
                tkinter.Label(self.footerframe, text="Calculated XP cost: "),
                tkinter.Label(self.footerframe, textvariable=self.totalxpcost)
            ),
            (
                tkinter.Button(self.footerframe, text="Recalculate", command = lambda: self.recalculate()),
                tkinter.Button(self.footerframe, text="Add standard loadout", command = lambda: self.stdload()),
                tkinter.Button(self.footerframe, text="Reset", command = lambda: self.reset())
            )
            )
        for y in range(0, len(self.footer)-1):
            self.footer[y][0].grid(row=y, column=1)
            self.footer[y][1].grid(row=y, column=2)
        self.footer[-1][0].grid(row=3, column=1)
        self.footer[-1][1].grid(row=4, column=1)
        self.footer[-1][2].grid(row=5, column=1)

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
        self.make_footer()
        self.window_tk.mainloop()
