import numpy as np
import pyaudio

# Configuración del audio
p = pyaudio.PyAudio()
volume = 0.5     # Volumen de la señal
fs = 44100       # Frecuencia de muestreo (samples por segundo)
duration = 1.0   # Duración de cada nota (en segundos)

# Frecuencias de la escala pentatónica mayor (en Hz)
pentatonic_scale = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25]

# Función para generar una onda senoidal
def generate_sine_wave(frequency, duration, fs):
    t = np.linspace(0, duration, int(fs * duration), False)
    wave = np.sin(2 * np.pi * frequency * t)
    return wave

# Reproducir cada nota de la escala pentatónica
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

for freq in pentatonic_scale:
    samples = generate_sine_wave(freq, duration, fs)
    samples = volume * samples.astype(np.float32)  # Asegúrate de que samples sea un array de NumPy
    stream.write(samples.tobytes())

# Cerrar el stream de audio
stream.stop_stream()
stream.close()
p.terminate()
