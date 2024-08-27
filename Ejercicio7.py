import numpy as np
import matplotlib.pyplot as plt
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

# Filtro de media móvil exponencial
def filtro_exponencial(data, alpha=0.6):
    filtered_data = np.zeros_like(data, dtype=np.float64)
    filtered_data[0] = data[0]
    for i in range(1, len(data)):
        filtered_data[i] = alpha * data[i] + (1 - alpha) * filtered_data[i-1]
    return filtered_data

# Análisis del espectro de frecuencias
def analizar_espectro(data, rate):
    N = len(data)
    T = 1.0 / rate
    yf = fft(data)
    xf = fftfreq(N, T)[:N//2]
    return xf, np.abs(yf[:N//2])

# Función principal
def main():
    rate, data = cargar_audio()
    
    if data is None:
        print("No se ha cargado ningún archivo de audio.")
        return
    
    # Si el archivo es estéreo, usa solo un canal (puedes modificar esto según tus necesidades)
    if len(data.shape) > 1:
        data = data[:, 0]
    
    # Aplicar filtro de media móvil exponencial
    alpha = 0.1  # Puedes ajustar este valor
    filtered_data = filtro_exponencial(data, alpha)
    
    # Analizar espectro de frecuencias de la señal original
    xf, yf = analizar_espectro(data, rate)
    
    # Analizar espectro de frecuencias de la señal filtrada
    xf_filtered, yf_filtered = analizar_espectro(filtered_data, rate)
    
    # Graficar señal original y filtrada
    plt.figure(figsize=(14, 6))
    plt.subplot(2, 1, 1)
    plt.plot(data, label="Señal Original", color="blue", alpha=0.7)
    plt.plot(filtered_data, label="Señal Filtrada", color="orange", alpha=0.7)
    plt.title("Señal Original vs Señal Filtrada")
    plt.legend()
    
    # Graficar espectro de frecuencias
    plt.subplot(2, 1, 2)
    plt.plot(xf, yf, label="Espectro Original", color="blue", alpha=0.7)
    plt.plot(xf_filtered, yf_filtered, label="Espectro Filtrado", color="orange", alpha=0.7)
    plt.title("Espectro de Frecuencias")
    plt.legend()
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
