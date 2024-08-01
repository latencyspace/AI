from google.cloud import bigquery
import pandas as pd
import paho.mqtt.client as mqtt
import datetime

# tabel ID
table_id = "andong-24-adv-idv-130.pi3_sensor.temp_humi"

schema = [
    bigquery.SchemaField("timestamp", "TIMESTAMP"),
    bigquery.SchemaField("temperature", "FLOAT"),
    bigquery.SchemaField("humidity", "FLOAT"),
]

def write_to_bq(data):
  client = bigquery.Client()
  dataframe = pd.DataFrame(data, columns=["timestamp", "temperature", "humidity"])

  # Load the data into a new table.
  job_config = bigquery.LoadJobConfig(
      schema=schema,
      write_disposition=bigquery.WriteDisposition.WRITE_APPEND)
  job = client.load_table_from_dataframe(dataframe, table_id, job_config=job_config)

  job.result()  # Wait for the job to complete.

  print("Loaded {} rows.".format(job.output_rows))

def on_connect(client, userdata, flags,rc):
  print ("Connected with result code " + str(rc))
  client.subscribe("icore-sdp/temp_humi")

def on_message(client, userdata, msg):
  # print ("Topic: ", msg.topic + '\nMessage: ' + str(msg.payload))
  s = str(msg.payload.decode('utf-8')).split()
  temp = float(s[0][s[0].find('T:')+2:])
  humi = float(s[1][s[1].find('H:')+2:])

  # 현재 시간 가져오기
  now = datetime.datetime.now()

  # 지정된 포맷으로 문자열 생성
  timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
  print('time:',timestamp,'temp:',temp, 'humi:',humi) 

  data = [
    (pd.to_datetime(timestamp), temp, humi)
  ]

  write_to_bq(data)	
  # print ("Topic: ", msg.topic + '\nMessage: ' + str(msg.payload.decode('euc-kr'))) # 완성형 (windows)
  # print ("Topic: ", msg.topic + '\nMessage: ' + str(msg.payload.decode('utf-8')))  # 조합형 (linux,mac)

client = mqtt.Client()        # MQTT Client 
client.on_connect = on_connect     # on_connect callback 
client.on_message = on_message     # on_message callback 

client.connect("test.mosquitto.org", 1883, 60)   # MQTT 
#client.connect("localhost", 1883, 60)   # iCORE-SDP Broker 

client.loop_forever()
