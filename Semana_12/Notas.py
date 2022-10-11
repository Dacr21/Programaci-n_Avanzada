# _*_ coding: utf-8 -*-
#%%
import cv2
cv2.__version__
#%%
#DATA 1: OpenCV Colormap: BGR (no es RGB)
img = cv2.imread("img\\img1.jpg",1)
print(type(img))

#%%
print(img)

#%%
#DATA 2: OpenCV (Ancho - Alto) numpy (filas - columnas)
print("Size : ",img.shape)
print("Dim : ",img.ndim)
print(img.dtype)

#%%
cv2.imshow("Sample Img", img)
cv2.waitKey(0) #blocking function
cv2.destroyAllWindows()

#%%
#Redimensionar imagenes
resize_img = cv2.resize(img,(300,100))

print("Size : ",resize_img.shape)
print("Dim : ",resize_img.ndim)
print(resize_img.dtype)

#%%
cv2.imshow("Sample Img", resize_img)
cv2.waitKey(0) #blocking function
cv2.destroyAllWindows()

#%%
resize_img = cv2.resize(img, (int(img.shape[1]/1.5), int(img.shape[0]/1.5)))
cv2.imshow("Sample Img", resize_img)
cv2.waitKey(0) #blocking function
cv2.destroyAllWindows()

#%%
#Crear imagen
cv2.imwrite("img\\res_img.jpg", resize_img) 

#%%
# OpenCV + Matplotlib
# Escala de grises
import matplotlib.pyplot as plt
import cv2

cv_img = cv2.imread("img\\img1.jpg", cv2.IMREAD_COLOR)

plt.imshow(cv_img, interpolation='bicubic', cmap='gray')
plt.xticks([]); plt.yticks([])
plt.show()

#%%
#Escala de colores

import matplotlib.pyplot as plt
import cv2

cv_img = cv2.imread("img\\img1.jpg", cv2.IMREAD_COLOR)
cv_img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

plt.imshow(cv_img_rgb, interpolation='bicubic')
plt.xticks([]); plt.yticks([])
plt.show()

#%%
import tkinter as tk
from PIL import Image, ImageTk
import cv2

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OpenCV + tkinter")
        self.resizable(0,0)
        width, height = 600,400

        self.canvas = tk.Canvas(self, width=width, height=height, borderwidth=1,
        relief=tk.SUNKEN)
        self.canvas.pack()

        cv_img = cv2.imread("img\\img2.jpg")
        cv_img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        cv_img_re = cv2.resize(cv_img_rgb,(width, height))

        try:
            photo = ImageTk.PhotoImage(image=Image.fromarray(cv_img_re))
            self.canvas.create_image(0,0,image=photo, anchor='nw')
            self.canvas.image = photo
        except:
            pass
App().mainloop()

#%%
import tkinter as tk
import imageio
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showinfo, askokcancel
from PIL import Image, ImageTk
import cv2

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Photo Viewer")
        self.resizable(0,0)
        self.width, self.height = 640,480

        self.protocol("WM_DELETE_WINDOW", self.close_app)

        menu = tk.Menu(self)
        self.configure(menu=menu)

        menu_archivo = tk.Menu(menu, tearoff=False)
        menu_ayuda = tk.Menu(menu, tearoff=False)

        menu_archivo.add_command(label = "Abrir", command = self.open_img)
        menu_archivo.add_command(label = "Cerrar", command = self.close_img)
        menu_archivo.add_separator()
        menu_archivo.add_command(label = "Salir", command = self.close_app)

        menu_ayuda.add_command(label = "Acerca de ...", command = self.about)

        menu.add_cascade(label = "Archivo", menu=menu_archivo)
        menu.add_cascade(label = "Archivo", menu=menu_ayuda)

        self.canvas = tk.Canvas(self, width=self.width, height=self.height, borderwidth=1,
                                relief=tk.SUNKEN)
        self.canvas.pack()

    def open_img(self):
        filetypes = (("Imagenes",["*.gif","*.jpg"]),("Todos los archivos", "*.*"))
        filename = askopenfilename(filetypes=filetypes)

        if filename.endswith(".gif"):
            gif = imageio.mimread(filename)
            imgs = [cv2.cvtColor(img, cv2.BGR2RGB) for img in gif]
            cv_img = imgs[0]
        else:
            cv_img = cv2.imread(filename)

        
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        cv_img = cv2.resize(cv_img,(self.width, self.height))
        try:
            photo = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
            self.img_canvas = self.canvas.create_image(0,0,image=photo, anchor='nw')
            self.canvas.image = photo
        except:
            pass
    
    def close_img(self):
        self.canvas.delete(self.img_canvas)

    def about(self):
        showinfo("Acerca de ...", "Photo Viewer v1.2\n2021 Covid Times")

    def close_app(self):
        if askokcancel("Cerrar", "Desea cerrar la aplicacion"):
        # TODO: Si hay una img abierta, debe cerrarse
            self.destroy()
App().mainloop()

#%%
#Tomar fotos de la camara
import cv2

cap = cv2.VideoCapture(0)

while True:
  ret, frame = cap.read()
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   
  cv2.imshow("WebCam", frame)
  cv2.imshow("Gray Cam", gray)  

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()

#%%
#Conectar a celular
#OpenCV + DroidCam(Android)
import cv2

cap = cv2.VideoCapture('http://192.168.0.21/mjpegfeed?640x480')

while True:
  ret, frame = cap.read()
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   
  cv2.imshow("WebCam", frame)
  cv2.imshow("Gray Cam", gray)  

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()

#%%
import cv2

cap = cv2.VideoCapture(0)
codec = cv2.VideoWriter_fourcc(*"MP4V") #XVID
out = cv2.VideoWriter('img\\cam_out.mp4', codec, 20.0, (640,480))

while True:
  ret, frame = cap.read()
  out.write(frame)
   
  cv2.imshow("WebCam", frame) 

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
out.release()
cv2.destroyAllWindows()

#%%
import tkinter as tk
from PIL import Image, ImageTk
import cv2

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Webcam Monitor")
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.close_app)
        self.cap = cv2.VideoCapture(0)
        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.canvas = tk.Canvas(self, width=width, height=height, borderwidth=1,
                relief=tk.SUNKEN)
        self.canvas.pack()

        self.cam_loop()

    
    def cam_loop(self):
        ret, frame = self.cap.read()
        
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
            try:
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0,0,image=photo, anchor='nw')
                self.canvas.image = photo
            except:
                pass
        self.after(20,self.cam_loop)
    
    def close_app(self):
        if self.cap.isOpened():
            self.cap.release()
        self.destroy()
   
App().mainloop()

#%%
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from tkinter.filedialog import asksaveasfilename
from datetime import datetime

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multimedia Kiosk --Preview")
        self.resizable(0,0)
        
        self.protocol("WM_DELETE_WINDOW", self.close_app)
        self.cap = cv2.VideoCapture(0)
        self.width = 320
        self.height = 240

        self.codec = cv2.VideoWriter_fourcc(*"MP4V") #XVID
        self.recording = False

        frm = tk.Frame(self)
        frm1 = tk.LabelFrame(frm, text="Preview")
        frm2 = tk.LabelFrame(frm, text="Controls")

        frm.pack(padx=10, pady=10)
        frm1.pack(padx=10, pady=10)
        frm2.pack(padx=10, pady=10)
        
        
        #FRM1
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, borderwidth=1,
                relief=tk.SUNKEN)
        self.canvas.pack()
        #FRM2
        self.btnPhoto = tk.Button(frm2, text = "Take Picture", width = 16, command=self.take_pic)
        self.btnVideo = tk.Button(frm2, text = "Rec Video", width=16, command=self.rec_video)

        self.btnPhoto.grid(row=0, column=0, padx=5, pady=5)
        self.btnVideo.grid(row=0, column=1, padx=5, pady=5)
        self.cam_loop()

    
    def cam_loop(self):
        ret, frame = self.cap.read()    
        if ret:
            if self.recording:
                self.output_file.write(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.width, self.height))
        
            try:
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0,0,image=photo, anchor='nw')
                self.canvas.image = photo
            except:
                pass
        self.after(20,self.cam_loop)
    
    def close_app(self):
        if self.cap.isOpened():
            self.cap.release()
        self.destroy()

    def take_pic(self):
        #Capturar un frame
        ret, frame = self.cap.read()
        filename = f"{datetime.strftime(datetime.now(), '%Y%m%d_%H%M')}.jpg"
        if ret:
            cv2.imwrite(filename, frame)
            PhotoWindow(filename)

    def rec_video(self):
        if not self.recording:
            filename = asksaveasfilename(defaultextension="mp4", filetypes=[("Archivos de video", "*mp4")])
            
            if filename != '':
                self.output_file = cv2.VideoWriter(filename, self.codec, 20.0, (640, 480))
                self.recording = True
                self.btnVideo.config(text = "Stop recording")
        else:
            self.output_file.release()
            self.recording = False
            self.btnVideo.config(text = "Rec Video")

class PhotoWindow(tk.Toplevel):
    def __init__(self, filename):
        super().__init__()
        self.title("Multimedia Kiosk --Preview")
        self.resizable(0,0)

        self.grab_set()
        self.focus()

        width = 320
        height = 240


        canvas = tk.Canvas(self, width=width+20, height=height+20, borderwidth=1,
                relief=tk.SUNKEN, bg='white')
        canvas.pack()

        cv_img = cv2.imread(filename, cv2.IMREAD_COLOR)
        cv_img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        cv_img_re = cv2.resize(cv_img_rgb,(width, height))

        try:
            photo = ImageTk.PhotoImage(image=Image.fromarray(cv_img_re))
            canvas.create_image(width//2 + 13, height//2 + 13,image=photo)
            canvas.image = photo
        except:
            pass

App().mainloop()

#%%
import cv2

cv2.namedWindow("Image")
img = cv2.imread("img\\img2.jpg")

lin = cv2.line(img, pt1=(100,500), pt2=(600,500),
                color=(255,0,0), thickness=3)
rec = cv2.rectangle(img, pt1=(240,360), pt2=(300,450), color=(0,255,0), thickness=2)
cir = cv2.circle(img, center=(800,100), radius=60, color=(0,0,255), thickness=-1)

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#%%
import cv2

COLOR = (0,0,255) #Rojo
pt1 = (0,0)
pt2 = (0,0)
topLeft_clicked = False
botRight_clicked = False

def set_figure(event, x, y, flags, param):
    global pt1, pt2, topLeft_clicked, botRight_clicked

    if event == cv2.EVENT_LBUTTONDOWN:
        if topLeft_clicked and botRight_clicked:
            pt1 = (0, 0)
            pt2 = (0, 0)
            topLeft_clicked = False
            botRight_clicked = False
        
        if topLeft_clicked == False:
            pt1 = (x,y)
            topLeft_clicked = True

        elif botRight_clicked == False:
            pt2 = (x,y)
            botRight_clicked = True

cv2.namedWindow("WebCam")
cv2.setMouseCallback("WebCam", set_figure)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    #Dibujar rectangulo
    if topLeft_clicked:
        cv2.circle(frame, center=pt1, radius=1, color=COLOR, thickness=-1)

    if topLeft_clicked and botRight_clicked: 
        cv2.circle(frame, center=pt2, radius=1, color=COLOR, thickness=-1)
        cv2.rectangle(frame, pt1, pt2, color=COLOR, thickness=3)

    cv2.imshow("WebCam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

#%%
#Ver eventos de mouse de cv2
events = [i for i in dir(cv2) if 'EVENT' in i]
for event in events: print(event)