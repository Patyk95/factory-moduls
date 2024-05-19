import customtkinter as ctk
from datetime import datetime
import sqlite3
ctk.set_default_color_theme('green')
ctk.set_appearance_mode('dark')


class Baza_danych():
    def __init__(self,db_name):
        self.con=sqlite3.connect(db_name)
        self.cur= self.con.cursor()

    def Create(self,table_name,columns):
        columns_with_types = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})'
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
        self.title ('maintennace system')

        self.personal_number=ctk.CTkEntry(self,width=350,font=('arial',30))
        self.personal_number.grid(row=1,column=2)

        self.label1=ctk.CTkLabel(self,text='PODAJ NAZWKĘ MASZYNY: ',font=('arial',25))
        self.label1.grid(row=1,column=1,padx=20,pady=20,sticky='n')

        self.machine_number=ctk.CTkEntry(self,width=350,font=('arial',30))
        self.machine_number.grid(row=2,column=2)

        self.label2=ctk.CTkLabel(self,text='PODAJ NUM PERSONALNY: ',font=('arial',25))
        self.label2.grid(row=2,column=1,padx=20,pady=20,sticky='n')

        self.label3=ctk.CTkLabel(self,text='OPISZ KRÓTKO ZDARZENIE: ',font=('arial',25))
        self.label3.grid(row=3,column=1,padx=20,pady=20,sticky='n')

        self.reason=ctk.CTkEntry(self,width=350,font=('arial',30))
        self.reason.grid(row=3,column=2)

        self.button2=ctk.CTkButton(self,width=30,text='ZGŁOŚ AWARIĘ',command=self.Zglos,font=('arial',30))
        self.button2.grid(row=5,column=1,padx=20,pady=20,sticky='n')

    def Zglos(self):
        machine= self.machine_number.get()
        personal=self.personal_number.get()
        issue=self.reason.get()
        current_time= datetime.now()
        time=current_time.strftime(("%Y-%m-%d %H:%M:%S"))
        print(f'Została zgłoszona awaria na maszynie {machine} przez pracownika {personal} o godzinie {time} po wystąpieniu {issue}')




b=Baza_danych("mainenance_db")

# b.Select('CH04')

current_time= datetime.now()
time=current_time.strftime(("%Y-%m-%d %H:%M:%S"))
# b.Insert("CH04",{'id':3,'data_zdarzenia':time,'pracownik':6501,'zdarzenie': 'urwało narzędzie'})
# b.Select_with_codnition('Ch04','pracownik =6500')