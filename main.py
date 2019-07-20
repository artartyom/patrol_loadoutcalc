import tkinter
from tkinter import messagebox
all_items=pd.read_csv("items.csv")

window=tkinter.Tk() 
buttons=[]
checkbutton_vals=[]
data=[]

with open("items.csv") as datafile:
    line=datafile.readline()
    for line in datafile:
        data.append(line.strip('\n').split(','))
        checkbutton_vals.append(tkinter.BooleanVar())
        buttons.append([
            tkinter.Spinbox(window, from_=1, to=10, width=3),
            tkinter.Checkbutton(window, var=checkbutton_vals[-1]),
            tkinter.Label(window, text=data[-1][1])
        ])
        buttons[-1][0].grid(row=len(buttons), column=1)
        buttons[-1][1].grid(row=len(buttons), column=2)
        buttons[-1][2].grid(row=len(buttons), column=3)

def get_button_vals(buttons):
    result=[]
    for n in range(0, len(buttons)):
        result.append(
            (buttons[n][0].get(),
            checkbutton_vals[n].get())
        )
    return result

def recalculate(buttons, values):
    button_vals=get_button_vals(buttons)
    totalweight=0
    for n in range(0,len(button_vals)):
        if not checkbutton_vals[n].get():
            pass
        else:
            totalweight+=int(data[n][3])*int(buttons[n][0].get())
    weight_title="Total weight: "
    tkinter.messagebox.showinfo('Weight', weight_title+str(totalweight))
    return 

ok_button=tkinter.Button(window, text="Recalculate", command = lambda: recalculate(buttons, data))
ok_button.grid(row=len(buttons)+1, column=3)

window.mainloop()
