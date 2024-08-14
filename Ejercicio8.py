import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import scipy.io.wavfile as wav
from scipy.fft import fft, fftfreq
import tkinter as tk
from tkinter import filedialog

# Función para cargar archivo wav
def cargar_audio():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        rate, data = wav.read(file_path)
        return rate, data
    else:
        return None, None

# Filtro de media móvil exponencial (EMA)
def filtro_exponencial(data, alpha):
    filtered_data = np.zeros_like(data, dtype=np.float64)
    filtered_data[0] = data[0]
    for i in range(1, len(data)):
        filtered_data[i] = alpha * data[i] + (1 - alpha) * filtered_data[i-1]
    return filtered_data

# Filtro de media móvil simple (SMA)
def filtro_sma(data, window_size):
    if window_size > 1:
        filtered_data = np.convolve(data, np.ones(window_size)/window_size, mode='same')
    else:
        filtered_data = data  # Si la ventana es 1, no hay filtrado
    return filtered_data

# Análisis del espectro de frecuencias
def analizar_espectro(data, rate):
    N = len(data)
    T = 1.0 / rate
    yf = fft(data)
    xf = fftfreq(N, T)[:N//2]
    return xf, np.abs(yf[:N//2])

# Función para actualizar gráficos
def actualizar(val):
    alpha = slider_alpha.val
    window_size = int(slider_window.val)
    
    filtered_data_ema = filtro_exponencial(data, alpha)
    filtered_data_sma = filtro_sma(data, window_size)
    
    line_ema.set_ydata(filtered_data_ema)
    line_sma.set_ydata(filtered_data_sma)
    
    xf_ema, yf_ema = analizar_espectro(filtered_data_ema, rate)
    xf_sma, yf_sma = analizar_espectro(filtered_data_sma, rate)
    
    line_spectrum_ema.set_ydata(yf_ema)
    line_spectrum_sma.set_ydata(yf_sma)
    
    fig.canvas.draw_idle()

# Función principal
def main():
    global rate, data, line_ema, line_sma, line_spectrum_ema, line_spectrum_sma, fig, slider_alpha, slider_window
    
    rate, data = cargar_audio()
    
    if data is None:
        print("No se ha cargado ningún archivo de audio.")
        return
    
    # Si el archivo es estéreo, usa solo un canal
    if len(data.shape) > 1:
        data = data[:, 0]
    
    # Inicializar valores
    initial_alpha = 0.1
    initial_window = 5
    
    filtered_data_ema = filtro_exponencial(data, initial_alpha)
    filtered_data_sma = filtro_sma(data, initial_window)
    
    xf, yf = analizar_espectro(data, rate)
    xf_ema, yf_ema = analizar_espectro(filtered_data_ema, rate)
    xf_sma, yf_sma = analizar_espectro(filtered_data_sma, rate)
    
    # Crear figura y ejes
    fig, axs = plt.subplots(3, 1, figsize=(14, 8))
    
    # Gráfico de señal original y filtradas
    axs[0].plot(data, label="Señal Original", color="blue", alpha=0.7)
    line_ema, = axs[0].plot(filtered_data_ema, label="Señal Filtrada (EMA)", color="orange", alpha=0.7)
    axs[0].legend()
    axs[0].set_title("Señal Original vs Señal Filtrada (EMA)")
    
    axs[1].plot(data, label="Señal Original", color="blue", alpha=0.7)
    line_sma, = axs[1].plot(filtered_data_sma, label="Señal Filtrada (SMA)", color="green", alpha=0.7)
    axs[1].legend()
    axs[1].set_title("Señal Original vs Señal Filtrada (SMA)")
    
    # Gráfico de espectro de frecuencias
    axs[2].plot(xf, yf, label="Espectro Original", color="blue", alpha=0.7)
    line_spectrum_ema, = axs[2].plot(xf_ema, yf_ema, label="Espectro EMA", color="orange", alpha=0.7)
    line_spectrum_sma, = axs[2].plot(xf_sma, yf_sma, label="Espectro SMA", color="green", alpha=0.7)
    axs[2].legend()
    axs[2].set_title("Espectro de Frecuencias")
    
    plt.subplots_adjust(left=0.1, bottom=0.25)
    
    # Crear sliders
    axcolor = 'lightgoldenrodyellow'
    ax_alpha = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor=axcolor)
    ax_window = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor=axcolor)
    
    slider_alpha = Slider(ax_alpha, 'Alpha (EMA)', 0.01, 1.0, valinit=initial_alpha)
    slider_window = Slider(ax_window, 'Window Size (SMA)', 1, 50, valinit=initial_window, valstep=1)
    
    # Conectar sliders a la función de actualización
    slider_alpha.on_changed(actualizar)
    slider_window.on_changed(actualizar)
    
    plt.show()

if __name__ == "__main__":
    main()
