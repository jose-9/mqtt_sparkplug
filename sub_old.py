import random
from paho.mqtt import client as mqtt_client

# MQTT Broker details (update the broker IP as needed)
broker = '127.0.0.1'
port = 1883
topic = "blablabla"
client_id = f'subscriber-{random.randint(0, 100)}'

def connect_mqtt():
    client = mqtt_client.Client(client_id=client_id)

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message

if __name__ == '__main__':
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
