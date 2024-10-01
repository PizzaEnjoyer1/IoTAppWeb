import paho.mqtt.client as paho
import time
import streamlit as st
import json
import numpy as np
import matplotlib.pyplot as plt

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

    # Crear el gráfico de la aguja
    fig, ax = plt.subplots()
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)

    # Dibuja la aguja
    angle_rad = np.deg2rad(current_angle)  # Convierte a radianes
    ax.plot([0, np.cos(angle_rad)], [0, np.sin(angle_rad)], lw=5, color='r')

    # Dibuja un círculo para representar el eje
    circle = plt.Circle((0, 0), 1, color='b', fill=False)
    ax.add_artist(circle)

    # Ajustar el aspecto
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')  # Quita los ejes

    st.pyplot(fig)  # Muestra la figura en Streamlit

else:
    st.write('')
