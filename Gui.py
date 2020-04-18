from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
import sqlite3
from PIL import ImageTk, Image
import pandas as pd
from classifier import predict,prediction

def prev():
    import tkinter as tk
    from tkinter import ttk

    def show():
        conn = sqlite3.connect('Database\\sepsis.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM data")
        result = cur.fetchall()
        tempList = [list(i) for i in result]
        # print(tempList)
        conn.commit()
        conn.close()

        # tempList = [['Jim', '0.33'], ['Dave', '0.67'], ['James', '0.67'], ['Eden', '0.5']]
        # tempList.sort(key=lambda e: e[1], reverse=True)

        for (id, name, sepsis_diag) in tempList:
            listBox.insert("", "end", values=(id, name, sepsis_diag))


    scores = Tk()
    # scores.geometry("300x400+200+100")
    scores.resizable(False,False)
    scores.title("")
    label = tk.Label(scores, text="Sepsis Diagnostic Results", font=("Arial", 30)).grid(row=0, columnspan=3)
    cols = ('ID', 'Name', 'Sepsis Result')
    listBox = ttk.Treeview(scores, columns=cols, show='headings')
    for col in cols:
        listBox.heading(col, text=col)
    listBox.grid(row=1, column=0, columnspan=2)
    show()
    # showScores = tk.Button(scores, text="Show Results", width=15, command=show).grid(row=4, column=0)
    # closeButton = tk.Button(scores, text="Close", width=15, command=exit).grid(row=4, column=0)
    # closeButton = Button(scores, text="Close", width=15, command=exit)
    # closeButton.pack(side = BOTTOM)
    scores.mainloop()
def diag(df):

    diag_window = Tk()
    # diag_window.protocol("WM_DELETE-_WINDOW", disable_event)
    # root.config(state=DISABLED)
    mainframe = Frame(diag_window)
    mainframe.grid()
    diag_window.title("Early Diagnosis of Sepsis")
    diag_window.geometry("600x400+200+100")
    diag_window.resizable(False, False)
    # root.grab_set()
    result = Text(diag_window, bd=2)
    tips = Text(diag_window, bd=2)
    output_result = 1
    if output_result:
        result.config(font=("Arial", 12), bg="#f05959")
        result.insert(END, "SEPSIS-POSITIVE")
        result.pack(side=LEFT,  fill=BOTH)

        # tips.config(font=("Arial", 12))
        # tips.insert(END, "Administer broad spectrum antibiotics (covering gram-positive and gram-negative organisms) within one hour of diagnosis or in those with high clinical suspicion for sepsis or septic shock.")
        # tips.insert(END,"Obtain two or more sets of blood cultures prior to the administration of antibiotics; at least one set should be peripheral, the other from a vascular access device, if present.")
        # tips.insert(END," In taking care of a patient with sepsis, it is imperative to re-assess hemodynamics, volume status and tissue perfusion regularly.")
        # tips.pack(side=RIGHT, fill=BOTH, expand=YES)
    else:
        result.config(font=("Arial", 12), bg="#63ff80")
        result.insert(END, "SEPSIS-NEGATIVE")
        result.pack(side=LEFT, fill=BOTH, expand=YES)

        tips.config(font=("Arial", 12))
        tips.insert(1, "THIS IS A TEST TIPS")
        tips.pack(side=RIGHT, fill=BOTH, expand=YES)
    sqlite3.connect('')



    # root.grab_release()

def dbwrite(a,b):
    # print(a)
    conn = sqlite3.connect('Database\\sepsis.db')
    conn.execute('INSERT INTO data (id,name) VALUES (?,?)',(b,a))
    conn.commit()
    conn.close()


root = Tk()
root.title("")
root.geometry("600x400+200+100")
root.resizable(False, False)

heading_main = Label(root, text = "BML Munjal University",compound = CENTER)
heading_main.config(font=("Arial", 25))
heading_main.pack(pady = 10)


img_bml = Image.open("Images\\BML_Munjal_University-Logo.png")
img_bml_resized = img_bml.resize((80,80))
img_bml_logo = ImageTk.PhotoImage(img_bml_resized)
img_bml_label = Label(root,image = img_bml_logo)
img_bml_label.place(x=0,y=0)

img_sih = Image.open("Images\\SIH_2018_logo.png")
img_sih_resized = img_sih.resize((75,75))
img_sih_logo = ImageTk.PhotoImage(img_sih_resized)
img_sih_label = Label(root,image = img_sih_logo)
img_sih_label.place(x=525,y=0)


def open_file():
    file = askopenfile(mode='r', filetypes=[('PSV Files', '*.psv')])
    if file is not None:
        content = file.read()
        a = name.get()
        b = id.get()
        dbwrite(a,b)
        data = content
        print(data)
        f = open("Database\\data.csv", "w")
        f.write(data)
        f.close()

        df = pd.read_csv('Database\\data.csv',sep='|')
        
        btn2 = Button(root, text='Run Diagnostic', command=lambda: predict(df))
        btn2.place(x=252, y=300)
        # predict(df)
        print(prediction)

name = StringVar()
id = StringVar()
lb2= Label(root, text='Name')
lb2.config(font=("Arial", 15))
lb2.place(x=190,y=147)
name = Entry(root, textvar = name)
name.place(x=255,y=150)
lb3= Label(root, text='ID')
lb3.config(font=("Arial", 15))
lb3.place(x=190,y=197)
id = Entry(root, textvar = id)
id.place(x=255, y=200)

btn = Button(root, text='Browse File', command=lambda: open_file())
btn.place(x=260,y=250)

btn3 = Button(root, text='Previous Diagnostic Results', command=lambda: prev())
btn3.pack(side = BOTTOM, pady=30)
# canvas = Canvas(root)
# canvas.create_line(00, 35, 300, 200, dash=(4, 2))

mainloop()



