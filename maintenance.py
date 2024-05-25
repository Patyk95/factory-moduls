from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime
import sqlite3
import tkinter as tk
from xlsxwriter.workbook import Workbook

ctk.set_default_color_theme('green')
ctk.set_appearance_mode('dark')


class Apk (ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('850x550')
        self.title ('maintenace system')
        self.menubar = tk.Menu()
        self.config(menu=self.menubar)

        self.machine_number_var = ctk.StringVar()
        self.material_number_var = ctk.StringVar()
        self.personal_number_var = ctk.StringVar()
        self.reason_var = ctk.StringVar()


        self.structure_label=ctk.CTkLabel(self,text='JEDNOSTKA ORGANIZACYJNA :',font=('arial',25),width=30)
        self.structure_label.grid(row=1,column=1,padx=20,pady=20,sticky='n')

        self.structureOptionMenu = ctk.CTkOptionMenu(self,
                                        values=['Produkcja Bezpośrednia','Utrzymanie Ruchu',
                                        'Przygotowanie Produkcji','Pomiary - Dział Jakości','Serwis Zewnętrzny'],width=30,font=('arial',25))
    
        self.structureOptionMenu.grid(row=1, column=2,
                                       padx=20, pady=20,
                                       columnspan=2)
        
        self.machine_label=ctk.CTkLabel(self,text='PODAJ NAZWĘ MASZYNY: ',font=('arial',25),width=40)
        self.machine_label.grid(row=2,column=1,padx=20,pady=20,sticky='n')

        self.machine_number=ctk.CTkEntry(self,textvariable=self.machine_number_var,width=350,font=('arial',30))
        self.machine_number.grid(row=2,column=2)

        self.material_label=ctk.CTkLabel(self,text='PRODUKOWANY ARTYKUŁ: ',font=('arial',25),width=40)
        self.material_label.grid(row=3,column=1,padx=20,pady=20,sticky='n')

        self.material_number=ctk.CTkEntry(self,textvariable=self.material_number_var,width=350,font=('arial',30))
        self.material_number.grid(row=3,column=2)

        self.personal_label=ctk.CTkLabel(self,text='PODAJ NUM PERSONALNY: ',font=('arial',25),width=30)
        self.personal_label.grid(row=4,column=1,padx=20,pady=20,sticky='n')

        self.personal_number=ctk.CTkEntry(self,textvariable=self.personal_number_var,width=350,font=('arial',30))
        self.personal_number.grid(row=4,column=2)

        self.reason_label=ctk.CTkLabel(self,text='OPISZ ZDARZENIE/CZYNNOŚĆ: ',font=('arial',25),width=30)
        self.reason_label.grid(row=5,column=1,padx=20,pady=20,sticky='n')

        self.reason=ctk.CTkEntry(self,textvariable=self.reason_var,width=350,font=('arial',30))
        self.reason.grid(row=5,column=2)

        self.button2=ctk.CTkButton(self,width=30,text='ODNOTUJ',command=self.Zgłos,font=('arial',30))
        self.button2.grid(row=6,column=1,padx=20,pady=20,sticky='n')

        self.machine_number_var.trace_add("write", self.to_uppercase)
        self.personal_number_var.trace_add("write", self.to_uppercase)
        self.reason_var.trace_add("write", self.to_uppercase)

        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Załóż Bazę",command=self.Create)
        file_menu.add_command(label="Wyczyść Bazę",command=self.Drop),
        file_menu.add_command(label="Importuj Bazę",command=self.To_excel)
       
        view_menu = tk.Menu(self.menubar, tearoff=0)
        view_menu.add_command(label="Szybki Podgląd",command=self.Display_database)

        self.menubar.add_cascade(label="Baza Danych", menu=view_menu)   
        self.menubar.add_cascade(label="System", menu=file_menu) 


    def to_uppercase(self, *args):
        self.machine_number_var.set(self.machine_number.get().upper())
        self.material_number_var.set(self.material_number.get().upper())
        self.personal_number_var.set(self.personal_number.get().upper())
        self.reason_var.set(self.reason.get().upper()
        )

    def Create(self):
        con=sqlite3.connect("maintenance_db")
        cur= con.cursor()
        cur.execute('create table if not exists maszyny (id integer primary key autoincrement, data_akcji not null, jednostka not null,maszyna not null,produkowany_material,operator not null, awaria not null)')
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
    

    def Zgłos(self):
        currenttime=datetime.now() 
        time=currenttime.strftime('%Y-%m-%d %H:%M:%S')
        con=sqlite3.connect("maintenance_db")
        cur= con.cursor()
        cur.execute('insert into maszyny(data_akcji,jednostka,maszyna,produkowany_material,operator,awaria) values(:data,:jednostka,:maszyna,:material,:operator,:usterka)',
                {
                    'data': time ,
                    'jednostka':self.structureOptionMenu.get(),
                    'maszyna': self.machine_number.get(),
                    'material': self.material_number.get(),
                    'operator': self.personal_number.get(),
                    'usterka': self.reason.get()
                })
        con.commit()
        messagebox.showinfo('Wiadomość Systemow','Adnotacja Została Dodana') 
        self.machine_number.delete(0,'end'),
        self.material_number.delete(0,'end'),
        self.personal_number.delete(0,'end'),
        self.reason.delete(0,'end')
        

    def Display_database(*args):
        con=sqlite3.connect("maintenance_db")
        cur = con
        results = cur.execute('select * from maszyny')
        w = results.fetchall()
        if len(w) > 0:
            window = tk.Tk()
            window.title('Baza Danych')
            window.geometry('1450x800')
            window.configure(background='#b3b3b3')
            columns = ('c1', 'c2', 'c3', 'c4', 'c5','c6','c7')
            tree = tk.ttk.Treeview(window, columns=columns, show='headings', height=52)
            tree.heading('c1', text='Id')
            tree.heading('c2', text='Data')
            tree.heading('c3', text='Jednostka')
            tree.heading('c4', text='Maszyna')
            tree.heading('c5', text='Material')
            tree.heading('c6', text='Operator')
            tree.heading('c7', text='Usterka')
            for row in cur.execute('select id,data_akcji,jednostka,maszyna,produkowany_material,operator,awaria from maszyny'):
                tree.insert('', tk.END, values=(row[0], row[1], row[2], row[3], row[4],row[5],row[6]))
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