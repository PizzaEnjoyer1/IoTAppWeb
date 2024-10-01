import paho.mqtt.client as paho
import time
import streamlit as st
import json
values = 0.0
act1="OFF"

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

        


broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("MOTOR_WEB_APP")   #DEBE CAMBIARSE CADA VEZ QUE SE CREA UNA NUEVA APLICACIÓN. EN ESTE CASO, ES EL PUBLISHER 
client1.on_message = on_message



st.title("Controla tu motor con esta aplicación")

if st.button('Encender el motor'):
    act1="ON"
    client1= paho.Client("MOTOR_WEB_APP")           #CAMBIO NECESARIO                      
    client1.on_publish = on_publish                          
    client1.connect(broker,port)  
    message =json.dumps({"Act1":act1})
    ret= client1.publish("OFF_ON", message)         #CAMBIO NECESARIO 
 
    #client1.subscribe("Sensores")
    
    
else:
    st.write('')

if st.button('Apagar el motor'):
    act1="OFF"
    client1= paho.Client("MOTOR_WEB_APP")         #CAMBIO NECESARIO                   
    client1.on_publish = on_publish                          
    client1.connect(broker,port)  
    message =json.dumps({"Act1":act1})
    ret= client1.publish("OFF_ON", message)        #AL SER EL TÓPICO, TAMBIÉN DEBE CAMBIARSE SU NOMBRE (EN TODAS LAS INSTANCIAS PRESENTES); DEBE SER IGUAL AL QUE TIENE EL SUBSCRIBER
  
    
else:
    st.write('')

values = st.slider('Selecciona el ángulo de giro de su servo',0.0, 180.0)
st.write('Values:', values)

if st.button('Enviar valor de ángulo al servo'):
    client1= paho.Client("MOTOR_WEB_APP")            #CAMBIO NECESARIO                
    client1.on_publish = on_publish                          
    client1.connect(broker,port)   
    message =json.dumps({"Analog": float(values)})
    ret= client1.publish("CHANGE_ANGLE", message)    #AL IGUAL QUE EL OTRO TÓPICO, TAMBIÉN TIENE QUE SER CAMBIADO; DEBE SER IGUAL AL QUE TIENE EL SUBSCRIBER
    
 
else:
    st.write('')




