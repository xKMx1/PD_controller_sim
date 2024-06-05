import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

PI = np.pi

h = 0.001       # krok obliczeń
T = 10.0        # całkowity czas symulacji

total = int(T / h) + 1
time = np.linspace(0, T, total)

u = np.zeros(total)  # sygnał wejściowy
u1p = np.zeros(total)  # pierwsza pochodna sygnału wejściowego
u2p = np.zeros(total)  # druga pochodna sygnału wejściowego
y = np.zeros(total)  # sygnał wyjściowy
y1p = np.zeros(total)  # pierwsza pochodna sygnału wyjściowego
y2p = np.zeros(total)  # druga pochodna sygnału wyjściowego

def dirac_delta_approx(x, epsilon): 
    return (1 / (epsilon * np.sqrt(2 * np.pi))) * np.exp(-x**2 / (2 * epsilon**2))

# Sygnał wejściowy (1. harmoniczny) i jego pochodne
def harmonic_function(L=2.5, M=8.0):
    w = 2.0 * PI * L / T

    for i in range(total):
        t = i * h
        u[i] = M * np.sin(w * t)
        u1p[i] = M * w * np.cos(w * t)
        u2p[i] = -M * w * w * np.sin(w * t)

# Sygnał wejściowy (2. trójkątny) i jego pochodne
def triangle_function(A=100, F=2):
    for i in range(total):
        t = i*h
        u[i] = A * (2 * np.abs(2 * (t * F - np.floor(t * F + 0.5))) - 1)
        u1p[i] = 4*A*np.sign(2*(t*F - np.floor(t*F+0.5)))*F
        delta_arg = t * F - np.floor(t * F + 0.5)
        u2p[i] = 8 * A * F * dirac_delta_approx(delta_arg, 0.001)

# Sygnał wejściowy (3. prostokątny) i jego pochodne
def square_function(AM=20, X=1, H=0.01):
    for i in range(total):
        t = i*h
        u[i] = AM*np.sign(np.sin(2*PI*H*(t - X)))
        u1p[i] = 0
        u2p[i] = 0

# transmitance constants
a1 = 4
a0 = 20
b2 = 300
b1 = 149
b0 = 69
# regulator constants
kd = 20
kp = 4

class PDSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Symulator PD")

        self.fig, (self.ax, self.bx) = plt.subplots(2, 1)

        self.canvas = FigureCanvasTkAgg(self.fig, self.root)

        self.quit_button = ttk.Button(self.root, text="Quit", command=root.quit)
        self.quit_button.pack(side=tk.BOTTOM)

        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        self.label = ttk.Label(self.root, text="Enter parameters:")
        self.label.pack(side=tk.TOP)

        # Create frames for the top and bottom rows of parameters
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.bottom_frame = ttk.Frame(self.root)
        self.bottom_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Create frame for input signal selection
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Input signal parameters
        self.signal_label = ttk.Label(self.input_frame, text="Select Input Signal:")
        self.signal_label.grid(row=0, column=0, padx=5, pady=5)
        self.signal_var = tk.StringVar(value="harmonic")
        self.signal_menu = ttk.Combobox(self.input_frame, textvariable=self.signal_var, values=["harmonic", "triangle", "square"])
        self.signal_menu.grid(row=0, column=1, padx=5, pady=5)
        self.signal_menu.bind("<<ComboboxSelected>>", lambda event: self.update_input_parameters())

        # Harmonic signal parameters
        self.L_label = ttk.Label(self.input_frame, text="L (Frequency Multiplier):")
        self.L_label.grid(row=1, column=0, padx=5, pady=5)
        self.L_entry = ttk.Spinbox(self.input_frame, from_=0.1, to=10.0, increment=0.1)
        self.L_entry.grid(row=1, column=1, padx=5, pady=5)
        self.L_entry.insert(0, "2.5")

        self.M_label = ttk.Label(self.input_frame, text="M (Amplitude):")
        self.M_label.grid(row=1, column=2, padx=5, pady=5)
        self.M_entry = ttk.Spinbox(self.input_frame, from_=0.1, to=20.0, increment=0.1)
        self.M_entry.grid(row=1, column=3, padx=5, pady=5)
        self.M_entry.insert(0, "8.0")

        # Triangle signal parameters
        self.A_label = ttk.Label(self.input_frame, text="A (Amplitude):")
        self.A_label.grid(row=2, column=0, padx=5, pady=5)
        self.A_entry = ttk.Spinbox(self.input_frame, from_=1, to=200, increment=1)
        self.A_entry.grid(row=2, column=1, padx=5, pady=5)
        self.A_entry.insert(0, "100")

        self.F_label = ttk.Label(self.input_frame, text="F (Frequency):")
        self.F_label.grid(row=2, column=2, padx=5, pady=5)
        self.F_entry = ttk.Spinbox(self.input_frame, from_=0.1, to=10.0, increment=0.1)
        self.F_entry.grid(row=2, column=3, padx=5, pady=5)
        self.F_entry.insert(0, "2.0")

        # Square signal parameters
        self.AM_label = ttk.Label(self.input_frame, text="AM (Amplitude):")
        self.AM_label.grid(row=3, column=0, padx=5, pady=5)
        self.AM_entry = ttk.Spinbox(self.input_frame, from_=1, to=50, increment=1)
        self.AM_entry.grid(row=3, column=1, padx=5, pady=5)
        self.AM_entry.insert(0, "20")

        self.X_label = ttk.Label(self.input_frame, text="X (Phase Shift):")
        self.X_label.grid(row=3, column=2, padx=5, pady=5)
        self.X_entry = ttk.Spinbox(self.input_frame, from_=0.0, to=5.0, increment=0.1)
        self.X_entry.grid(row=3, column=3, padx=5, pady=5)
        self.X_entry.insert(0, "1.0")

        self.H_label = ttk.Label(self.input_frame, text="H (Frequency):")
        self.H_label.grid(row=3, column=4, padx=5, pady=5)
        self.H_entry = ttk.Spinbox(self.input_frame, from_=0.01, to=1.0, increment=0.01)
        self.H_entry.grid(row=3, column=5, padx=5, pady=5)
        self.H_entry.insert(0, "0.01")

        # Top frame parameters
        self.a0_label = ttk.Label(self.top_frame, text="a0:")
        self.a0_label.grid(row=0, column=0, padx=5, pady=5)
        self.a0_entry = ttk.Spinbox(self.top_frame, from_=-100, to=100, increment=0.1)
        self.a0_entry.grid(row=0, column=1, padx=5, pady=5)
        self.a0_entry.insert(1, "1")

        self.a1_label = ttk.Label(self.top_frame, text="a1:")
        self.a1_label.grid(row=0, column=2, padx=5, pady=5)
        self.a1_entry = ttk.Spinbox(self.top_frame, from_=-100, to=100, increment=0.1)
        self.a1_entry.grid(row=0, column=3, padx=5, pady=5)
        self.a1_entry.insert(1, "1")

        self.b0_label = ttk.Label(self.top_frame, text="b0:")
        self.b0_label.grid(row=0, column=4, padx=5, pady=5)
        self.b0_entry = ttk.Spinbox(self.top_frame, from_=-100, to=100, increment=0.1)
        self.b0_entry.grid(row=0, column=5, padx=5, pady=5)
        self.b0_entry.insert(1, "1")

        self.b1_label = ttk.Label(self.top_frame, text="b1:")
        self.b1_label.grid(row=0, column=6, padx=5, pady=5)
        self.b1_entry = ttk.Spinbox(self.top_frame, from_=-100, to=100, increment=0.1)
        self.b1_entry.grid(row=0, column=7, padx=5, pady=5)
        self.b1_entry.insert(1, "1")

        self.b2_label = ttk.Label(self.top_frame, text="b2:")
        self.b2_label.grid(row=0, column=8, padx=5, pady=5)
        self.b2_entry = ttk.Spinbox(self.top_frame, from_=-100, to=100, increment=0.1)
        self.b2_entry.grid(row=0, column=9, padx=5, pady=5)
        self.b2_entry.insert(1, "1")

        # Bottom frame parameters
        self.kp_label = ttk.Label(self.bottom_frame, text="kp:")
        self.kp_label.grid(row=0, column=0, padx=1, pady=5, sticky='e')
        self.kp_entry = ttk.Spinbox(self.bottom_frame, from_=-100, to=100, increment=0.1)
        self.kp_entry.grid(row=0, column=1, padx=1, pady=5)
        self.kp_entry.insert(1, "1")

        self.kd_label = ttk.Label(self.bottom_frame, text="kd:")
        self.kd_label.grid(row=0, column=2, padx=1, pady=5, sticky='e')
        self.kd_entry = ttk.Spinbox(self.bottom_frame, from_=-100, to=100, increment=0.1)
        self.kd_entry.grid(row=0, column=3, padx=1, pady=5)
        self.kd_entry.insert(1, "1")

        # Center the bottom frame
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)
        self.bottom_frame.grid_columnconfigure(2, weight=1)
        self.bottom_frame.grid_columnconfigure(3, weight=1)

        # Update signal parameters and plot when changing the values
        self.L_entry.bind("<Return>", lambda event: self.update_plot())
        self.M_entry.bind("<Return>", lambda event: self.update_plot())
        self.A_entry.bind("<Return>", lambda event: self.update_plot())
        self.F_entry.bind("<Return>", lambda event: self.update_plot())
        self.AM_entry.bind("<Return>", lambda event: self.update_plot())
        self.X_entry.bind("<Return>", lambda event: self.update_plot())
        self.H_entry.bind("<Return>", lambda event: self.update_plot())

        self.a0_entry.bind("<Return>", lambda event: self.update_plot())
        self.a1_entry.bind("<Return>", lambda event: self.update_plot())
        self.b0_entry.bind("<Return>", lambda event: self.update_plot())
        self.b1_entry.bind("<Return>", lambda event: self.update_plot())
        self.b2_entry.bind("<Return>", lambda event: self.update_plot())
        self.kp_entry.bind("<Return>", lambda event: self.update_plot())
        self.kd_entry.bind("<Return>", lambda event: self.update_plot())

        self.update_plot()

    def update_input_parameters(self):
        signal_type = self.signal_var.get()
        if signal_type == "harmonic":
            self.L_entry.grid()
            self.M_entry.grid()
            self.A_entry.grid_remove()
            self.F_entry.grid_remove()
            self.AM_entry.grid_remove()
            self.X_entry.grid_remove()
            self.H_entry.grid_remove()
        elif signal_type == "triangle":
            self.L_entry.grid_remove()
            self.M_entry.grid_remove()
            self.A_entry.grid()
            self.F_entry.grid()
            self.AM_entry.grid_remove()
            self.X_entry.grid_remove()
            self.H_entry.grid_remove()
        elif signal_type == "square":
            self.L_entry.grid_remove()
            self.M_entry.grid_remove()
            self.A_entry.grid_remove()
            self.F_entry.grid_remove()
            self.AM_entry.grid()
            self.X_entry.grid()
            self.H_entry.grid()

    def calculate(self):
        self.a0 = float(self.a0_entry.get())
        self.a1 = float(self.a1_entry.get())
        self.b0 = float(self.b0_entry.get())
        self.b1 = float(self.b1_entry.get())
        self.b2 = float(self.b2_entry.get())
        self.kp = float(self.kp_entry.get())
        self.kd = float(self.kd_entry.get())

        signal_type = self.signal_var.get()
        if signal_type == "harmonic":
            L = float(self.L_entry.get())
            M = float(self.M_entry.get())
            harmonic_function(L, M)
        elif signal_type == "triangle":
            A = float(self.A_entry.get())
            F = float(self.F_entry.get())
            triangle_function(A, F)
        elif signal_type == "square":
            AM = float(self.AM_entry.get())
            X = float(self.X_entry.get())
            H = float(self.H_entry.get())
            square_function(AM, X, H)

        # closed loop transmitance values
        self.A1 = -(self.b1 + self.kd * self.a0 + self.kp * self.a1) / (self.b2 + self.kd * self.a1)
        self.A0 = (self.b0 + self.kp * self.a0) / (self.b2 + self.kd * self.a1)
        self.B2 = (self.kd * self.a1) / (self.b2 + self.kd * self.a1)
        self.B1 = (self.kd * self.a0 + self.kp * self.a1) / (self.b2 + self.kd * self.a1)
        self.B0 = (self.kp * self.a0) / (self.b2 + self.kd * self.a1)

        for i in range(total - 1):
            y2p[i] = -self.A1 * y1p[i] - self.A0 * y[i] + self.B2 * u2p[i] + self.B1 * u1p[i] + self.B0 * u[i]
            y1p[i + 1] = y1p[i] + h * y2p[i]
            y[i + 1] = y[i] + h * y1p[i] + (h * h / 2.0) * y2p[i]

    def print_to_plot(self):
        self.ax.clear()
        self.ax.plot(time, u, color='b')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.ax.set_title('Input Function')

        self.bx.clear()
        self.bx.plot(time, y, color='r')
        self.bx.set_xlabel('Time')
        self.bx.set_ylabel('Value')
        self.bx.set_title('Output Function')

        self.canvas.draw()

    def update_plot(self):
        self.calculate()
        self.print_to_plot()

def main():
    root = tk.Tk()
    app = PDSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
