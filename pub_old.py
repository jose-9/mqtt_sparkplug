import time
import random
from paho.mqtt import client as mqtt_client
import socket

# MQTT Broker details (update the broker IP as needed)
broker = '127.0.0.1'
port = 1883
topic = "MQTT_Tags_sampa"
client_id = f'publisher-{random.randint(0, 100)}'

# Credentials
username = 'admin'
password = 'admin'

# Connection test function
def test_connection(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=5):
            print(f"Successfully connected to {ip}:{port}")
    except Exception as e:
        print(f"Could not connect to {ip}:{port}: {e}")

# Verify connection
test_connection(broker, port)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id=client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
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
