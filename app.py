import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

PI = np.pi

h = 0.001       # krok obliczeń
T = 10.0        # całkowity czas symulacji

total = int(T / h) + 1
time = list(range(0, total))

u = np.zeros(total)  # sygnał wejściowy
u1p = np.zeros(total)  # pierwsza pochodna sygnału wejściowego
u2p = np.zeros(total)  # druga pochodna sygnału wejściowego
y = np.zeros(total)  # sygnał wyjściowy
y1p = np.zeros(total)  # pierwsza pochodna sygnału wyjściowego
y2p = np.zeros(total)  # druga pochodna sygnału wyjściowego


a1 = 4
a0 = 20
b2 = 300
b1 = 149
b0 = 69

kd = 20
kp = 4


A1 = -(b1+kd*a0+kp*a1)/(b2+kd*a1)
A0 = (b0+kp*a0)/(b2+kd*a1)
B2 = (kd*a1)/(b2+kd*a1)
B1 = (kd*a0+kp*a1)/(b2+kd*a1)
B0 = (kp*a0)/(b2+kd*a1)

def dirac_delta_approx(x, epsilon): return (1 / (epsilon * np.sqrt(2 * np.pi))) * np.exp(-x**2 / (2 * epsilon**2))

# a1 = float(input("\n a1 = "))
# a0 = float(input("\n a0 = "))
# b2 = float(input("\n b2 = "))
# b1 = float(input("\n b1 = "))
# b0 = float(input("\n b0 = "))

# Sygnał wejściowy (1. harmoniczny) i jego pochodne
L = 2.5         # liczba okresów sygnału sinus w przedziale T
M = 8.0         # amplituda sygnału sinus
w = 2.0 * PI * L / T

# for i in range(total):
#     t = i * h
#     u[i] = M * np.sin(w * t)
#     u1p[i] = M * w * np.cos(w * t)
#     u2p[i] = -M * w * w * np.sin(w * t)


# Sygnał wejściowy (2. trójkątny) i jego pochodne
# A = 100
# F = 2

# for i in range(total):
#     t = i*h
#     u[i] = A * (2 * np.abs(2 * (t * F - np.floor(t * F + 0.5))) - 1)
#     u1p[i] = 4*A*np.sign(2*(t*F - np.floor(t*F+0.5)))*F
#     delta_arg = t * F - np.floor(t * F + 0.5)
#     u2p[i] = 8 * A * F * dirac_delta_approx(delta_arg, 0.001)


# Sygnał wejściowy (3. prostokątny) i jego pochodne

AM = 20
X = 1            #przesuwa o X * 1000
H= 0.01

for i in range(total):
    t = i*h
    u[i] = AM*np.sign(np.sin(2*PI*H*(t - X)))
    u1p[i]= 0
    u2p[i]= 0

for i in range(total - 1):
    y2p[i] = -A1 * y1p[i] - A0 * y[i] + B2 * u2p[i] + B1 * u1p[i] + B0 * u[i]
    y1p[i + 1] = y1p[i] + h * y2p[i]
    y[i + 1] = y[i] + h * y1p[i] + (h * h / 2.0) * y2p[i]



root = tk.Tk()
root.title("Symulator PD")

fig, (ax, bx) = plt.subplots(2, 1)
ax.plot(time,u)
bx.plot(time, u)

canvas = FigureCanvasTkAgg(fig, root)

quit_button = ttk.Button(root, text="Quit", command=root.quit)
quit_button.pack(side=tk.BOTTOM)

canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

label = ttk.Label(root, text="Enter parameters:")
label.pack(side=tk.TOP)

# Create frames for the top and bottom rows of parameters
top_frame = ttk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

bottom_frame = ttk.Frame(root)
bottom_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

# Top frame parameters
a0_label = ttk.Label(top_frame, text="a0:")
a0_label.grid(row=0, column=0, padx=5, pady=5)
a0_entry = ttk.Spinbox(top_frame, from_=0, to=9)
a0_entry.grid(row=0, column=1, padx=5, pady=5)
a0_entry.insert(0, "1")

a1_label = ttk.Label(top_frame, text="a1:")
a1_label.grid(row=0, column=2, padx=5, pady=5)
a1_entry = ttk.Spinbox(top_frame, from_=0, to=9)
a1_entry.grid(row=0, column=3, padx=5, pady=5)
a1_entry.insert(0, "1")

b0_label = ttk.Label(top_frame, text="b0:")
b0_label.grid(row=0, column=4, padx=5, pady=5)
b0_entry = ttk.Spinbox(top_frame, from_=0, to=9)
b0_entry.grid(row=0, column=5, padx=5, pady=5)
b0_entry.insert(0, "1")

b1_label = ttk.Label(top_frame, text="b1:")
b1_label.grid(row=0, column=6, padx=5, pady=5)
b1_entry = ttk.Spinbox(top_frame, from_=0, to=9)
b1_entry.grid(row=0, column=7, padx=5, pady=5)
b1_entry.insert(0, "1")

b2_label = ttk.Label(top_frame, text="b2:")
b2_label.grid(row=0, column=8, padx=5, pady=5)
b2_entry = ttk.Spinbox(top_frame, from_=0, to=9)
b2_entry.grid(row=0, column=9, padx=5, pady=5)
b2_entry.insert(0, "1")

# Bottom frame parameters
kp_label = ttk.Label(bottom_frame, text="kp:")
kp_label.grid(row=0, column=0, padx=1, pady=5, sticky='e')
kp_entry = ttk.Spinbox(bottom_frame, from_=0, to=9)
kp_entry.grid(row=0, column=1, padx=1, pady=5)
kp_entry.insert(0, "1")

kd_label = ttk.Label(bottom_frame, text="kd:")
kd_label.grid(row=0, column=2, padx=1, pady=5, sticky='e')
kd_entry = ttk.Spinbox(bottom_frame, from_=0, to=9)
kd_entry.grid(row=0, column=3, padx=1, pady=5)
kd_entry.insert(0, "1")

# Center the bottom frame
bottom_frame.grid_columnconfigure(0, weight=1)
bottom_frame.grid_columnconfigure(1, weight=1)
bottom_frame.grid_columnconfigure(2, weight=1)
bottom_frame.grid_columnconfigure(3, weight=1)

canvas.draw()
# plt.show()

root.mainloop()
