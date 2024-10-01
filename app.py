import paho.mqtt.client as paho
import time
import streamlit as st
import json

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

    # Generar HTML para la aguja
    st.markdown(
        f"""
        <div style="position: relative; width: 200px; height: 200px;">
            <div style="position: absolute; width: 100%; height: 100%; border: 2px solid black; border-radius: 50%;"></div>
            <div style="position: absolute; width: 2px; height: 90px; background: red; 
                transform-origin: bottom center; 
                transform: rotate({current_angle}deg); 
                bottom: 50%; left: 50%; margin-left: -1px; margin-bottom: -90px;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.write('')
