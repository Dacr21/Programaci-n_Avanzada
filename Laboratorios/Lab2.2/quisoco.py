#%%
import tkinter as tk
import time
import cv2
from PIL import Image, ImageTk
from tkinter.filedialog import asksaveasfilename
from datetime import datetime

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quisoco")
        self.resizable(0,0)
        
        #Parametros
        self.protocol("WM_DELETE_WINDOW", self.close_app)
        self.cap = cv2.VideoCapture(0)
        self.width = 640
        self.height = 360
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.eye_cascada = cv2.CascadeClassifier("haarcascade_eye.xml")
        self.num_ojos_pas = 0
        self.guino = False

        self.frmVideo = tk.Frame(self)
        self.frmVideo.pack(side = tk.TOP)

        self.frmStatus = tk.Frame(self,bd = 1, relief= tk.SUNKEN)
        self.frmStatus.pack(side = tk.BOTTOM, fill = tk.X)

        self.statusBar = tk.Label(self.frmStatus, text = "Detectando Rostro ...")
        self.statusBar.pack(side=tk.LEFT, fill=tk.X)

        #Videos
        self.Video = tk.Canvas(self.frmVideo,width=self.width, height=self.height, borderwidth=1, relief=tk.SUNKEN)
        self.Video.pack()

        self.grabacion()
    
    def grabacion(self):
        ret, frame = self.cap.read()    
        if ret:
            #Redimencionamiento
            frame = cv2.resize(frame, (self.width, self.height))
            #Deteccion de rostro
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for x,y,w,h in faces:
                cv2.rectangle(frame, (x,y), (w+x,h+y), (255,0,0), 2)
                #Delimitar a cara
                gray_eye = gray[y:y+h,x:x+w]
                #Buscar ojos
                ojos = self.eye_cascada.detectMultiScale(gray_eye, 1.1, 20)

                for x1,y1,w1,h1 in ojos:
                    cv2.rectangle(frame, (x1+x,y1+y), (w1+x1+x,h1+y1+y), (0,0,255), 2)

                num_ojos_pre = len(ojos)

                #Si existe variacion de numero de ojos, se reconoce como guiño y toma foto
                if self.num_ojos_pas == 2 and num_ojos_pre == 1:
                    t,frameOri = self.cap.read()
                    filename = f"{datetime.strftime(datetime.now(), '%Y%m%d_%H%M')}.jpg"
                    self.guino = True
                    if t:
                        cv2.imwrite(filename, frameOri)
                        PhotoWindow(filename)
                    
                if num_ojos_pre == 2 and self.guino:
                    self.guino = False

                self.num_ojos_pas = num_ojos_pre
            #Mientras se detecta el rostro, pero no hay guino
            if len(faces) == 1 and self.guino == False:
                self.statusBar.config(text = "Rostro Detectado")
            #Si detecta varias caras
            elif len(faces) > 1:
                self.statusBar.config(text = "Una persona a la vez PORFAVOR")
            #Si detecta y se mantiene el guino
            elif self.guino and len(faces) > 0:
                self.statusBar.config(text = "Imagen capturada")
            #Si no se detecta cara
            else:
                self.statusBar.config(text = "Detectando Rostro ...")

            #Paso a RGB
            Color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            #Mostrar frame
            try: 
                photo = ImageTk.PhotoImage(image=Image.fromarray(Color))
                self.Video.create_image(0,0,image=photo,anchor='nw')
                self.Video.image = photo
            except:
                pass
        self.after(20,self.grabacion)

    def close_app(self):
        if self.cap.isOpened():
            self.cap.release()
        self.destroy()

class PhotoWindow(tk.Toplevel):
    def __init__(self, filename):
        super().__init__()
        self.title("Resultado")
        self.resizable(0,0)

        self.grab_set()
        self.focus()

        width = 640
        height = 360

        canvas = tk.Canvas(self, width=width, height=height, borderwidth=1,
                relief=tk.SUNKEN, bg='white')
        canvas.pack()

        self.frmStatus = tk.Frame(self,bd = 1, relief= tk.SUNKEN)
        self.frmStatus.pack(side = tk.BOTTOM, fill = tk.X)

        self.statusBar = tk.Label(self.frmStatus, text = "Imagen Capurada")
        self.statusBar.pack(side=tk.LEFT, fill=tk.X)

        cv_img = cv2.imread(filename, cv2.IMREAD_COLOR)
        cv_img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        cv_img_re = cv2.resize(cv_img_rgb,(width, height))

        try:
            photo = ImageTk.PhotoImage(image=Image.fromarray(cv_img_re))
            canvas.create_image(0, 0,image=photo,anchor='nw')
            canvas.image = photo
        except:
            pass

App().mainloop()