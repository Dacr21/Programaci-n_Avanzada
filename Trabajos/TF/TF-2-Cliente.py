#%%
import socket
import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
import time


class Cliente(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chat Server")
        self.geometry("+50+50")
        self.resizable(0, 0)

        HOST = "192.168.0.100"
        PORT = 54321
        Username = "USER"
        self.HEADER_SIZE = 5
        self.Cierre = False

        #Frames
        fr1 = tk.LabelFrame(self,text = "Conexion")
        fraux2 = tk.Frame(self)
        fr2 = tk.LabelFrame(fraux2,text = "Usuarios Conectados")
        fraux1 = tk.LabelFrame(fraux2,text = "Chat Grupal")
        fr3 = tk.Frame(fraux1)
        fr4 = tk.LabelFrame(fraux1,text = "Enviar mensaje")
        fr1.pack(padx=5, pady=5, side=tk.TOP, fill = tk.X)
        fraux2.pack(padx=5, pady=5)
        fr2.pack(padx=5, pady=5, side = tk.RIGHT, anchor = tk.N)
        fraux1.pack(padx=5, pady=5, side = tk.LEFT, anchor = tk.N)
        fr3.pack(padx=5, pady=5, side = tk.TOP)
        fr4.pack(padx=5, pady=5, side = tk.BOTTOM)
        #Elementos
        #Fr1
        self.Lbl1 = tk.Label(fr1, text="HOST")
        self.EHost = tk.Entry(fr1)
        self.EHost.insert(tk.INSERT,HOST)
        self.Lbl2 = tk.Label(fr1, text="PORT")
        self.EPort = tk.Entry(fr1)
        self.EPort.insert(tk.INSERT,PORT)
        self.Lbl3 = tk.Label(fr1, text="USERNAME")
        self.EUserName = tk.Entry(fr1)
        self.EUserName.insert(tk.INSERT,Username)
        self.BtnConnect = tk.Button(fr1,text = "Conectar", command = self.conectar)

        self.Lbl1.grid(row=0, column=0, padx=5, pady=5)
        self.EHost.grid(row=0, column=1, padx=5, pady=5)
        self.Lbl2.grid(row=0, column=2, padx=5, pady=5)
        self.EPort.grid(row=0, column=3, padx=5, pady=5)
        self.Lbl3.grid(row=0, column=4, padx=5, pady=5)
        self.EUserName.grid(row=0, column=5, padx=5, pady=5)
        self.BtnConnect.grid(row=0, column=6, padx=5, pady=5)
        #Fr2
        self.UserList = ScrolledText(fr2,height=20, width=25, wrap=tk.WORD, state='disable')
        self.UserList.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        #Fr3
        self.ChatText = ScrolledText(fr3,height=15, width=45, wrap=tk.WORD, state='disable')
        self.ChatText.grid(row=0, column=0, columnspan=3, padx=5, pady=8)
        #Fr4
        self.Lbl4 = tk.Label(fr4,text="Texto")
        self.EText = tk.Entry(fr4,width=45, state='disable')
        self.BtnEnvio = tk.Button(fr4,text="Envio", command=self.Envio)
        self.Lbl4.grid(row=0,column=0,padx=5, pady=5)
        self.EText.grid(row=0,column=1,padx=5, pady=5)
        self.BtnEnvio.grid(row=0,column=2,padx=5, pady=5)


        self.StatusBar = tk.Label(self,bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.StatusBar.pack(side=tk.BOTTOM, fill=tk.X)

        self.protocol("WM_DELETE_WINDOW", self.cerrar)

        #Eventos
        self.EText.bind('<Return>', self.Envio1)

    def conectar(self):
        try:
            self.Cierre = False
            self.Direccion = self.EHost.get()
            self.Puerto = self.EPort.get()
            self.Nombre = self.EUserName.get()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.Direccion, int(self.Puerto)))
            self.StatusBar.config(text = "Conectado con el servidor")
            self.th=threading.Thread(target=self.Lectura, daemon=True)
            self.th.start()

            #Envio de nombre de usuario
            comand_Code = 'US'
            data_len = len(self.Nombre)
            self.sock.send(f"{comand_Code}{data_len:<{self.HEADER_SIZE}}{self.Nombre}".encode('utf-8'))

            self.EText.config(state = 'normal')
            self.BtnEnvio.config(state = 'normal')
            self.BtnConnect.config(text = "Desconectar", command = self.desconectar)
            self.EHost.config(state = 'disable')
            self.EPort.config(state = 'disable')
            self.EUserName.config(state = 'disable')
        except:
            self.StatusBar.config(text = "Servidor no encontrado")
    
    def desconectar(self):
        self.EText.config(state = 'disable')
        self.BtnEnvio.config(state = 'disable')
        self.BtnConnect.config(text = "Conectar", command = self.conectar)
        self.EHost.config(state = 'normal')
        self.EPort.config(state = 'normal')
        self.EUserName.config(state = 'normal')

        #Borrar listas
        self.UserList.config(state = 'normal')
        self.UserList.delete("1.0", "end")
        self.UserList.config(state = 'disable')

        self.ChatText.config(state = 'normal')
        self.ChatText.delete("1.0", "end")
        self.ChatText.config(state = 'disable')

        #Borrar texto
        self.EText.delete(0,'end')

        try:
            self.sock.close()
        except:
            pass

    def Lectura(self):
        while True:
            try:
                comand_code = self.sock.recv(2)
                if comand_code == b'TX':
                    data_header = self.sock.recv(self.HEADER_SIZE)
                    if not data_header:
                        break
                    data = self.sock.recv(int(data_header)).decode('utf-8')
                    data = data + '\n'
                    self.ChatText.config(state = 'normal')
                    self.ChatText.insert(tk.INSERT, data)
                    self.ChatText.see("end")
                    self.ChatText.config(state = 'disable')

                elif comand_code == b'CC':
                    self.th1=threading.Thread(target=self.Mensaje_Repetido, daemon=True)
                    self.th1.start()
                    self.desconectar()

                elif comand_code == b'CL':
                    self.UserList.config(state = 'normal')
                    self.UserList.delete("1.0", "end")
                    self.UserList.config(state = 'disable')

                elif comand_code == b'US':
                    data_header = self.sock.recv(self.HEADER_SIZE)
                    data = self.sock.recv(int(data_header)).decode('utf-8')
                    data = data + '\n'
                    if not data_header:
                        break
                    self.UserList.config(state = 'normal')
                    self.UserList.insert(tk.INSERT, data)
                    self.UserList.see("end")
                    self.UserList.config(state = 'disable')

            except:
                try:
                    try:
                        self.th1.join()
                    except:
                        pass
                    th3=threading.Thread(target = self.Mensaje_desconeccion, daemon =True)
                    th3.start()
                    self.desconectar()
                except:
                    pass
                break

    def Envio(self):
        mensaje = self.EText.get()
        if mensaje == '':
            th2=threading.Thread(target = self.Mensaje_vacio, daemon =True)
            th2.start()
        else:
            self.EText.delete(0,'end')
            comand_Code = 'TX'
            data_len = len(mensaje + self.Nombre + '>')
            self.sock.send(f"{comand_Code}{data_len:<{self.HEADER_SIZE}}{self.Nombre}>{mensaje}".encode('utf-8'))

    def Envio1(self,event):
        mensaje = self.EText.get()
        if mensaje == '':
            th2=threading.Thread(target = self.Mensaje_vacio, daemon =True)
            th2.start()
        else:
            self.EText.delete(0,'end')
            comand_Code = 'TX'
            data_len = len(mensaje + self.Nombre + '>')
            self.sock.send(f"{comand_Code}{data_len:<{self.HEADER_SIZE}}{self.Nombre}>{mensaje}".encode('utf-8'))

    def Mensaje_Repetido(self):
        self.StatusBar.config(text = "Nombre de Usuario repetido")
        time.sleep(1)

    def Mensaje_vacio(self):
        self.StatusBar.config(text = "Escriba algo para enviar")
        time.sleep(1)
        self.StatusBar.config(text = "Conectado con el servidor")

    def Mensaje_desconeccion(self):
        self.StatusBar.config(text = "Conexion perdida")
        time.sleep(1)
        self.StatusBar.config(text = "")

    def cerrar(self):
        try:
            self.sock.close()
        except:
            pass
        self.destroy()

Cliente().mainloop()
   