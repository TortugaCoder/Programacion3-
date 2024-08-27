import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la señal
f = 1000  # Frecuencia de 1 kHz
A = 5     # Amplitud de -5 a 5
t = np.linspace(0, 0.01, 500)  # 10 ms de señal continua

# Señal continua senoidal
y_cont = A * np.sin(2 * np.pi * f * t)

# Muestreo a 50,000 samples por segundo
fs = 50000  # Frecuencia de muestreo
n = np.arange(50)  # Primeras 50 muestras
t_sampled = n / fs
y_sampled = A * np.sin(2 * np.pi * f * t_sampled)

# Cuantificación con ADC de 12 bits
ADC_bits = 8
ADC_levels = 2**ADC_bits
y_quantized = np.round((y_sampled + A) * (ADC_levels - 1) / (2 * A)) * (2 * A) / (ADC_levels - 1) - A

# Graficar las señales
plt.figure(figsize=(12, 8))

# Señal continua
plt.subplot(3, 1, 1)
plt.plot(t, y_cont)
plt.title('Señal continua senoidal de 1 kHz')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid(True)

# Primeras 50 muestras sin cuantificar
plt.subplot(3, 1, 2)
plt.stem(n, y_sampled)
plt.title('Primeras 50 muestras sin cuantificar')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.grid(True)

# Primeras 50 muestras cuantificadas
plt.subplot(3, 1, 3)
plt.stem(n, y_quantized)
plt.title('Primeras 50 muestras cuantificadas (ADC de 12 bits)')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.grid(True)

plt.tight_layout()
plt.show()
