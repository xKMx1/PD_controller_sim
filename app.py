from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

h = 0.001       # krok obliczeń
T = 10.0        # całkowity czas symulacji

a1 = 1
a0 = 2
b2 = 3
b1 = 2
b0 = 1

root = Tk()
frm = ttk.Frame(root, padding=100)
frm.grid()

fig, (ax, bx) = plt.subplots(2, 1)
ax.plot([1,2,3,4], [1,2,3,4])
bx.plot([1,2,3,4], [3,4,6,2])


canvas = FigureCanvasTkAgg(fig, root)
canvas.draw()
# plt.show()

root.mainloop()