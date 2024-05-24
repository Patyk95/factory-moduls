from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime
import sqlite3
from tkinter import StringVar
import re

ctk.set_default_color_theme('green')
ctk.set_appearance_mode('dark')
currenttime=datetime.now()
time=currenttime.strftime('%Y-%m-%d %H:%M:%S')


class Baza_danych():
    def __init__(self,db_name):
        self.con=sqlite3.connect(db_name)
        self.cur= self.con.cursor()

    def Create(self,table_name,columns):
        columns_with_types = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})'
        print(create_table_query)
        self.cur.execute(create_table_query)
        self.con.commit()
        

    def Delete(self,table_name,condition ):
        delete_query =f"Delete from {table_name} where {condition}"
        self.cur.execute(delete_query)
        self.con.commit()

    def Drop (self,table_name):
        drop_table_query =f'drop table if exists {table_name}'
        self.cur.execute(drop_table_query)
        self.con.commit()
    
    
    def Insert(self,table_name, data):
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data.values()])
        values = tuple(data.values())
        insert_query =f'insert into {table_name} ({columns}) values ({placeholders})'
        self.cur.execute(insert_query,values)
        self.con.commit()

    def Select(self,table):
        select_query = f'Select *from {table}'
        # self.cur.execute(select_query)
        for i in self.cur.execute(select_query):
            print (i)

    def Select_with_codnition(self,table,codnition):
        select_query = f'Select *from {table} where {codnition}'
        # self.cur.execute(select_query)
        for i in self.cur.execute(select_query):
            print (i)
    


class Apk (ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('750x400')
        self.title ('maintennace and failure system')

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
    
    def to_uppercase(self, *args):
        self.machine_number_var.set(self.machine_number.get().upper())
        self.personal_number_var.set(self.personal_number.get().upper())
        self.reason_var.set(self.reason.get().upper())


    def Zgłoś(self):
        con=sqlite3.connect("maintenance_db")
        cur= con.cursor()
        # cur.execute('insert into CH04(data_akcji,maszyna,operator,awaria) values(:data,:maszyna,:operator,:usterka)',
        #         {
        #             'data': time ,
        #             'maszyna': self.machine_number.get(),
        #             'operator': self.personal_number.get(),
        #             'usterka': self.reason.get()
                # })
        table_name = self.machine_number_var.get()
        
        if  re.match("^[A-Za-z0-9_]+$", table_name):
            query = f'INSERT INTO {table_name} (data_akcji, maszyna, operator, awaria) VALUES (:data, :maszyna, :operator, :usterka)'
            params = {
                'data': time,
                'maszyna': self.machine_number_var.get(),
                'operator': self.personal_number_var.get(),
                'usterka': self.reason_var.get()
            }
            print(query, params)
            con.commit()

        # self.machine_number.delete(0,'end'),
        # self.personal_number.delete(0,'end'),
        # self.reason.delete(0,'end')
        




b=Baza_danych("maintenance_db")



# b.Create('CH04',{'id': 'integer primary key autoincrement',
#                 'data_akcji': 'not null',
#                 'maszyna':'not null',
#                 'operator':'not null',
#                 'awaria':'not null'})



# b.Insert ('CH04',{'data_akcji': time,
#                 'maszyna':'CH04',
#                 'operator':'6500',
#                 'awaria':'awaria'})

con=sqlite3.connect('maintenance_db')
cur=con
for i in cur.execute('select * from CH04'):
    print (i)


ap=Apk()
ap.mainloop()