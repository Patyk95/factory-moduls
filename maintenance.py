import customtkinter as ctk
from datetime import datetime
ctk.set_default_color_theme('green')
ctk.set_appearance_mode('dark')



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








app=Apk()

app.mainloop()