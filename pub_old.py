import time
import random
from paho.mqtt import client as mqtt_client

# MQTT Broker details (update the broker IP as needed)
broker = '127.0.0.1'
port = 1883
topic = "blablabla"
client_id = f'publisher-{random.randint(0, 100)}'

def connect_mqtt():
    client = mqtt_client.Client(client_id=client_id)
    client.connect(broker, port)
    return client

def publish(client):
    while True:
        msg = f"Hello MQTT {random.randint(1, 100)}"
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Sent `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        time.sleep(5)

if __name__ == '__main__':
    client = connect_mqtt()
    publish(client)
