import sys
import random
import time
from datetime import datetime
from Adafruit_IO import MQTTClient
import cv2
from detectors import mask_detector

AIO_FEED_IDS = ['button1', 'button2']
AIO_USERNAME = 'khoadtran'
AIO_KEY = 'aio_Xpay75BJoHjjw9LeIfyfe187KdbX'

def connected(client):
  print("Connected...")
  for id in AIO_FEED_IDS:
    client.subscribe(id)

def subscribe(client , userdata , mid , granted_qos):
  print("Subscribed...")

def disconnected(client):
  print("Disconnected...")
  sys.exit (1)

def message(client , feed_id , payload):
  print(f"Receive data: {feed_id} - {payload}")

client = MQTTClient(username=AIO_USERNAME , key=AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

counter = 5
sensor_counter = -1

def send_sensor_data(sensor_key, data):
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  print(f'Sending data to {sensor_key} at {current_time}: {data}')
  client.publish(sensor_key, data)
  
# def random_data(sensor_type):
#   match sensor_type:
#     case 1:
#       return random.randint(0, 100)
#     case 2:
#       return random.randint(0, 500)
#     case 3:
#       return random.randint(15, 60)

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

while True:
  if counter <= 0:
    counter = 5
    sensor_counter += 1
    sensor_type = sensor_counter % 3 + 1
    
    # match sensor_type:
    #   case 1:
    #     send_sensor_data('sensor1', random_data(sensor_type))
    #   case 2:
    #     send_sensor_data('sensor2', random_data(sensor_type))
    #   case 3:
    #     send_sensor_data('sensor3', random_data(sensor_type))
    
    
    
    _, image = camera.read()
    mask_result = mask_detector(image)
    send_sensor_data('ai', mask_result)
    
  
  counter -= 1
  time.sleep(1)
  pass



camera.release()
cv2.destroyAllWindows()
