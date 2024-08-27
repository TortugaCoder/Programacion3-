import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import upfirdn

# Configuraciones
fs = 1e9  # Frecuencia de muestreo (1 GHz)
symbol_rate = 1e6  # Velocidad de símbolos (1 Msymbol/s)
rolloff = 0.35  # Factor de roll-off para el filtro de caída cosenoidal

# Generación del mensaje simple
def generate_message():
    message = "Hola Mundo"
    return message

# Codificación del mensaje en binario
def encode_message(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message

# Agregar encabezado HTTP
def add_http_header(binary_message):
    http_header = "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
    binary_header = ''.join(format(ord(char), '08b') for char in http_header)
    return binary_header + binary_message

# Agregar encabezado TCP
def add_tcp_header(binary_message):
    # Simplificación: el encabezado TCP básico no incluye todos los campos reales
    tcp_header = "00000000"  # Simplificado: un encabezado TCP básico de 8 bits
    return tcp_header + binary_message

# Agregar encabezado IP
def add_ip_header(binary_message):
    # Simplificación: el encabezado IP básico no incluye todos los campos reales
    ip_header = "11100000"  # Simplificado: un encabezado IP básico de 8 bits
    return ip_header + binary_message

# Agregar encabezado Ethernet
def add_ethernet_header(binary_message):
    # Simplificación: el encabezado Ethernet básico no incluye todos los campos reales
    ethernet_header = "0000000000000000"  # Simplificado: un encabezado Ethernet básico de 16 bytes
    return ethernet_header + binary_message

# Codificación 4D-PAM5
def encode_pam5(binary_message):
    # Simular codificación PAM5 (simplificada para este ejemplo)
    mapping = {'00': -2, '01': -1, '10': 1, '11': 2}
    pam5_symbols = [mapping[binary_message[i:i+2]] for i in range(0, len(binary_message), 2)]
    return np.array(pam5_symbols)

# Filtro sinc de caída cosenoidal
def sinc_filter(rolloff, symbol_rate, fs):
    span = 10  # Número de símbolos en la ventana del filtro
    num_taps = span * int(fs / symbol_rate) + 1
    t = np.linspace(-span / 2, span / 2, num_taps)
    sinc_filter = np.sinc(t * symbol_rate) * np.cos(np.pi * rolloff * t * symbol_rate) / (1 - (2 * rolloff * t * symbol_rate) ** 2)
    sinc_filter /= np.sum(sinc_filter)  # Normalizar
    return sinc_filter

# Aplicación del filtro sinc
def apply_filter(pam5_symbols, filter_coeffs):
    return upfirdn(filter_coeffs, pam5_symbols, up=1, down=1)

# Graficar resultados
def plot_results(original_message, binary_message, binary_message_with_http, binary_message_with_tcp, binary_message_with_ip, binary_message_with_ethernet, pam5_symbols, filtered_signal):
    plt.figure(figsize=(15, 15))

    plt.subplot(8, 1, 1)
    plt.title('Mensaje Original')
    plt.text(0, 0.5, original_message, fontsize=12)
    plt.axis('off')

    plt.subplot(8, 1, 2)
    plt.title('Mensaje Binario (Antes de Protocolos)')
    plt.step(np.arange(len(binary_message)), [int(bit) for bit in binary_message], where='post')
    plt.xlabel('Índice de bits')
    plt.ylabel('Valor del bit')

    plt.subplot(8, 1, 3)
    plt.title('Mensaje Binario (Después de Agregar Encabezado HTTP)')
    plt.step(np.arange(len(binary_message_with_http)), [int(bit) for bit in binary_message_with_http], where='post')
    plt.xlabel('Índice de bits')
    plt.ylabel('Valor del bit')

    plt.subplot(8, 1, 4)
    plt.title('Mensaje Binario (Después de Agregar Encabezado TCP)')
    plt.step(np.arange(len(binary_message_with_tcp)), [int(bit) for bit in binary_message_with_tcp], where='post')
    plt.xlabel('Índice de bits')
    plt.ylabel('Valor del bit')

    plt.subplot(8, 1, 5)
    plt.title('Mensaje Binario (Después de Agregar Encabezado IP)')
    plt.step(np.arange(len(binary_message_with_ip)), [int(bit) for bit in binary_message_with_ip], where='post')
    plt.xlabel('Índice de bits')
    plt.ylabel('Valor del bit')

    plt.subplot(8, 1, 6)
    plt.title('Mensaje Binario (Después de Agregar Encabezado Ethernet)')
    plt.step(np.arange(len(binary_message_with_ethernet)), [int(bit) for bit in binary_message_with_ethernet], where='post')
    plt.xlabel('Índice de bits')
    plt.ylabel('Valor del bit')

    plt.subplot(8, 1, 7)
    plt.title('Símbolos PAM5 Codificados')
    plt.stem(pam5_symbols)  # Sin use_line_collection=True
    plt.xlabel('Índice de símbolo')
    plt.ylabel('Valor del símbolo PAM5')

    plt.subplot(8, 1, 8)
    plt.title('Señal Después del Filtro Sinc')
    plt.plot(filtered_signal)
    plt.xlabel('Índice de muestra')
    plt.ylabel('Amplitud')

    plt.tight_layout()
    plt.show()

# Main
original_message = generate_message()
binary_message = encode_message(original_message)
binary_message_with_http = add_http_header(binary_message)
binary_message_with_tcp = add_tcp_header(binary_message_with_http)
binary_message_with_ip = add_ip_header(binary_message_with_tcp)
binary_message_with_ethernet = add_ethernet_header(binary_message_with_ip)
pam5_symbols = encode_pam5(binary_message_with_ethernet)
sinc_filter_coeffs = sinc_filter(rolloff, symbol_rate, fs)
filtered_signal = apply_filter(pam5_symbols, sinc_filter_coeffs)

# Imprimir resultados
print("Mensaje Original:")
print(original_message)
print("\nMensaje Binario (Antes de Protocolos):")
print(binary_message)
print("\nMensaje Binario (Después de Agregar Encabezado HTTP):")
print(binary_message_with_http)
print("\nMensaje Binario (Después de Agregar Encabezado TCP):")
print(binary_message_with_tcp)
print("\nMensaje Binario (Después de Agregar Encabezado IP):")
print(binary_message_with_ip)
print("\nMensaje Binario (Después de Agregar Encabezado Ethernet):")
print(binary_message_with_ethernet)

# Graficar resultados
plot_results(original_message, binary_message, binary_message_with_http, binary_message_with_tcp, binary_message_with_ip, binary_message_with_ethernet, pam5_symbols, filtered_signal)
