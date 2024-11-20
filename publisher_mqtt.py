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
topic = "spBv1.0/LARI/DDATA/my_node_id/my_device_id"
# topic = "spBv1.0/LARI/NBIRTH/nodetest"
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

sequence_number = 1
birth_topic = "spBv1.0/LARI/NBIRTH/my_node_id"

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

def generate_random_axis_values():
    """Generates random float values for X, Y, and Z axes."""
    return {
        'X': random.uniform(-4.0, 4.0),
        'Y': random.uniform(-4.0, 4.0),
        'Z': random.uniform(-4.0, 4.0)
    }

def create_nbirth_payload(sequence_number):
    payload = sparkplug_b_pb2.Payload()

    payload.timestamp = int(time.time() * 1000)

    payload.seq=sequence_number

    node_metric = payload.metrics.add()
    node_metric.name = "node_id"
    node_metric.float_value = 0.0  # This could represent a static value or be used differently based on your system
    node_metric.datatype = sparkplug_b_pb2.DataType.String  # Representing node as a string value


    return payload

def create_ddata_payload(axis_data, sequence_number):
    """Creates a Sparkplug B payload for publishing"""
    payload = sparkplug_b_pb2.Payload()

    # Set timestamp
    payload.timestamp = int(time.time() * 1000)

    # Set sequence number
    payload.seq = sequence_number

    axes = {'X': 1, 'Y': 2, 'Z': 3}
    for axis, alias in axes.items():
        # Add a metric (example)
        metric = payload.metrics.add()
        metric.name = f"axis_{axis}"
        metric.alias = alias
        metric.timestamp = payload.timestamp
        # metric.datatype = sparkplug_b_pb2.DataType.Int32
        # metric.int_value = random.randint(2, 30)  # Random temperature data
        metric.datatype = sparkplug_b_pb2.DataType.Float
        metric.float_value = axis_data[axis]  # Use the pre-generated axis data

    return payload


def publish(client):
    global sequence_number 

    print("Sending Nbirth message")
    nbirth_payload = create_nbirth_payload(sequence_number)
    nbirth_payload_bytes = nbirth_payload.SerializeToString()

    client.publish(birth_topic, nbirth_payload_bytes)
    print(f"Sent Nbirth message to topic `{birth_topic}`")
    sequence_number += 1

    while True:
        axis_data = generate_random_axis_values()
        payload = create_ddata_payload(axis_data, sequence_number)  # Use the data and sequence number to create the payload

        # Serialize the payload to bytes for Sparkplug B
        payload_bytes = payload.SerializeToString()
        
        # Publish the message to the MQTT broker
        result = client.publish(topic, payload_bytes)
        status = result[0]
        if status == 0:
            print(f"Sent Sparkplug message to topic `{topic}` with axis data: {axis_data}, sequence: {sequence_number}")
            # print(f"Sent Sparkplug {int_value} to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        
        sequence_number += 1
        
        time.sleep(5)  # Adjust the interval as needed


if __name__ == '__main__':
    client = connect_mqtt()
    publish(client)
