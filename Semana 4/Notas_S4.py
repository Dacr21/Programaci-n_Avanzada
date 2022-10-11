#%%
import tkinter as tk
from tkinter import font
import tkinter.ttk as ttk
from random import randrange, uniform

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Tk Animation APP")

        self.WIDTH = 300
        self.HEIGHT = 400
        self.SIZE = 15

        self.canvas = tk.Canvas(self.master, bg = 'white', 
                                width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack()
        self.set_ball()
        self.canvas.bind("<Button-1>", self.update_graph)

    def update_graph(self, event):
        xmouse, ymouse = event.x, event.y
        print("Click")

        if self.x < xmouse < (self.x + self.SIZE) and self.y < ymouse < (self.y + self.SIZE):
            self.canvas.delete(self.ball)
            self.set_ball()

    def set_ball(self):
        self.x = randrange(1, self.WIDTH - self.SIZE -1)
        self.y = randrange(1, self.HEIGHT - self.SIZE -1)
        self.ball = self.canvas.create_oval(self.x, self.y, 
                                            self.x + self.SIZE, 
                                            self.y + self.SIZE, 
                                            fill = 'red')


root = tk.Tk()
App(root)
root.mainloop()

#%%
import tkinter as tk
import tkinter.ttk as ttk
from random import randrange, uniform

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Tk Animation APP")

        self.WIDTH = 300
        self.HEIGHT = 400
        self.SIZE = 10
        self.DELAY = 30 # 50ms
        self.pause_animation = False

        self.canvas = tk.Canvas(self.master, bg = 'white', 
                                width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack()
        self.set_ball()
        self.canvas.bind("<Button-1>", self.control_animation)
        self.animate_canvas()

    def control_animation(self, event):
        #Pausar o reanudar animacion
        self.pause_animation = not self.pause_animation

        if self.pause_animation:
            self.text = self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2,
                                    text="Animation Paused",
                                    font = "Arial 16 bold")
        
        else:
            self.canvas.delete(self.text)


    def set_ball(self):
        self.x = randrange(10, self.WIDTH - self.SIZE -1)
        self.y = randrange(10, self.HEIGHT - self.SIZE -1)

        self.dx = uniform(-10,10)
        self.dy = uniform(-10,10)

        self.ball = self.canvas.create_oval(self.x, self.y, 
                                            self.x + self.SIZE, 
                                            self.y + self.SIZE, 
                                            fill = 'red')
    
    def animate_canvas(self):
        if not self.pause_animation:
        #verificar si la bola debe revotar
            if self.x <= 0 or (self.x + self.SIZE) >= self.WIDTH:
                self.dx = -self.dx

            if self.y <= 0 or (self.y + self.SIZE) >= self.HEIGHT:
                self.dy = -self.dy

        #Moverla a su nueva posicion
            self.x += self.dx
            self.y += self.dy

            self.canvas.move(self.ball, self.dx, self.dy)
    
        self.canvas.after(self.DELAY, self.animate_canvas)

root = tk.Tk()
App(root)
root.mainloop()

#%%
import tkinter as tk
import tkinter.ttk as ttk
from random import randrange, uniform
import numpy as np

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Tk Animation APP")

        self.WIDTH = 300
        self.HEIGHT = 400
        self.SIZE = 10
        self.DELAY = 30 # 50ms
        self.pause_animation = False
        self.N_BALLS = 5

        self.canvas = tk.Canvas(self.master, bg = 'white', 
                                width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack()
        self.set_ball()
        self.canvas.bind("<Button-1>", self.control_animation)
        self.animate_canvas()

    def control_animation(self, event):
        #Pausar o reanudar animacion
        self.pause_animation = not self.pause_animation

        if self.pause_animation:
            self.text = self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2,
                                    text="Animation Paused",
                                    font = "Arial 16 bold")
        
        else:
            self.canvas.delete(self.text)


    def set_ball(self):
        #self.x = [65, 23]
        self.x = np.random.randint(10, self.WIDTH - self.SIZE -10, (self.N_BALLS))
        self.y = np.random.randint(10, self.HEIGHT - self.SIZE -10, (self.N_BALLS))
        #self.dx = [4.3216589, 7.165132]
        self.dx = np.random.uniform(-10,10,self.N_BALLS)
        self.dy = np.random.uniform(-10,10,self.N_BALLS)

        self.balls = []

        for idx in range(self.N_BALLS):
            self.balls.append(self.canvas.create_oval(self.x[idx], self.y[idx], 
                                            self.x[idx] + self.SIZE, 
                                            self.y[idx] + self.SIZE, 
                                            fill = 'red'))

     
    
    def animate_canvas(self):
        if not self.pause_animation:
        #verificar si la bola debe revotar
            for idx in range(self.N_BALLS):
                if self.x[idx] <= 0 or (self.x[idx] + self.SIZE) >= self.WIDTH:
                    self.dx[idx] = -self.dx[idx]

                if self.y[idx] <= 0 or (self.y[idx] + self.SIZE) >= self.HEIGHT:
                    self.dy[idx] = -self.dy[idx]

        #Moverla a su nueva posicion
                self.x[idx] = self.x[idx] + self.dx[idx]
                self.y[idx] = self.y[idx] + self.dy[idx]
            
            for idx in range(self.N_BALLS):
                self.canvas.move(self.balls[idx], self.dx[idx], self.dy[idx])
    
        self.canvas.after(self.DELAY, self.animate_canvas)

root = tk.Tk()
App(root)
root.mainloop()
#%%
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App:

    def __init__(self, master):
        self.master = master
        self.master.title("Tk + Matplotlib")
        self.master.resizable(0, 0)
        self.amp = tk.DoubleVar(value=6)
        self.freq = tk.IntVar(value=1)
        self.var_color = tk.IntVar()
        self.amp_max = 12
        self.freq_max = 20
        self.t_max = 3
        self.plot_colors = {0: 'blue', 1: 'red', 2: 'green', 3: 'magenta'}

    # ------------------------------ Frames -------------------------------------

        frm = tk.Frame(self.master)
        frm.pack()

        frm1 = tk.Frame(frm)
        frm1.pack(padx=10, pady=10)
        frm2 = tk.Frame(frm)
        frm2.pack(padx=10, pady=10)
        frm3 = tk.Frame(frm)
        frm3.pack(padx=10, pady=10)
        frmAmp = tk.LabelFrame(frm2, text="Amplitud")
        frmFreq = tk.LabelFrame(frm2, text="Frecuencia")
        frmAmp.pack(side=tk.LEFT, padx=10, pady=10, ipadx=6)
        frmFreq.pack(side=tk.LEFT, padx=10, pady=10, ipadx=6)    
        frmColor = tk.LabelFrame(frm3, text="Color")
        frmColor.pack(padx=10, pady=10, ipadx=2)

    # ------------------- Matplotlib initial plot ---------------------------

        self.fig, self.ax = plt.subplots(figsize=(6, 4), facecolor='#F0F0F0')
        self.t = np.linspace(0, self.t_max, 50 * self.freq_max)
        y = self.amp.get() * np.sin(2 * np.pi * self.freq.get() * self.t)
        self.line, = self.ax.plot(self.t, y, color=self.plot_colors[self.var_color.get()])
        self.ax.grid(linestyle=':')
        self.ax.set_xlim([0, self.t_max])
        self.ax.set_ylim([-self.amp_max - 3, self.amp_max + 3])
        self.ax.set_title(f"Onda senoidal @ {self.freq.get()}Hz")
        self.ax.set_xlabel("Tiempo [seg]")
        self.ax.set_ylabel("Amplitud")   

    # -------------------------------- frm1 ---------------------------------

        self.graph = FigureCanvasTkAgg(self.fig, master=frm1)
        self.graph.get_tk_widget().pack(expand=True, fill=tk.BOTH)

        # -------------------------------- frmAmp --------------------------------

        self.btnAmp_Low = tk.Button(frmAmp, text="<<", font="Arial 12", width=4, 
                    command=self.set_amp_low)

        self.btnAmp_High = tk.Button(frmAmp, text=">>", font="Arial 12", width=4,
                    command=self.set_amp_high)

        self.btnAmp_Low.grid(row=0, column=0, padx=10, pady=10)
        self.btnAmp_High.grid(row=0, column=1, padx=10, pady=10)

    # -------------------------------- frmFreq -------------------------------

        self.btnFreq_Low = tk.Button(frmFreq, text="<<", font="Arial 12", width=4, 
                    command=self.set_freq_low)

        self.btnFreq_High = tk.Button(frmFreq, text=">>", font="Arial 12", width=4,
                    command=self.set_freq_high)

        self.btnFreq_Low.grid(row=0, column=0, padx=10, pady=10)
        self.btnFreq_High.grid(row=0, column=1, padx=10, pady=10)

# -------------------------------- frmColor -------------------------------

        self.rdoBlue = tk.Radiobutton(frmColor, text="Azul", variable=self.var_color, value=0,
                    command=self.set_plot_color)

        self.rdoRed = tk.Radiobutton(frmColor, text="Rojo", variable=self.var_color, value=1,
                    command=self.set_plot_color)

        self.rdoGreen = tk.Radiobutton(frmColor, text="Verde", variable=self.var_color, value=2,
                        command=self.set_plot_color)

        self.Magenta = tk.Radiobutton(frmColor, text="Magenta", variable=self.var_color, value=3, 
                    command=self.set_plot_color) 

        self.rdoBlue.grid(row=0, column=0, padx=10, pady=5)
        self.rdoRed.grid(row=0, column=1, padx=10, pady=5)
        self.rdoGreen.grid(row=0, column=2, padx=10, pady=5)
        self.Magenta.grid(row=0, column=3, padx=10, pady=5)

    def set_amp_low(self):
        if self.amp.get() > 0:
            self.amp.set(self.amp.get() - 0.25)
            self.draw_graph()

    def set_amp_high(self):
        if self.amp.get() < self.amp_max:
            self.amp.set(self.amp.get() + 0.25)
            self.draw_graph()

    def set_freq_low(self):
        if self.freq.get() > 1:
            self.freq.set(self.freq.get() - 1)
            self.draw_graph()

    def set_freq_high(self):
        if self.freq.get() < self.freq_max:
            self.freq.set(self.freq.get() + 1)
            self.draw_graph()

    def set_plot_color(self):
        self.line.set_color(self.plot_colors[self.var_color.get()])
        self.graph.draw()   

    def draw_graph(self):
        self.line.set_ydata(self.amp.get() * np.sin(2 * np.pi * self.freq.get() * self.t))
        self.ax.set_title(f"Onda senoidal @ {self.freq.get()}Hz")
        self.graph.draw()

root = tk.Tk()
App(root)
root.mainloop()

# %%
