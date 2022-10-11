#%%
import tkinter as tk
from tkinter.constants import BOTTOM, W
import tkinter.ttk as ttk
from typing_extensions import IntVar

class Cal_color:
    def __init__(self, master):
        #TK
        self.master = master
        self.master.resizable(0,0)
        self.master.title("MI APP")
        #Propio
        alumnos = ["1" , "2", "3", "4"]
        self.var_color = tk.IntVar()
        #Distribucion de espacios
        #Universo
        fr = tk.Frame(self.master)
        fr.pack(padx=10, pady=10)
        #Planetas
        fr1 = tk.LabelFrame(fr, text = "Color de letra")
        fr2 = tk.LabelFrame(fr, text="Tamaño de letra")
        fr1.pack(padx=5,pady=5, side = BOTTOM)
        fr2.pack(padx=5,pady=5)
        #fr
        #Poblacion
        self.lblNombre = tk.Label(fr, text="Nombres:")
        self.coboNombres = ttk.Combobox(fr, values=alumnos, state='readonly', width=40)
        #Direccion
        self.lblNombre.pack(padx = 10, pady=10)
        self.coboNombres.pack(padx = 10, pady=10)
        #fr1
        #Poblacion
        self.rdoNegro = tk.Radiobutton(fr1, text="Negro", variable=self.var_color, value=0)
        self.rdoAzul = tk.Radiobutton(fr1, text="Azul", variable=self.var_color, value=1)
        self.rdoRojo = tk.Radiobutton(fr1, text="Rojo", variable=self.var_color, value=2)
        #Direccion
        self.rdoNegro.grid(row=0, column=0, padx=5, pady=5)
        self.rdoAzul.grid(row=0, column=1, padx=5, pady=5)
        self.rdoRojo.grid(row=0, column=2, padx=5, pady=5)
        #fr2
        #Poblacion
        
        #Direccion
        

root = tk.Tk()
app = Cal_color(root)
root.mainloop()

#%%
