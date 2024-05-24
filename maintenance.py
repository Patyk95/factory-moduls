from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime
import sqlite3
import tkinter as tk
from xlsxwriter.workbook import Workbook

ctk.set_default_color_theme('green')
ctk.set_appearance_mode('dark')
currenttime=datetime.now()
time=currenttime.strftime('%Y-%m-%d %H:%M:%S')


class Apk (ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('750x400')
        self.title ('maintenace system')
        self.menubar = tk.Menu()
        self.config(menu=self.menubar)

        self.machine_number_var = ctk.StringVar()
        self.personal_number_var = ctk.StringVar()
        self.reason_var = ctk.StringVar()

       
        self.personal_number=ctk.CTkEntry(self,textvariable=self.personal_number_var,width=350,font=('arial',30))
        self.personal_number.grid(row=1,column=2)

        self.label1=ctk.CTkLabel(self,text='PODAJ NAZWĘ MASZYNY: ',font=('arial',25))
        self.label1.grid(row=1,column=1,padx=20,pady=20,sticky='n')

        self.machine_number=ctk.CTkEntry(self,textvariable=self.machine_number_var,width=350,font=('arial',30))
        self.machine_number.grid(row=2,column=2)

        self.label2=ctk.CTkLabel(self,text='PODAJ NUM PERSONALNY: ',font=('arial',25))
        self.label2.grid(row=2,column=1,padx=20,pady=20,sticky='n')

        self.label3=ctk.CTkLabel(self,text='OPISZ KRÓTKO ZDARZENIE: ',font=('arial',25))
        self.label3.grid(row=3,column=1,padx=20,pady=20,sticky='n')

        self.reason=ctk.CTkEntry(self,textvariable=self.reason_var,width=350,font=('arial',30))
        self.reason.grid(row=3,column=2)

        self.button2=ctk.CTkButton(self,width=30,text='ZGŁOŚ AWARIĘ',command=self.Zgłoś,font=('arial',30))
        self.button2.grid(row=5,column=1,padx=20,pady=20,sticky='n')

        self.machine_number_var.trace_add("write", self.to_uppercase)
        self.personal_number_var.trace_add("write", self.to_uppercase)
        self.reason_var.trace_add("write", self.to_uppercase)

        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Załóż Bazę",command=self.Create)
        file_menu.add_command(label="Wyczyść Bazę",command=self.Drop),
        file_menu.add_command(label="Importuj Bazę",command=self.To_excel)
        file_menu.add_separator()
        file_menu.add_command(label="Exit",command=exit)

        view_menu = tk.Menu(self.menubar, tearoff=0)
        view_menu.add_command(label="Szybki Podgląd",command=self.display_database)

        self.menubar.add_cascade(label="Baza Danych", menu=view_menu)   
        self.menubar.add_cascade(label="System", menu=file_menu) 


    def to_uppercase(self, *args):
        self.machine_number_var.set(self.machine_number.get().upper())
        self.personal_number_var.set(self.personal_number.get().upper())
        self.reason_var.set(self.reason.get().upper()
        )

    def Create(self):
        con=sqlite3.connect("maintenance_db")
        cur= con.cursor()
        cur.execute('create table if not exists maszyny (id integer primary key autoincrement, data_akcji not null, maszyna not null, operator not null, awaria not null)')
        messagebox.showinfo('Informacja Systemowa', 'Baza Danych Została Stworzona')
        con.commit()
    

    def Drop(self):
        con=sqlite3.connect("maintenance_db")
        cur= con.cursor()
        cur.execute('drop table maszyny')
        messagebox.showinfo('Informacja Systemowa', 'Baza Danych Została Usunięta')
        con.commit()


    def To_excel(*args):
        workbook = Workbook('Failure_file.xlsx')
        worksheet = workbook.add_worksheet('Awarie')
        con=sqlite3.connect("maintenance_db")
        cur = con
        mysel = cur.execute("select * from maszyny")
        for i, row in enumerate(mysel):
            for j, value in enumerate(row):
                worksheet.write(i, j, row[j])
        messagebox.showinfo('Informacja Systemowa', 'Baza Danych Została Zaimportowana')
        workbook.close()
    

    def Zgłoś(self):
        con=sqlite3.connect("maintenance_db")
        cur= con.cursor()
        cur.execute('insert into maszyny(data_akcji,maszyna,operator,awaria) values(:data,:maszyna,:operator,:usterka)',
                {
                    'data': time ,
                    'maszyna': self.machine_number.get(),
                    'operator': self.personal_number.get(),
                    'usterka': self.reason.get()
                })
        con.commit()
        messagebox.showinfo('Wiadomość Systemow','Adnotacja Została Dodana') 
        self.machine_number.delete(0,'end'),
        self.personal_number.delete(0,'end'),
        self.reason.delete(0,'end')
        
    def display_database(*args):
        con=sqlite3.connect("maintenance_db")
        cur = con
        results = cur.execute('select * from maszyny')
        w = results.fetchall()
        if len(w) > 0:
            window = tk.Tk()
            window.title('Baza Danych Awari')
            window.geometry('1050x800')
            window.configure(background='#b3b3b3')
            columns = ('c1', 'c2', 'c3', 'c4', 'c5')
            tree = tk.ttk.Treeview(window, columns=columns, show='headings', height=52)
            tree.heading('c1', text='Id')
            tree.heading('c2', text='Data')
            tree.heading('c3', text='Maszyna')
            tree.heading('c4', text='Operator')
            tree.heading('c5', text='Usterka')
            for row in cur.execute('select id,data_akcji,maszyna,operator,awaria from maszyny'):
                tree.insert('', tk.END, values=(row[0], row[1], row[2], row[3], row[4]))
                tree.grid(row=0, column=0, sticky='n')
                scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscroll=scrollbar.set)
                scrollbar.grid(row=0, column=1, sticky='ns')
                con.commit()
        else:
            messagebox.showinfo('Informacja Systemowa', 'Baza Danych Jest Pusta')



con=sqlite3.connect('maintenance_db')
cur=con
# for i in cur.execute('select * from maszyny'):
    #  print (i)




ap=Apk()
ap.mainloop()