#%%
import tkinter as tk
from tkinter.constants import FALSE
import numpy as np
import matplotlib.pyplot as plt
import tkinter.ttk as ttk
import psutil
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
%matplotlib inline

class Ventana:
        def __init__(self, master):
        # Propiedades de la ventana
                self.master = master
                self.master.title("Monitor de recursos")
                self.master.resizable(0,0)

        # Espacio
                frm = tk.Frame(self.master, bg = '#0A5CB4')
                frm.pack()

                self.frmMedidas = tk.Frame(frm, bg = '#0A5CB4')
                self.frmMedidas.pack(side = tk.LEFT,padx = 10, pady = 10, fill = tk.BOTH)

                self.CPU = tk.Frame(self.frmMedidas, bg = '#0A5CB4')
                self.CPU.pack(padx=10, pady=10, fill = tk.X)
                self.RAM = tk.Frame(self.frmMedidas, bg = '#0A5CB4')
                self.RAM.pack(padx=10, pady=10, fill = tk.X)
                self.HDD = tk.Frame(self.frmMedidas, bg = '#0A5CB4')
                self.HDD.pack(padx=10, pady=10, fill = tk.X)

                self.frmGrafico = tk.Frame(frm, bg = '#0A5CB4')
                self.frmGrafico.pack(side = tk.LEFT,padx = 10, pady = 10, fill = tk.BOTH)

                self.frmStatus = tk.Frame(self.master,bd = 1, relief= tk.SUNKEN, bg = '#33C8B1')
                self.frmStatus.pack(side = tk.BOTTOM, fill = tk.X)
                
        #Variables
                # tasa de uso de cpu
                self.cup_per = psutil.cpu_percent()
                # Información de la memoria
                self.memory_info = psutil.virtual_memory()   
                # Información del disco duro
                self.disk_info = psutil.disk_usage("/") # Información del disco del directorio raíz    
                # Información de Internet
                self.net_info = psutil.net_io_counters()    
                # Obtener la hora actual del sistema
                self.current_time = datetime.datetime.now().strftime("%F %T") #% F año mes día% T hora, minuto y segundo
                #Frecuencia
                self.time = 800 #Recomendable que el valor sea menor a 1000 milisegundos
                #Valores presentes y pasados de uso de CPU
                self.lista = np.zeros(100) + self.cup_per
                #Fuente
                self.fuente = 'Arial 12 bold'
                #Largo de progressbar
                self.largo = 300
                
        # Objetos
        #frmMedidas
        # Información de CPU
                self.Info1 = tk.Label(self.CPU, text =f"CPU usage ({psutil.cpu_count(logical=False)} core): {self.cup_per}%", font= self.fuente
                , bg = '#0A5CB4', fg = 'white')
                self.Info1.pack(anchor = tk.W, padx = 10, pady = 5)

                self.Porce1 = ttk.Progressbar(self.CPU, orient= tk.HORIZONTAL, length = self.largo, value=self.cup_per)
                self.Porce1.pack(anchor = tk.W, padx = 10, pady = 5)

        #Información de la memoria RAM
                self.Info2 = tk.Label(self.RAM, text = f"RAM usage (Total: {self.memory_info.total/1024/1024/1024:.2f} Gb): {self.memory_info.percent}%", font= self.fuente
                , bg = '#0A5CB4', fg = 'white')
                self.Info2.pack(anchor = tk.W, padx = 10, pady = 5)

                self.Porce2 = ttk.Progressbar(self.RAM, orient= tk.HORIZONTAL, length = self.largo, value=self.memory_info.percent)
                self.Porce2.pack(anchor = tk.W, padx = 10, pady = 5)

        # Información del disco duro
                self.Info3 = tk.Label(self.HDD, text = f"HDD Usage (Total: {self.disk_info.total/1024/1024/1024:.2f} Gb): {self.disk_info.percent}%", font= self.fuente
                , bg = '#0A5CB4', fg = 'white')
                self.Info3.pack(anchor = tk.W, padx = 10, pady = 5) 

                self.Porce3 = ttk.Progressbar(self.HDD, orient= tk.HORIZONTAL, length = self.largo, value=self.disk_info.percent)
                self.Porce3.pack(anchor = tk.W, padx = 10, pady = 5)     

        #frmGrafico
        #Grafico
                self.fig, self.ax = plt.subplots(figsize=(6, 4), facecolor='#0A5CB4')
                self.muestras = np.arange(0,100,1)
                y = self.lista
                self.linea, = self.ax.plot(self.muestras, y, color= 'c', linewidth = 5)
                self.ax.grid(color = 'w')
                self.ax.get_xaxis().set_visible(FALSE)
                self.ax.set_xlim([0, 100])
                self.ax.set_ylim(0,100)
                self.ax.set_title("CPU Usage [%]", fontname = 'Arial', fontsize = 20, color = 'w')
                self.ax.set_facecolor('#0A5CB4')
                plt.yticks(color = 'w')
                self.ax.spines['bottom'].set_color('w')
                self.ax.spines['left'].set_color('w')
                self.ax.spines['right'].set_color('w')
                self.ax.spines['top'].set_color('w')
                self.ax.tick_params(axis = 'both', color = 'w')

                self.grafica = FigureCanvasTkAgg(self.fig, master = self.frmGrafico)
                self.grafica.get_tk_widget().pack(expand=True, fill=tk.BOTH)

        #Status Barr

                self.statusbarInfo = tk.Label(self.frmStatus, text=f"Net Info: [in: {self.net_info.bytes_recv} | {self.net_info.bytes_sent}]", anchor=tk.W
                , bg = '#33C8B1', fg = 'white')
                self.statusbarInfo.pack(side=tk.LEFT, fill=tk.X)

                self.statusbarFecha = tk.Label(self.frmStatus, text=self.current_time, anchor=tk.E, bg = '#33C8B1', fg = 'white')
                self.statusbarFecha.pack(side=tk.RIGHT, fill=tk.X)

        #Bucle
                self.Datos()
                self.Tiempo()

        #Funciones
        def Datos(self):
        #Actualizar datos
                self.cup_per = psutil.cpu_percent()
                self.memory_info = psutil.virtual_memory()   
                self.disk_info = psutil.disk_usage("/")
                self.net_info = psutil.net_io_counters()
                self.lista = np.append(self.lista,self.cup_per)
                self.lista = np.delete(self.lista,0)

        #Actualizar vista
        #Info
                self.Info1.config(text =f"CPU usage ({psutil.cpu_count(logical=False)} core): {self.cup_per}%")
                self.Porce1.config(value=self.cup_per)
                self.Info2.config(text = f"RAM usage (Total: {self.memory_info.total/1024/1024/1024:.2f} Gb): {self.memory_info.percent}%")
                self.Porce2.config(value=self.memory_info.percent)
                self.Info3.config(text = f"HDD Usage (Total: {self.disk_info.total/1024/1024/1024:.2f} Gb): {self.disk_info.percent}%")
                self.Porce3.config(value=self.disk_info.percent)
        #Grafica
                self.linea.set_ydata(self.lista)
                self.grafica.draw()
        #Statusbar
                self.statusbarInfo.config(text=f"Net Info: [in: {self.net_info.bytes_recv} | {self.net_info.bytes_sent}]")

                self.master.after(self.time,self.Datos)

        def Tiempo(self):
                self.current_time = datetime.datetime.now().strftime("%F %T")
                self.statusbarFecha.config(text= self.current_time)
                self.master.after(1000,self.Tiempo)

root = tk.Tk()
Ventana(root)
root.mainloop()
