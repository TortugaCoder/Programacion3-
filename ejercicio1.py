import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la señal
fs = 100  # Frecuencia de muestreo
t = np.arange(0, 0.3, 1/fs)  # Vector de tiempo de 1 segundo
fc = 5  # Frecuencia de la portadora
fm = 1  # Frecuencia de la señal moduladora
Am = 1  # Amplitud de la señal moduladora
Ac = 1  # Amplitud de la portadora

# Señal portadora
carrier = Ac * np.sin(2 * np.pi * fc * t)

# Señal moduladora
modulator = Am * np.sin(2 * np.pi * fm * t)

# Señal modulada en amplitud
modulated_signal = (modulator) * carrier

# Gque tocas?????raficar las señales
plt.figure(figsize=(10, 8))

# Graficar la señal portadora
plt.subplot(3, 1, 1)
plt.stem(t, carrier)
plt.title('Señal Portadora')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid()

# Graficar la señal moduladora
plt.subplot(3, 1, 2)
plt.stem(t, modulator)
plt.title('Señal Moduladora')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid()

# Graficar la señal modulada en amplitud
plt.subplot(3, 1, 3)
plt.stem(t, modulated_signal)
plt.title('Señal Modulada en Amplitud')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid()

plt.tight_layout()
plt.show()
