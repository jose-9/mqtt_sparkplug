import time
import random
import sys
import os
import socket

from paho.mqtt import client as mqtt_client

sys.path.append(os.path.join(os.path.dirname(__file__), 'tahu', 'python', 'core'))
# import sparkplug_b_pb2

try:
    import sparkplug_b_pb2
except ImportError as e:
    print(f"Error importing Sparkplug B library: {e}")
    sys.exit(1)


# MQTT Broker details
broker = "127.0.0.1"
# broker = 'broker.emqx.io'
port = 1883
# topic = "spBv1.0/mygroup_id/NBIRTH/my_node_id"
topic = "spBv1.0/LARI/NBIRTH/nodetest"
client_id = f'sparkplug_publisher_{random.randint(0, 1000)}'

# Sparkplug B details
namespace = "spBv1.0"  # Sparkplug namespace
# group_id = "mygroup_id"
# node_id = "my_node_id"
# device_id = "my_device_id"

# namespace = "sparkLARI"  # Sparkplug namespace
group_id = "G20"
node_id = "nodelet"
device_id = "devv"

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
    client = mqtt_client.Client(client_id=client_id)

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
   
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client




def create_payload(seq=0):
    """Creates a Sparkplug B payload for publishing"""
    payload = sparkplug_b_pb2.Payload()

    # Set timestamp
    payload.timestamp = int(time.time() * 1000)

    # Set sequence number
    payload.seq = seq

    # Add a metric (example)
    metric = payload.metrics.add()
    metric.name = ""
    metric.alias = 1
    metric.timestamp = payload.timestamp
    metric.datatype = sparkplug_b_pb2.DataType.Int32
    metric.int_value = random.randint(2, 30)  # Random temperature data

    return payload,metric.int_value


def publish(client):
    while True:
        payload,int_value = create_payload()
        # Serialize the payload to bytes for Sparkplug B
        payload_bytes = payload.SerializeToString()
        
        # Publish the message to the MQTT broker
        result = client.publish(topic, payload_bytes)
        status = result[0]
        if status == 0:
            print(f"Sent Sparkplug {int_value} to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        
        time.sleep(5)  # Adjust the interval as needed


if __name__ == '__main__':
    client = connect_mqtt()
    publish(client)
