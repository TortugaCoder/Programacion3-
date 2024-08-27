import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io.wavfile import write
from IPython.display import Audio, display

def cuantificar_secuencia(secuencia, bits, valor_min, valor_max):
    """
    Cuantifica una secuencia de valores en función de los bits de cuantificación.

    Parámetros:
    - secuencia: array o lista de valores a cuantificar.
    - bits: número de bits para la cuantificación (ej. 8 bits).
    - valor_min: valor mínimo del rango de la señal original.
    - valor_max: valor máximo del rango de la señal original.

    Retorna:
    - secuencia_cuantificada: array de la secuencia cuantificada.
    """
    # Determinar el número de niveles de cuantificación
    niveles = 2 ** bits

    # Calcular el tamaño de cada paso de cuantificación
    paso = (valor_max - valor_min) / (niveles - 1)

    # Cuantificar la secuencia
    secuencia_cuantificada = np.round((secuencia - valor_min) / paso) * paso + valor_min

    # Asegurarse de que los valores estén dentro del rango
    secuencia_cuantificada = np.clip(secuencia_cuantificada, valor_min, valor_max)

    return secuencia_cuantificada

# Parámetros
fs = 44100  # Frecuencia de muestreo (44.1 kHz, estándar para audio)
t = np.linspace(0, 1, fs)  # Vector de tiempo de 1 segundo
f_square = 440  # Frecuencia de la onda cuadrada (440 Hz, la nota A4)
f_triangle = 880  # Frecuencia de la onda triangular (880 Hz, la nota A5)
amplitude = 5  # Amplitud de las ondas
amplitudequant = 2
bits = 5  # Número de bits de cuantificación

# Generar la onda cuadrada
square_wave = amplitude * signal.square(2 * np.pi * f_square * t)

# Generar la onda triangular
triangle_wave = amplitude * signal.sawtooth(2 * np.pi * f_triangle * t, 0.5)

# Sumar ambas ondas
combined_wave = square_wave + triangle_wave

# Cuantificar las señales sin normalización previa
square_wave_quantized = cuantificar_secuencia(square_wave, bits, -amplitudequant, amplitudequant)
triangle_wave_quantized = cuantificar_secuencia(triangle_wave, bits, -amplitudequant, amplitudequant)
combined_wave_quantized = cuantificar_secuencia(combined_wave, bits, -2*amplitudequant, 2*amplitudequant)

# Graficar la onda cuadrada y su versión cuantificada
plt.figure(figsize=(10, 4))
plt.plot(t[:1000], square_wave[:1000], label='Onda Cuadrada Original')
plt.plot(t[:1000], square_wave_quantized[:1000], label='Onda Cuadrada Cuantificada', linestyle='--')
plt.title("Onda Cuadrada vs Cuantificada")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud")
plt.legend()
plt.show()

# Graficar la onda triangular y su versión cuantificada
plt.figure(figsize=(10, 4))
plt.plot(t[:1000], triangle_wave[:1000], label='Onda Triangular Original')
plt.plot(t[:1000], triangle_wave_quantized[:1000], label='Onda Triangular Cuantificada', linestyle='--')
plt.title("Onda Triangular vs Cuantificada")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud")
plt.legend()
plt.show()

# Graficar la onda combinada y su versión cuantificada
plt.figure(figsize=(10, 4))
plt.plot(t[:1000], combined_wave[:1000], label='Onda Combinada Original')
plt.plot(t[:1000], combined_wave_quantized[:1000], label='Onda Combinada Cuantificada', linestyle='--')
plt.title("Onda Combinada vs Cuantificada")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud")
plt.legend()
plt.show()

# Reproducir y guardar la señal cuantificada de la onda cuadrada
display(Audio(square_wave_quantized, rate=fs))
write("onda_cuadrada_cuantificada.wav", fs, square_wave_quantized.astype(np.float32))

# Reproducir y guardar la señal cuantificada de la onda triangular
display(Audio(triangle_wave_quantized, rate=fs))
write("onda_triangular_cuantificada.wav", fs, triangle_wave_quantized.astype(np.float32))

# Reproducir y guardar la señal cuantificada combinada
display(Audio(combined_wave_quantized, rate=fs))
write("onda_combinada_cuantificada.wav", fs, combined_wave_quantized.astype(np.float32))
