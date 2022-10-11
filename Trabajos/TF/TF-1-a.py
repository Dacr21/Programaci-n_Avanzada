#%%
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
import serial.tools.list_ports
import serial
import threading
import time
class SerialChat:
    def __init__(self, master):
        self.master = master
        #Buscar puertos y ponerlos en una lista
        ports =  serial.tools.list_ports.comports()
        self.lis = []
        for port in ports:
            idx = str(port).find(' ')
            puerto = str(port)[0:idx]
            self.lis.append(puerto)
        
        self.master.title(f"Serial Chat")
        self.master.geometry("+50+50")
        self.master.resizable(0, 0)
        #Indicador de cierre

        self.cierre = False
        # ---------------------- SERIAL PORT --------------------------
        self.serial = None
        
        # ------------------------ FRAMES -----------------------------
        frm1 = tk.LabelFrame(self.master, text="Conexion")
        frm2 = tk.Frame(self.master)
        frm3 = tk.LabelFrame(self.master, text="Enviar mensaje")
        frm1.pack(padx=5, pady=5, anchor=tk.W)
        frm2.pack(padx=5, pady=5, fill='y', expand=True)
        frm3.pack(padx=5, pady=5)
        
        # ------------------------ FRAME 1 ----------------------------
        self.lblCOM = tk.Label(frm1, text="Puerto COM:") 
        self.cboPort = ttk.Combobox(frm1, values=self.lis)
        self.lblSpace = tk.Label(frm1, text="")
        self.btnConnect = ttk.Button(frm1, text="Conectar", width=16, command = self.Conectar)
        self.lblCOM.grid(row=0, column=0, padx=5, pady=5)
        self.cboPort.grid(row=0, column=1, padx=5, pady=5)
        self.lblSpace.grid(row=0,column=2, padx=30, pady=5)
        self.btnConnect.grid(row=0, column=3, padx=5, pady=5)
        
        # ------------------------ FRAME 2 ---------------------------
        self.txtChat = ScrolledText(frm2, height=25, width=50, wrap=tk.WORD, state='disable')
        self.txtChat.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
                
        # ------------------------ FRAME 3 --------------------------
        self.lblText = tk.Label(frm3, text="Texto:")
        self.inText = tk.Entry(frm3, width=45, state='disable')
        self.btnSend = ttk.Button(frm3, text="Enviar", width=12, state='disable', command = self.Envio1)
        self.lblText.grid(row=0, column=0, padx=5, pady=5)
        self.inText.grid(row=0, column=1, padx=5, pady=5)
        self.btnSend.grid(row=0, column=2, padx=5, pady=5)
               
        # --------------------------- StatusBar -----------------------
        self.statusBar = tk.Label(self.master, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)
            
        # ------------- Control del boton "X" de la ventana -----------
        self.master.protocol("WM_DELETE_WINDOW", self.cerrar_puertos)

        #Eventos
        self.inText.bind('<Return>', self.Envio)

    def Tex_Envio(self):
        self.statusBar.config(text = "Enviando mensaje ...")
        time.sleep(1)
        self.statusBar.config(text = f"Conectando al {self.PORT_FIN} a 9600")

    def Tex_Recivido(self):
        self.statusBar.config(text = "Recibiendo mensaje ...")
        time.sleep(1)
        self.statusBar.config(text = f"Conectando al {self.PORT_FIN} a 9600")

    def Lectura(self):
        while True:
            if self.ser.in_waiting > 0:
                    funcion2 = threading.Thread(target=self.Tex_Recivido, daemon=True)
                    funcion2.start()
                    # Se leen los datos y esperar al caracter EOL
                    data = self.ser.readline()
                    #La data recibida son bytes y hay que convertirlos
                    string = data.decode('utf-8')
                    self.txtChat.config(state = 'normal')
                    self.txtChat.insert(tk.INSERT, string, 'rojo')
                    self.txtChat.see("end")
                    self.txtChat.config(state = 'disable')
            elif self.cierre == True:
                break
    
    def Conectar(self):
        self.cierre = False
        #Activar todo
        self.PORT_FIN = self.cboPort.get()

        self.txtChat.tag_config('rojo', foreground='red')
        self.txtChat.tag_config('verde', foreground='green')
        try:
            #Establecer conexion con el purto serial
            self.statusBar.config(text = f"Conectando al {self.PORT_FIN} a 9600")
            self.ser = serial.Serial(port = self.PORT_FIN,
                                baudrate = 9600,
                                bytesize = 8,
                                stopbits=serial.STOPBITS_ONE)
            self.statusBar.config(text = f"Conectado al {self.PORT_FIN} a 9600")
            #Aviso de coneccion
            string = f"{self.PORT_FIN} SE HA CONECTADO"+'\n'
            data = string.encode("utf-8")
            self.ser.write(data)
            #Preparar para conexion
            self.btnSend.config(state = 'normal')
            self.inText.config(state = 'normal')
            self.cboPort.config(state = 'disable')
            self.btnConnect.config(text = 'Desconectar', command = self.Desconectar)
            #Lectura de entrada
            funcion1 = threading.Thread(target=self.Lectura, daemon=True)
            funcion1.start()
        except:
            self.statusBar.config(text = f"Error al conectar a {self.PORT_FIN}")
            
    def Desconectar(self):
        #Cierre de los bucles
        self.cierre = True
        #Aviso de desconeccion
        string = f"{self.PORT_FIN} SE HA DESCONECTADO"+'\n'
        data = string.encode("utf-8")
        self.ser.write(data)
        #Desconectar
        self.ser.close()
        #Predeterminado
        self.btnConnect.config(text = 'Conectar', command = self.Conectar)
        self.statusBar.config(text = "")
        self.btnSend.config(state = 'disable')
        self.inText.config(state = 'disable')
        self.cboPort.config(state = 'normal')


    def Envio(self,event):
        funcion3 = threading.Thread(target=self.Tex_Envio, daemon = True)
        funcion3.start()
        #Estraccion de datos
        string = f"[{self.PORT_FIN}] "+self.inText.get()+'\n'
        self.inText.delete(0,'end')
        self.txtChat.config(state = 'normal')
        self.txtChat.insert(tk.INSERT, string, 'verde')
        self.txtChat.config(state = 'disable')
        self.txtChat.see("end")
        data = string.encode("utf-8")
        self.ser.write(data)
    
    def Envio1(self):
        funcion3 = threading.Thread(target=self.Tex_Envio, daemon = True)
        funcion3.start()
        #Estraccion de datos
        string = f"[{self.PORT_FIN}] "+self.inText.get()+'\n'
        self.inText.delete(0,'end')
        self.txtChat.config(state = 'normal')
        self.txtChat.insert(tk.INSERT, string, 'verde')
        self.txtChat.config(state = 'disable')
        self.txtChat.see("end")
        data = string.encode("utf-8")
        self.ser.write(data) 

    def cerrar_puertos(self):
        # Se cierran los puertos COM y la ventana de tkinter
        try:
            self.cierre = True
            self.ser.close()
        except:
            pass

        self.master.destroy()
    
    
root = tk.Tk()
app = SerialChat(root)
root.mainloop()