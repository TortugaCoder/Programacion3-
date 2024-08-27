import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ====================
#  Funciones de Utilidad
# ====================
def texto_a_binario(texto):
    binario = ''.join(format(ord(char), '08b') for char in texto)
    return np.array([int(bit) for bit in binario])

def binario_a_nrz(bits):
    return np.where(bits == 0, -1, 1)

def actualizar_graficos():
    mensaje_texto = entry.get()
    bits_binarios = texto_a_binario(mensaje_texto)
    nrz_signal = binario_a_nrz(bits_binarios)

    xn = np.zeros(len(nrz_signal) * M)
    for i in range(len(nrz_signal)):
        xn[i * M] = nrz_signal[i]

    # ====================
    #  Gráfico del Mensaje en Binario NRZ
    # ====================
    ax1.clear()
    ax1.stem(np.arange(0, len(bits_binarios)), nrz_signal)
    ax1.set_title('Mensaje Binario NRZ')
    ax1.grid(True)

    # ====================
    #  Gráfico del Filtro Sinc (gn)
    # ====================
    ax2.clear()
    ax2.stem(t, gn)
    ax2.set_title('Filtro Transmisor (sinc de caída cosenoidal)')
    ax2.grid(True)

    # ====================
    #  Convolución de la señal con el filtro
    # ====================
    sn = convolve(xn, gn, mode='same')

    ax3.clear()
    cuantos_chupetines = len(sn)
    ax3.plot(np.arange(0, cuantos_chupetines), sn)
    ax3.set_title('Señal Convolucionada')
    ax3.grid(True)

    canvas.draw()

# ====================
#  Configuración y Filtro g[n]
# ====================
fB = 32e9    # Velocidad de símbolos (baud rate)
T = 1 / fB   # Tiempo entre símbolos
M = 8        # Factor de sobremuestreo
fs = fB * M  # Sample rate
alpha = 0.1  # Factor de roll-off
L = 20       # (2 * L * M + 1) es el largo del filtro sobremuestreado

t = np.arange(-L, L, 1 / M) * T
gn = np.sinc(t / T) * np.cos(np.pi * alpha * t / T) / (1 - 4 * alpha**2 * t**2 / T**2)

# ====================
#  Configuración de la Interfaz Gráfica
# ====================
root = tk.Tk()
root.title("Simulación de Transmisión")

# Crear un frame para los widgets de entrada (campo de texto y botón)
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Campo de texto para ingresar el mensaje
entry_label = tk.Label(input_frame, text="Ingrese el mensaje de texto:")
entry_label.pack(side=tk.LEFT)
entry = tk.Entry(input_frame, width=50)
entry.pack(side=tk.LEFT)

# Botón para actualizar gráficos
button = tk.Button(input_frame, text="Actualizar Gráficos", command=actualizar_graficos)
button.pack(side=tk.LEFT, padx=10)

# Crear un frame para los gráficos
plot_frame = tk.Frame(root)
plot_frame.pack()

# Configurar el lienzo de Matplotlib
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12))
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack()

# Mensaje inicial
entry.insert(0, "Hola Mundo")
actualizar_graficos()

root.mainloop()
