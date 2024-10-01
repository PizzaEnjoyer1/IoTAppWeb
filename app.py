import paho.mqtt.client as paho
import time
import streamlit as st
import json
import pandas as pd

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
    
else:
    st.write('')

if st.button('Apagar el motor'):
    act1 = "OFF"
    client1 = paho.Client("MOTOR_WEB_APP")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Act1": act1})
    ret = client1.publish("OFF_ON", message)
    
else:
    st.write('')

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
    
    # Crear un gráfico para mostrar el ángulo
    df = pd.DataFrame({'Ángulo': [current_angle]})
    st.bar_chart(df)

else:
    st.write('')
