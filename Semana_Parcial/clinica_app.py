# -*- coding: utf-8 -*-
#%%
import tkinter as tk
import tkinter.ttk as ttk
from db_clinica import Database
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainWindow:
    def __init__(self, master):
        # Definicion de la Ventana Principal
        self.master = master
        self.master.title("Clinica Peso Feliz")
        self.master.resizable(0, 0)
        
        self.db = Database()
        
        style = ttk.Style()
        style.theme_use('default')

        style.configure("Treeview")
        style.map("Treeview", background = [('selected','blue')])
        
        frm = tk.Frame(self.master)
        frm.pack(padx=10, pady=10)
        
        frm1 = tk.LabelFrame(frm, text="Medicos")
        frm1.pack(side=tk.LEFT, padx=10, pady=10)

        frm2 = tk.LabelFrame(frm, text="Data Pacientes")
        frm2.pack(side=tk.LEFT, padx=10, pady=10)
        
        # -------------------------- frm1 ------------------------------
        # Tabla para el registro de los Medicos
        self.tabMedicos = ttk.Treeview(frm1, columns=(1, 2))
        self.tabMedicos.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        data = self.db.listar_medicos()

        self.tabMedicos.heading("#0", text="ID")
        self.tabMedicos.heading("#1", text="Nombre")
        self.tabMedicos.heading("#2", text="Apellido")
        
        self.tabMedicos.column("#0", width=120, minwidth=120, stretch=tk.NO)
        self.tabMedicos.column("#1", width=80, minwidth=80, stretch=tk.NO)
        self.tabMedicos.column("#2", width=80, minwidth=80, stretch=tk.NO)

        for item in data:
            self.tabMedicos.insert("", tk.END, text=item[0], values=item[1:])
        
        self.tabMedicos.bind("<<TreeviewSelect>>", self.update_data_patients)
                
        # NOTA: Al hacer click a un medico debe llamar al metodo self.update_data_patients
        
        # -------------------------- frm2 ------------------------------ 
        # Tabla con el registro de los Pacientes + Scrollbar Vertical
        self.scrY = tk.Scrollbar(frm2, orient='vertical')
        self.tabPacientes = ttk.Treeview(frm2, columns=(1, 2, 3, 4, 5), 
                                         yscrollcommand=self.scrY.set,
                                         selectmode='browse')
        self.scrY.configure(command=self.tabPacientes.yview)
        
        self.tabPacientes.pack(side=tk.LEFT, padx=5, pady=5)
        self.scrY.pack(side=tk.LEFT, expand=True, fill=tk.Y)

        self.tabPacientes.heading("#0", text="ID")
        self.tabPacientes.heading("#1", text="Apellido")
        self.tabPacientes.heading("#2", text="Nombre")
        self.tabPacientes.heading("#3", text="Altura")
        self.tabPacientes.heading("#4", text="Edad")
        self.tabPacientes.heading("#5", text="Sexo")

        self.tabPacientes.bind("<<TreeviewSelect>>", self.open_graph_window)

        # NOTA: Al hacer click a un paciente debe llamar a self.open_graph_window
        
        # ------------------------ statusbar ---------------------------
        self.statusbar = tk.Label(self.master, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tabMedicos.bind("<Enter>", lambda x: self.update_statusbar("Haga click para ver los pacientes asigandos al medico"))
        self.tabMedicos.bind("<Leave>", lambda x: self.update_statusbar(""))
        self.tabPacientes.bind("<Enter>", lambda x: self.update_statusbar("Haga click para ver el registro de peso del paciente"))
        self.tabPacientes.bind("<Leave>", lambda x: self.update_statusbar(""))


    def update_statusbar(self, message):
        # Actualiza los mensajes en el statusbar
        self.statusbar.config(text=message)
        
        
    def update_data_patients(self, event): 
        #Borran datos actuales de la tabla pacientes
        for y in self.tabPacientes.get_children():
            self.tabPacientes.delete(y)
        #Seleccionar ID del medico
        idx = self.tabMedicos.selection()
        id = self.tabMedicos.item(idx)['text']
        #Seleccionar datos de los pacientes del medico
        paci = self.db.listar_pacientes_medico(id)
        #Mostrar datos en la tabla pacientes
        for item in paci:
            self.tabPacientes.insert("", tk.END, text=item[0], values=item[1:])
            
    def open_graph_window(self, event):
        idx = self.tabPacientes.selection()
        id_paciente = self.tabPacientes.item(idx)['text']
        window = tk.Toplevel(self.master)
        GraphWindow(window, id_paciente)
    
    
    
class GraphWindow:
    def __init__(self, master, id_pac):
        self.master = master
        self.master.title("Reporte Grafico")
        self.master.resizable(0, 0)
        self.master.focus()
        self.master.grab_set()

        self.db = Database()
        
        #Variables
        self.varID = id_pac 
        self.nombres = self.db.nombre_paciente(self.varID)
        self.pesos = self.db.data_peso(self.varID)
        self.y = []       
        self.x = [1,]

        for i in list(range(0,len(self.pesos)-1)):
            self.x.append(self.x[i]+1)

        for i in self.pesos:
            self.y.append(i[0])

        #Grafico
        self.fig, self.ax = plt.subplots(figsize=(6, 4), facecolor='#F0F0F0')
        self.line, = self.ax.plot(self.x, self.y, color='r', marker = 's')
        self.ax.grid(linestyle=':')
        self.ax.set_title(f"Paciente - {self.nombres[0]} {self.nombres[1]}")
        self.ax.set_xlabel("Semanas")
        self.ax.set_ylabel("Peso[Kg]")

        self.grafica = FigureCanvasTkAgg(self.fig, master = self.master)
        self.grafica.get_tk_widget().pack(expand=True, fill=tk.BOTH)

root = tk.Tk()
app = MainWindow(root)
root.mainloop()
