# -*- coding: utf-8 -*-
#%%
#INSTRUCCIONES:
# * CONECTARME A LA DB
# * CREAR UN CURSOR
# * REALIZAR UN CONJUNTO DE ACCIONES:
#   * CREAR UNA TABLA
#   * BORRAR UNA TABLA
#   * INSERTAR UN REGISTRO
#   * CONSULTAR INFORMACION
#   * MODIFICAR INFORMACION
#   * ELIMIAR UN REGISTRO
#   * CONFIRMAR UN CAMBIO
#   * DESHACER LAS OPERACIONES
# * CERRAR LA CONEXION

#%%
import sqlite3

# CREAR UNA TABLA

comn = sqlite3.connect("database.db")

cur = comn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS pacientes 
                        (id_pac INTEGER PRIMARY KEY, 
                         nombre TEXT NOT NULL, 
                         peso INTEGER NOT NULL, 
                         altura REAL NOT NULL)""")

comn.commit()

comn.close()

#%%
import sqlite3

comn = sqlite3.connect("database.db")
cur = comn.cursor()

try:
    cur.execute("""""")
except:
    print("ERROR: La tabla no existe")

comn.close()
#%%
#Insertar registros

import sqlite3

comn = sqlite3.connect("database.db")
cur = comn.cursor()

personas = [("Elsa Payo", 54, 1.65),
            ("Armando Paredes", 88, 1.75),
            ("Susana Oria", 48, 1.60),
            ("Esteban Dido", 110, 1.68),
           ]

SQL_QUERY = """INSERT INTO pacientes
                        (nombre, peso, altura)
                    VALUES (?, ?, ?)"""

cur.execute(SQL_QUERY, ("Elvio Lado", 80, 1.72))

comn.commit()
comn.close()

#%%
#Insertar varios registros

import sqlite3

comn = sqlite3.connect("database.db")
cur = comn.cursor()

personas = [("Elsa Payo", 54, 1.65),
            ("Armando Paredes", 88, 1.75),
            ("Susana Oria", 48, 1.60),
            ("Esteban Dido", 110, 1.68),
           ]

SQL_QUERY = """INSERT INTO pacientes
                        (nombre, peso, altura)
                    VALUES (?, ?, ?)"""

cur.executemany(SQL_QUERY, personas)

comn.commit() #<- Actualiza
comn.close()

#%% ----------------------------------------------------------------------------


import sqlite3

comn = sqlite3.connect("database.db")
cur = comn.cursor()

SQL_QUERY = """SELECT * FROM pacientes"""

cur.execute(SQL_QUERY)

#data = cur.fetchone() # <- Trae un dato
data = cur.fetchall() # <- Trae todos los datos
#data = cur.fetchmany(3) # <- Trae los primeros n datos
print(data)


comn.close()

#%% --------------------------------------------------------------


import sqlite3

comn = sqlite3.connect("database.db")
cur = comn.cursor()

SQL_QUERY = """SELECT * FROM pacientes"""

cur.execute(SQL_QUERY)

for data in cur: # equivalente a cur.fetchone
    print("ID:{:<3} NOMBRE {:16} PESO: {:3}Kg ALTURA: {:.2f} m".format(data))


comn.close()
#%%----------------------------------------------------------------------------

#Insertar registros

import sqlite3

comn = sqlite3.connect("database.db")
cur = comn.cursor()

SQL_QUERY = """SELECT * FROM pacientes WHERE peso < 60 AND altura > 1.60"""
cur.execute(SQL_QUERY)
data = cur.fetchall()
print(data)

SQL_QUERY = """SELECT nombre, peso, altura FROM pacientes WHERE nombre LIKE '%eL%'"""
cur.execute(SQL_QUERY)
data = cur.fetchall()
print(data)

SQL_QUERY = """SELECT nombre, altura FROM pacientes WHERE altura > ?"""
cur.execute(SQL_QUERY, (1.70,))
data = cur.fetchall()
print(data)

comn.close()

#%%----------------------------------------------------------------

import sqlite3

comn = sqlite3.connect("database.db")
cur = comn.cursor()

SQL_QUERY = """UPDATE pacientes SET peso = ? WHERE id_pac = ?"""
cur.execute(SQL_QUERY,(88,5))

comn.commit()
comn.close()

#%%----------------------------------------------------------------

import sqlite3

comn = sqlite3.connect("database.db")
cur = comn.cursor()

SQL_QUERY = """DELETE FROM pacientes WHERE id_pac = ?"""
cur.execute(SQL_QUERY,(1,))

comn.commit()
comn.close()
#%%----------------------------------------------------------------
conn = sqlite3.connect("database.db")

# Se crea un cursor para poder acceder a la informacion
cur = conn.cursor()

# Se ejecuta una accion sobre la base de datos
print("------- SE ELIMINA REGISTRO ID 4 --------\n")
cur.execute("DELETE FROM pacientes WHERE id_pac = ?", (4,))
cur.execute("UPDATE pacientes SET peso = ? WHERE id_pac = ?", (0, 1))

# Consulta
cur.execute("SELECT * FROM pacientes")
for data in cur:
    print("ID: {:<3} Nombre: {:16} Peso: {:3}kg      Altura:{:.2f}m".format(*data))

print()
    
# Se deshace la ultima transaccion
conn.rollback()
print("------- ROLLBACK --------\n")

# Consulta
cur.execute("SELECT * FROM pacientes")
for data in cur:
    print("ID: {:<3} Nombre: {:16} Peso: {:3}kg      Altura:{:.2f}m".format(*data))

# Se cierra la conexion con la base de datos
conn.close()

#%%---------------------------------------------------------------------------------------------------------------
import sqlite3
try:
    comn = sqlite3.connect("database.db")
    cur = comn.cursor()

    SQL_QUERY = """INSERT INTO pacientes (id_pac, nombre, peso, altura) VALUES (?, ?, ?, ?)"""
    cur.execute(SQL_QUERY,(1, "Dina Mita", 120, 1.55))

    comn.commit()
except sqlite3.IntegrityError :
    comn.rollback()
    print("ERROR: El 'id ya existe en el registro. Los campos no se guardan")

finally:
    comn.close()

#%% -----------------------------------------------------------------------------------------------------------
comn = sqlite3.connect("database.db")

with comn:
    cur = comn.cursor()
    SQL_QUERY = """SELECT * FROM pacientes WHERE altura > 1.70"""

    for data in cur.execute(SQL_QUERY):
        print(data)

conn.close()
#%%--------------------------------------------------------------------------------------------------------------
import sqlite3

class Database:
    filename = "database.db"
    def __init__(self):
        self.comn = sqlite3.connect(Database.filename)
        self.cur = self.comn.cursor()

    def __del__(self):
        self.comn.close()

    def listar_pacientes(self):
        return self.cur.execute("SELECT * FROM pacientes").fetchall()

    def paciente_id(self, id_pac):
        return self.cur.execute("SELECT nombre, peso, altura FROM pacientes WHERE id = ?",
                                                                (id_pac)).fetchone()

    def nombres_pacientes(self, order='asc'):
        if order == 'asc':
            self.cur.execute("SELECT nombres FROM pacientes ORDER BY nombre")
        elif order == 'desc':
            self.cur.execute("SELECT nombres FROM pacientes ORDER BY nombre DESC")
        else:
            raise ValueError("El attr 'order' puede ser 'asc p 'desc")
        
        return [item[0] for item in self.cur]
#%%----------------------------------------------------------------
from db_pacientes import Database
db = Database()

for idx, item in enumerate(db.listar_pacientes(),start = 1):
    print(f"{idx} - {item}")

else:
    print()
#%%------------------------------------------------------------------------------
import tkinter as tk
import tkinter.ttk as ttk
from db_pacientes import Database

class App:
    def __init__(self, master):
        self.master = master
        self.master.title = "Tk dB App"
        self.dB = Database()

        self.varNombre = tk.StringVar()
        self.varPeso = tk.StringVar()
        self.varAltura = tk.StringVar()

        frm = tk.Frame(self.master)
        frm.pack(padx=10, pady=10)

        frm1 = tk.Frame(frm)
        frm1.pack(padx=10, pady=10, anchor = tk.N)
        frm2 = tk.Frame(frm)
        frm2.pack(padx=10, pady=10)

        self.cboNombres = ttk.Combobox(frm1, value = self.dB.nombres_pacientes())
        self.cboNombres.grid(row=0, column=0, padx=5, pady=5)

        self.lblNombre = tk.Label(frm2, text="Nombre")
        self.lblPeso = tk.Label(frm2, text="Peso")
        self.lblAltura = tk.Label(frm2, text="Altura")
        self.EntNombre = tk.Entry(frm2, textvariable=self.varNombre, state = 'disable')
        self.EntPeso = tk.Entry(frm2, textvariable=self.varPeso, state = 'disable')
        self.EntAltura = tk.Entry(frm2, textvariable=self.varAltura, state = 'disable')

        self.lblNombre.grid(row = 0, column = 0, padx=5, pady=5,sticky=tk.W)
        self.lblPeso.grid(row = 1, column = 0, padx=5, pady=5,sticky=tk.W)
        self.lblAltura.grid(row = 2, column = 0, padx=5, pady=5,sticky=tk.W)
        self.EntNombre.grid(row = 0, column = 1, padx=5, pady=5,sticky=tk.W)
        self.EntPeso.grid(row = 1, column = 1, padx=5, pady=5,sticky=tk.W)
        self.EntAltura.grid(row = 2, column = 1, padx=5, pady=5,sticky=tk.W)

        self.cboNombres.bind("<<ComboboxSelected>>", self.name_selected)

    def name_selected(self,event):
        nombre = self.cboNombres.get()
        peso, altura = self.dB.data_imc(nombre)

        self.varNombre.set(nombre)
        self.varPeso.set(peso)
        self.varAltura.set(altura)

    
root =tk.Tk()
app = App(root)
root.mainloop()
#%%----------------------------------------------------------------
class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Main Window")
        self.master.geometry("400x200+100+100")

        btn = tk.Button(self.master, text = "Otra ventana"
                        , command = self.__open__other_window)
        btn.pack(padx=20, pady=80)

    def __open__other_window(self):
        window = tk.Toplevel(self.master)
        OtherWindow(window)

class OtherWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Main Window")
        self.master.geometry("400x200+100+100")
        self.master.focus()
        self.master.grab_set()
        btn = tk.Button(self.master, text = "   Salir  ", command = self.master.destroy)
        btn.pack(padx=20, pady=80)

root =tk.Tk()
app = MainWindow(root)
root.mainloop()
#%%---------------------------------------------------------------------------
#Mejoras en el treeview
import tkinter as tk
import tkinter.ttk as ttk
from db_pacientes import Database

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Tabla de Datos")
        self.dB = Database()
        
        style = ttk.Style()
        style.theme_use('default')

        style.configure("Treeview")
        style.map("Treeview", background = [('selected','blue')])

        frm = tk.Frame(self.master)
        frm.pack(padx=10, pady=10)
        
        self.table = ttk.Treeview(frm, columns=(1, 2))
        self.table.pack()
        
        data = self.dB.data_pacientes()
        
        self.table.heading("#0", text="Nombre")
        self.table.heading("#1", text="Peso [kg]")
        self.table.heading("#2", text="Altura [m]")
        
        self.table.column("#0", width=120, minwidth=120, stretch=tk.NO)
        self.table.column("#1", width=80, minwidth=80, stretch=tk.NO)
        self.table.column("#2", width=80, minwidth=80, stretch=tk.NO)
        
        self.table.tag_configure('par', background = "#a3a3c2")
        self.table.tag_configure('impar', background = "#f0f0f5")


        for idx,item in enumerate(data):
            if idx % 2 == 0:
                self.table.insert("", tk.END, text=item[0], values=item[1:], tags = ('par',))
            else:
                self.table.insert("", tk.END, text=item[0], values=item[1:], tags = ('impar',))
        
        self.table.bind("<<TreeviewSelect>>", self.print_selected)
        
    def print_selected(self, event):
        idx = self.table.selection()
        print(self.table.item(idx))   # Completar con keys de dict
        
        
root = tk.Tk()
app = App(root)
root.mainloop()