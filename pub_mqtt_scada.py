import time
import random
import sys
import os
import socket

from paho.mqtt import client as mqtt_client

sys.path.append(os.path.join(os.path.dirname(__file__), 'tahu', 'python', 'core'))

try:
    import sparkplug_b_pb2
except ImportError as e:
    print(f"Error importing Sparkplug B library: {e}")
    sys.exit(1)

# MQTT Broker details
broker = "127.0.0.1"
port = 1883

#Set Up Topic Structure: Sparkplug B topic format follows 
#spBv1.0/{group_id}/{message_type}/{edge_node_id}/{device_id}.

topic = "spBv1.0/LARI/DDATA/nodetest/gyroscope"
client_id = f'sparkplug_publisher_{random.randint(0, 1000)}'

# Sparkplug B details
# namespace = "spBv1.0"  # Sparkplug namespace
# group_id = "LARI"
# node_id = "nodetest"
# device_id = "gyroscope"

sequence_number = 1
birth_topic = "spBv1.0/LARI/NBIRTH/nodetest"

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

def generate_random_pump_state():
    #Generates a random pump state value (0, 1, or 2).
    return random.randint(0, 2)

def create_nbirth_payload(sequence_number):
    payload = sparkplug_b_pb2.Payload()
    payload.timestamp = int(time.time() * 1000)
    payload.seq = 0  # Sequence number for NBIRTH is always 0

    # Add Node Control Metric (required for Sparkplug compliance)
    control_metric = payload.metrics.add()
    control_metric.name = "Node Control/Rebirth"
    control_metric.alias = 1
    control_metric.datatype = sparkplug_b_pb2.DataType.Boolean
    control_metric.boolean_value = False

    return payload


def create_dbirth_payload(sequence_number):
    """Creates a Sparkplug B payload for device birth."""
    payload = sparkplug_b_pb2.Payload()
    payload.timestamp = int(time.time() * 1000)
    payload.seq = 1

    # Define initial metrics for the device
    pump_metric = payload.metrics.add()
    pump_metric.name = "pump_state"
    pump_metric.alias = 1
    pump_metric.datatype = sparkplug_b_pb2.DataType.Int32
    pump_metric.int_value = 0  # Initialize to 0

    return payload


def create_ddata_payload(pump_state, sequence_number):
    """Creates a Sparkplug B payload for device data updates."""
    payload = sparkplug_b_pb2.Payload()
    payload.timestamp = int(time.time() * 1000)
    payload.seq = sequence_number  # Incrementing sequence number for DDATA

    # Add pump state metric
    pump_metric = payload.metrics.add()
    pump_metric.name = "pump_state"
    pump_metric.alias = 1
    pump_metric.datatype = sparkplug_b_pb2.DataType.Int32
    pump_metric.int_value = pump_state  # Use dynamically generated value

    return payload


def publish(client):
    global sequence_number 

    # Send NBIRTH
    print("Sending NBIRTH message")
    nbirth_payload = create_nbirth_payload(sequence_number)
    client.publish(birth_topic, nbirth_payload.SerializeToString())
    print(f"Sent NBIRTH message to topic `{birth_topic}`")

    time.sleep(5)  # Allow time for broker to process NBIRTH

    # Send DBIRTH
    print("Sending DBIRTH message")
    dbirth_topic = f"spBv1.0/LARI/DBIRTH/nodetest/gyroscope"
    dbirth_payload = create_dbirth_payload(sequence_number)
    client.publish(dbirth_topic, dbirth_payload.SerializeToString())
    print(f"Sent DBIRTH message to topic `{dbirth_topic}`")
    sequence_number += 1

    time.sleep(5)  # Allow time for broker to process DBIRTH

    # Send periodic DDATA
    while True:
        pump_state = generate_random_pump_state()
        ddata_payload = create_ddata_payload(pump_state, sequence_number)
        result = client.publish(topic, ddata_payload.SerializeToString())

        status = result[0]
        if status == 0:
            print(f"Sent DDATA to topic `{topic}` with pump state: {pump_state}, sequence: {sequence_number}")
        else:
            print(f"Failed to send DDATA to topic `{topic}`")
        sequence_number += 1
        time.sleep(2)

if __name__ == '__main__':
    client = connect_mqtt()
    publish(client)
