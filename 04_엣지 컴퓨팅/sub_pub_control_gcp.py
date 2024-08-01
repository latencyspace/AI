import paho.mqtt.client as mqtt
import pandas as pd
import datetime

def pub_buzzer_on():
  print('pub_buzzer_on!!')
  mqttc = mqtt.Client()      # MQTT Client 
  mqttc.connect("test.mosquitto.org", 1883)    # MQTT 
  mqttc.publish("icore-sdp/buzzer", "on")  
  mqttc.loop(2)  

def pub_motor_on():
  print('pub_motor_on!!')
  mqttc = mqtt.Client()
  mqttc.connect("test.mosquitto.org", 1883)    # MQTT 
  mqttc.publish("icore-sdp/dc_motor", "on")

def pub_motor_off():
  print('pub_motor_off!!')
  mqttc = mqtt.Client()
  mqttc.connect("test.mosquitto.org", 1883)
  mqttc.publish("icore-sdp/dc_motor", "off")  # 'hello/world'  "Hello World!"
  mqttc.loop(2) 

def on_connect(client, userdata, flags,rc):
  print ("Connected with result code " + str(rc))
  client.subscribe("icore-sdp/temp_humi")

def on_message(client, userdata, msg):
  s = str(msg.payload.decode('utf-8')).split()
  temp = float(s[0][s[0].find('T:')+2:])
  humi = float(s[1][s[1].find('H:')+2:])

  # 현재 시간 가져오기
  now = datetime.datetime.now()

  # 지정된 포맷으로 문자열 생성
  timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
  print('time:',timestamp,'temp:',temp, 'humi:',humi)

  if temp > 27.0:
     pub_buzzer_on()
     pub_motor_on()
  else:
     pub_motor_off()
      

client = mqtt.Client()        # MQTT Client 
client.on_connect = on_connect     # on_connect callback 
client.on_message = on_message     # on_message callback 

client.connect("test.mosquitto.org", 1883, 60)   # MQTT 

client.loop_forever()
