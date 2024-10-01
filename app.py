import paho.mqtt.client as paho
import time
import streamlit as st
import json
import matplotlib.pyplot as plt
import numpy as np

values = 0.0
act1 = "OFF"
current_angle = 0.0  # Variable para almacenar el ángulo actual

def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("MOTOR_WEB_APP")
client1.on_message = on_message

st.title("Controla tu servo con esta aplicación")

if st.button('Encender el motor'):
    act1 = "ON"
    client1 = paho.Client("MOTOR_WEB_APP")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Act1": act1})
    ret = client1.publish("OFF_ON", message)

elif st.button('Apagar el motor'):
    act1 = "OFF"
    client1 = paho.Client("MOTOR_WEB_APP")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Act1": act1})
    ret = client1.publish("OFF_ON", message)

values = st.slider('Selecciona el ángulo de giro de su servo', 0.0, 180.0)
st.write('Valores:', values)

if st.button('Enviar valor de ángulo al servo'):
    current_angle = values  # Actualiza el ángulo actual
    client1 = paho.Client("MOTOR_WEB_APP")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    ret = client1.publish("CHANGE_ANGLE", message)

    # Mostrar el ángulo actual
    st.write(f"Ángulo actual del servo: {current_angle}°")

    # Visualizar el ángulo usando Matplotlib con un tamaño más pequeño
    fig, ax = plt.subplots(figsize=(3, 3))  # Tamaño más pequeño

    # Dibujar la línea horizontal
    ax.plot([-1, 1], [0, 0], 'k-', lw=2)

    # Calcular la posición final de la línea basada en el ángulo actual
    if current_angle <= 90:
        # Invertir el comportamiento para ángulos menores o iguales a 90 (debajo de la línea horizontal)
        angle_rad = np.deg2rad(90 - current_angle)
    else:
        # Invertir el comportamiento para ángulos mayores a 90 (arriba de la línea horizontal)
        angle_rad = np.deg2rad(90 - current_angle)

    # Coordenadas de la línea
    x = np.cos(angle_rad)  # Coordenada x
    y = np.sin(angle_rad)  # Coordenada y

    # Invertir la dirección del eje y para ángulos mayores a 90 (arriba de la línea horizontal)
    if current_angle > 90:
        y = -y

    # Dibujar la línea que representa el ángulo
    ax.plot([0, x], [0, y], 'r-', lw=4)

    # Configuración de los ejes
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')

    # Ocultar las etiquetas de los ejes
    ax.set_xticks([])
    ax.set_yticks([])

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

else:
    st.write('')
