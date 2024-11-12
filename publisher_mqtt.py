import time
import random
from paho.mqtt import client as mqtt_client
from sparkplug_b import sparkplug_b_pb2  # Import the Sparkplug B protobuf schema

# MQTT Broker details
broker = '127.0.0.1'  # Replace with your broker's IP
port = 1883

# Sparkplug B topic and client details
group_id = "myGroup"
message_type = "NDATA"  # "NDATA" for node data, "DATAB" for device data, etc.
edge_node_id = "myEdgeNode"
device_id = "myDevice"
client_id = f'publisher-{random.randint(0, 100)}'
topic = f"spBv1.0/{group_id}/{message_type}/{edge_node_id}/{device_id}"

def create_sparkplug_payload():
    # Create Sparkplug B payload
    payload = sparkplug_b_pb2.Payload()
    payload.timestamp = int(time.time() * 1000)  # Timestamp in milliseconds
    
    # Define metrics as per Sparkplug B format, e.g., a simple integer metric
    metric = payload.metrics.add()
    metric.name = "exampleMetric"
    metric.alias = 1  # Alias is a unique identifier for this metric
    metric.timestamp = payload.timestamp
    metric.int_value = random.randint(0, 100)  # Random integer for demonstration
    
    return payload.SerializeToString()

def connect_mqtt():
    client = mqtt_client.Client(client_id=client_id)
    client.connect(broker, port)
    return client

def publish(client):
    while True:
        # Create Sparkplug B formatted payload
        msg = create_sparkplug_payload()
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Sent Sparkplug B message to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        time.sleep(5)

if __name__ == '__main__':
    client = connect_mqtt()
    publish(client)
