from tkinter import *
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


# Sygnał wejściowy (1. trójkątny) i jego pochodne
# A = 100
# F = 2  

# for i in range(total):
#     t = i*h
#     u[i] = A * (2 * np.abs(2 * (t * F - np.floor(t * F + 0.5))) - 1)
#     u1p[i] = 4*A*np.sign(2*(t*F - np.floor(t*F+0.5)))*F
#     delta_arg = t * F - np.floor(t * F + 0.5)
#     u2p[i] = 8 * A * F * dirac_delta_approx(delta_arg, 0.001)


# Sygnał wejściowy (1. prostokątny) i jego pochodne

AM = 20
X = 1  #przesuwa o X * 1000
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

    

root = Tk()
frm = ttk.Frame(root, padding=100)
frm.grid()

fig, (ax, bx) = plt.subplots(2, 1)
ax.plot(time,u)
bx.plot(time, u)


canvas = FigureCanvasTkAgg(fig, root)
canvas.draw()
plt.show()

root.mainloop()
