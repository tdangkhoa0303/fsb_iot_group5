import sys
import time
import cv2
from datetime import datetime
from Adafruit_IO import MQTTClient
from uart import *

AIO_FEED_IDS = ["button1", "button2", "button3"]
AIO_USERNAME = ""
AIO_KEY = ""


def connected(client):
    print("Connected...")
    for id in AIO_FEED_IDS:
        client.subscribe(id)


def subscribe(client, userdata, mid, granted_qos):
    print("Subscribed...")


def disconnected(client):
    print("Disconnected...")
    sys.exit(1)


def message(client, feed_id, payload):
    print(f"Receive data: {feed_id} - {payload}")
    if feed_id == "button1":
        if payload == "0":
            write_data("0")
        else:
            write_data("1")
    if feed_id == "button2":
        if payload == "0":
            write_data("3")
        else:
            write_data("2")
    if feed_id == "button3":
        if payload == "0":
            write_data("5")
        else:
            write_data("4")


client = MQTTClient(username=AIO_USERNAME, key=AIO_KEY)
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
    print(f"Sending data to {sensor_key} at {current_time}: {data}")
    client.publish(sensor_key, data)


# CAMERA can be 0 or 1 based on default camera of your computer
# camera = cv2.VideoCapture(0)

while True:
    if counter <= 0:
        counter = 5
        sensor_counter += 1
        sensor_type = sensor_counter % 3 + 1
        # _, image = camera.read()
        # mask_result = mask_detector(image)
        # send_sensor_data('ai', mask_result)

    read_serial(client)

    counter -= 1
    time.sleep(1)
    pass


# camera.release()
# cv2.destroyAllWindows()
