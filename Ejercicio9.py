import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve
import datetime

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
#  Generación de símbolos PAM-4
# ====================
segundos_desde_1970 = int(datetime.datetime.now().timestamp())
np.random.seed(segundos_desde_1970)

cantidad_simbolos = 1000
# PAM-4 tiene niveles [-3, -1, 1, 3]
simbolos_PAM4 = np.random.choice([-3, -1, 1, 3], size=cantidad_simbolos)

xn = np.zeros(cantidad_simbolos * M)
for i in range(cantidad_simbolos):
    xn[i * M] = simbolos_PAM4[i]

# ====================
#  Gráficos de la Función sinc (gn)
# ====================
params = { 'legend.fontsize': 'large',
           'figure.figsize': (12, 6),
           'axes.labelsize': 20,
           'axes.titlesize': 20,
           'xtick.labelsize': 15,
           'ytick.labelsize': 15,
           'axes.titlepad': 30 }
plt.rcParams.update(params)

plt.figure(figsize=(15, 6))
plt.stem(t, gn)
plt.title('Filtro Transmisor (sinc)')
plt.grid(True)
plt.show()

# ====================
#  Gráfico de la Muestra Extendida
# ====================
fig, ax = plt.subplots()

cuantos_chupetines = 60
ax.stem(np.arange(0, cuantos_chupetines), xn[0 : cuantos_chupetines])
plt.title('Muestra Extendida (Simbolos PAM-4)')
plt.grid(True)
plt.show()

# ====================
#  Convolución de la señal con el filtro
# ====================
sn = convolve(xn, gn, mode='same')

plt.figure(figsize=(15, 6))
cuantos_chupetines = 1600
plt.plot(np.arange(1000, cuantos_chupetines), sn[1000 : cuantos_chupetines])
plt.title('Señal Convolucionada')
plt.grid(True)
plt.show()

# ====================
#  Diagrama de Ojo
# ====================
d = 4  # Delay para centrar el ojo

plt.figure(figsize=(15, 6))
for i in range(2 * L + 1, cantidad_simbolos - (2 * L + 1)):
    sn_p = sn[i * M + d : i * M + d + M]
    plt.plot(np.arange(-3, 4), sn_p[1 : 8], 'purple')

plt.title('Diagrama de Ojo para PAM-4')
plt.grid(True)
plt.xlim([-3, 3])
plt.ylim([-4, 4])
plt.show()
