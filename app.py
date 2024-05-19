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

a2 = 0
a1 = 1
a0 = 2
b2 = 3
b1 = 2
b0 = 1

# a1 = float(input("\n a1 = "))
# a0 = float(input("\n a0 = "))
# b2 = float(input("\n b2 = "))
# b1 = float(input("\n b1 = "))
# b0 = float(input("\n b0 = "))

# Sygnał wejściowy (1. harmoniczny) i jego pochodne
L = 2.5         # liczba okresów sygnału sinus w przedziale T
M = 8.0         # amplituda sygnału sinus
w = 2.0 * PI * L / T

for i in range(total):
    t = i * h
    u[i] = M * np.sin(w * t)
    u1p[i] = M * w * np.cos(w * t)
    u2p[i] = -M * w * w * np.sin(w * t)

for i in range(total - 1):
    y2p[i] = -a2 * y2p[i] - a1 * y1p[i] - a0 * y[i] + b2 * u2p[i] + b1 * u1p[i] + b0 * u[i]
    y1p[i + 1] = y1p[i] + h * y2p[i]
    y[i + 1] = y[i] + h * y1p[i] + (h * h / 2.0) * y2p[i]


root = Tk()
frm = ttk.Frame(root, padding=100)
frm.grid()

fig, (ax, bx) = plt.subplots(2, 1)
ax.plot(time, y1p)
bx.plot(time, y2p)


canvas = FigureCanvasTkAgg(fig, root)
canvas.draw()
plt.show()

root.mainloop()