from tkinter import *
# from tkinter.ttk import *
from tkinter.filedialog import askopenfile
import sqlite3
from tkinter import messagebox
from classifier import predict,prediction
from PIL import ImageTk, Image
import pandas as pd
import tkinter.font as font
k = ""

def prev():
    import tkinter as tk
    from tkinter import ttk

    def show():
        conn = sqlite3.connect('Database\\sepsis.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM data")
        result = cur.fetchall()
        tempList = [list(i) for i in result]
        conn.commit()
        conn.close()



        for (id, name, sepsis_diag) in tempList:
            listBox.insert("", "end", values=(id, name, sepsis_diag))


    scores = Tk()
    scores.resizable(False,False)
    scores.title("")
    label = tk.Label(scores, text="Sepsis Diagnostic Results", font=("Arial", 30)).grid(row=0, columnspan=3)
    cols = ('ID', 'Name', 'Sepsis Result')
    listBox = ttk.Treeview(scores, columns=cols, show='headings')
    for col in cols:
        listBox.heading(col, text=col)
    listBox.grid(row=1, column=0, columnspan=2)
    show()

    scores.mainloop()
def diag(prediction):
    conn = sqlite3.connect('Database\\sepsis.db')
    conn.execute('''UPDATE data SET sepsis_diag= ? where id=?''', (prediction,b))
    conn.commit()
    conn.close()
    diag_window = Tk()

    text = Text(diag_window)


    diag_window.title("Early Diagnosis of Sepsis")
    diag_window.geometry("600x250+200+100")
    diag_window.resizable(False, False)
    # diag_window = Toplevel(root)

    if prediction=="positive":
        text.config(wrap=WORD, font='Arial', bg='#b33e3e')
        messagebox.showinfo("Sepsis Result", "Sepsis-Positive",parent = diag_window)
        text.insert(INSERT, "GUIDELINES TO BE FOLLOWED:--\n")
        text.insert(INSERT,"1. Administer broad spectrum antibiotics (covering gram-positive and gram-negative organisms) within one hour of diagnosis or in those with high clinical suspicion for sepsis or septic shock.\n")
        text.insert(INSERT,"2. Obtain two or more sets of blood cultures prior to the administration of antibiotics; at least one set should be peripheral, the other from a vascular access device, if present.\n")
        text.insert(INSERT,"3. In taking care of a patient with sepsis, it is imperative to re-assess hemodynamics, volume status and tissue perfusion regularly.")
        text.pack()

    else:
        text.config(wrap=WORD, font='Arial', bg='#32a852')
        messagebox.showinfo("Sepsis Result", "Sepsis-Negative",parent = diag_window)
        text.insert(INSERT, "GUIDELINES TO BE FOLLOWED:--\n")
        text.insert(INSERT,"1. Hygienic hand disinfection is recommended before and after each patient encounter.\n")
        text.insert(INSERT,"2. A routine change of intravascular and urinary catheters is not recommended.\n")
        text.insert(INSERT,"3. It is recommended to use oral antiseptics for infection prevention.\n")
        text.insert(INSERT,"4. A moderate intravenous insulin therapy to lower the increased blood glucose levels sho be considered in ICU patients.")
        text.pack()


def dbwrite(a,b):
    conn = sqlite3.connect('Database\\sepsis.db')
    conn.execute('INSERT INTO data (id,name) VALUES (?,?)',(b,a))
    conn.commit()
    conn.close()


root = Tk()
root.title("Early Prediction of Sepsis using Clinical Data")
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
        global b
        a = name.get()
        b = id.get()
        dbwrite(a, b)
        data = content
        f = open("Database\\data.csv", "w")
        f.write(data)
        f.close()
        global k
        df = pd.read_csv('Database\\data.csv', sep='|')
        k=predict(df)



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

def_font=font.Font(family='arial')

btn = Button(root, text='Browse File', command=lambda: open_file(),font=def_font)
btn.place(x=260,y=250)


btn3 = Button(root, text='Previous Diagnostic Results', command=lambda: prev(),font=def_font)
btn3.pack(side = BOTTOM, pady=25, anchor=CENTER)

btn2 = Button(root, text='Run Diagnostic', command=lambda: diag(k),font=def_font)
btn2.place(x=246, y=300)

mainloop()



