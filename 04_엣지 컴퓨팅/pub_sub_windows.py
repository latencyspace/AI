# ! pip install paho-mqtt
# python.exe -m pip install --upgrade pip

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags,rc):
    print ("Connected with result code " + str(rc))
    client.subscribe("hello/world")

# def on_message(client, userdata, msg):
#   print ("Topic: ", msg.topic + '\nMessage: ' + str(msg.payload))

def on_message(client, user_data, msg):
    print('message : ' + str(msg.payload.decode('utf-8')))
    
    
client = mqtt.Client()        # MQTT Client 
client.on_connect = on_connect     # on_connect callback 
client.on_message = on_message   # on_message callback 

client.connect("test.mosquitto.org", 1883, 60)   # MQTT 
#client.connect("localhost", 1883, 60)   # iCORE-SDP Broker 

client.loop_forever()
---------------------------------------------------------
import paho.mqtt.client as mqtt

mqttc = mqtt.Client()      # MQTT Client 
mqttc.connect("test.mosquitto.org", 1883)    # MQTT 
#mqttc.connect("localhost", 1883)    # iCORE-SDP Broker 
mqttc.publish("hello/world", "I am Raspberry!! Hello World!")  # 'hello/world'  "Hello World!"
mqttc.loop(2)        # timeout = 2