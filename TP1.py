import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import librosa
import librosa.display
import numpy as np
from scipy.fft import fft
from pydub import AudioSegment
import pygame
import os
import wave

# Función para cargar y convertir archivo de audio
def load_and_convert_audio(file_path):
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext == ".mp3":
        audio = AudioSegment.from_mp3(file_path)
        file_path = "temp.wav"
        audio.export(file_path, format="wav")
    y, sr = librosa.load(file_path, sr=None)
    return y, sr, file_path

# Función para obtener los bits de codificación del ADC
def get_bits_per_sample(file_path):
    with wave.open(file_path, "rb") as wf:
        return wf.getsampwidth() * 8  # Obtiene el ancho de la muestra en bytes y lo convierte a bits

# Función para reproducir el archivo de audio
def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Función para analizar y graficar el audio
def analyze_audio():
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav;*.mp3")])
    if not file_path:
        return

    y, sr, wav_path = load_and_convert_audio(file_path)
    
    # Mostrar información del archivo
    duration = len(y) / sr
    channels = "1 (Mono)" if len(y.shape) == 1 else str(y.shape[1])
    bits_per_sample = get_bits_per_sample(wav_path)

    freq_label.config(text=f"Frecuencia de muestreo: {sr} Hz")
    dur_label.config(text=f"Duración: {duration:.2f} segundos")
    chan_label.config(text=f"Cantidad de canales: {channels}")
    bits_label.config(text=f"Bits de codificación: {bits_per_sample} bits")
    
    # Reproducir el audio
    play_audio(file_path)

    # Ajustar dinámicamente el valor de n_fft
    n_fft = min(2048, len(y))  # n_fft nunca será mayor que la longitud de la señal
    
    if len(y) < n_fft:
        result_label.config(text="El archivo de audio es demasiado corto para analizar con n_fft=2048")
        return
    
    # Limpiar gráficos anteriores
    for ax in [ax1, ax2, ax3]:
        ax.clear()

    # Espectrograma
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y, n_fft=n_fft)), ref=np.max)
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log', ax=ax1)
    ax1.set_title('Espectrograma')
    ax1.set_xlabel('')
    ax1.set_ylabel('')
    
    # Transformada de Fourier
    yf = fft(y)
    xf = np.linspace(0.0, sr/2, len(y)//2)
    ax2.plot(xf, 2.0/len(y) * np.abs(yf[:len(y)//2]), color='orange')
    ax2.grid()
    ax2.set_title('Transformada de Fourier')
    ax2.set_xlabel('')
    ax2.set_ylabel('')

    # Señal en función del tiempo
    librosa.display.waveshow(y, sr=sr, ax=ax3, color='green')
    ax3.set_title('Señal de audio en función del tiempo')
    ax3.set_xlabel('')
    ax3.set_ylabel('')

    # Dibujar los gráficos
    canvas.draw()

# Crear la ventana principal con estilo
root = tk.Tk()
root.title("Análisis de Audio")
root.configure(bg="#2E2E2E")  # Fondo gris oscuro

# Estilo de los textos y botones
label_style = {"bg": "#2E2E2E", "fg": "white", "font": ("Helvetica", 12)}
button_style = {"bg": "#4CAF50", "fg": "white", "font": ("Helvetica", 12, "bold")}

# Crear el botón para cargar archivo
upload_button = tk.Button(root, text="Subir", command=analyze_audio, **button_style)
upload_button.grid(row=0, column=1, pady=10, padx=10)

# Crear etiquetas para mostrar la información del archivo
freq_label = tk.Label(root, text="Frecuencia de muestreo:", **label_style)
freq_label.grid(row=1, column=1, sticky="w", padx=10)

dur_label = tk.Label(root, text="Duración:", **label_style)
dur_label.grid(row=2, column=1, sticky="w", padx=10)

chan_label = tk.Label(root, text="Cantidad de canales:", **label_style)
chan_label.grid(row=3, column=1, sticky="w", padx=10)

bits_label = tk.Label(root, text="Bits de codificación:", **label_style)
bits_label.grid(row=4, column=1, sticky="w", padx=10)

# Crear el canvas para los gráficos con un fondo más estético
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6))
fig.patch.set_facecolor("#2E2E2E")  # Fondo de la figura
fig.tight_layout(pad=3.0)

for ax in [ax1, ax2, ax3]:
    ax.set_facecolor("#1E1E1E")  # Fondo de los gráficos
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, rowspan=5, padx=10)

# Etiqueta para mostrar el resultado de análisis
result_label = tk.Label(root, text="", **label_style)
result_label.grid(row=5, column=0, columnspan=2)

# Iniciar la interfaz
root.mainloop()
