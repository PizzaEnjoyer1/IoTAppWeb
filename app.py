import paho.mqtt.client as paho
import streamlit as st
import json
import matplotlib.pyplot as plt
import numpy as np

# Variables para el control del ángulo
values = 0.0
act1 = "OFF"
current_angle = 0.0  # Variable para almacenar el ángulo actual

# Función MQTT para publicación
def on_publish(client, userdata, result):
    print("El dato ha sido publicado \n")
    pass

# Función MQTT para recibir mensajes
def on_message(client, userdata, message):
    global message_received
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

# Configuración del broker MQTT
broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("MOTOR_WEB_APP")
client1.on_message = on_message

# Título de la aplicación
st.title("Controla tu servo con esta aplicación")

# Slider para seleccionar el ángulo de giro
values = st.slider('Selecciona el ángulo de giro de su servo', 0.0, 180.0, 90.0)
st.write('Ángulo seleccionado:', values)

# Botón para enviar el valor al servo
if st.button('Enviar valor al servo'):
    client1 = paho.Client("MOTOR_WEB_APP")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    client1.publish("CHANGE_ANGLE", message)
    st.write(f"Ángulo {values} enviado al servo.")

# Actualización automática del gráfico cuando cambia el slider
current_angle = values  # Actualiza el ángulo actual

# Dibujar el gráfico que representa el ángulo
fig, ax = plt.subplots(figsize=(3, 3))  # Tamaño más pequeño

# Dibujar la línea horizontal (amarilla)
ax.plot([-1, 1], [0, 0], color='black', lw=6)

# Invertir la lógica del ángulo para que 0 grados apunte hacia arriba
angle_rad = np.deg2rad(current_angle)
x = np.sin(angle_rad)  # Coordenada x
y = np.cos(angle_rad)  # Coordenada y

ax.plot([0, x], [0, y], 'r-', lw=4)

# Título de la gráfica
ax.set_title("Representación gráfica del movimiento", fontsize=12)

# Configuración de los ejes
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')

# Ocultar las etiquetas de los ejes
ax.set_xticks([])
ax.set_yticks([])

# Mostrar el gráfico en Streamlit
st.pyplot(fig)
