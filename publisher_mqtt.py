import time
import random
import sys
import os
from paho.mqtt import client as mqtt_client

sys.path.append(os.path.join(os.path.dirname(__file__), 'tahu', 'python', 'core'))
# import sparkplug_b_pb2

try:
    import sparkplug_b_pb2
except ImportError as e:
    print(f"Error importing Sparkplug B library: {e}")
    sys.exit(1)


# MQTT Broker details
broker = 'broker.emqx.io'
port = 1883
topic = "spBv1.0/mygroup_id/NBIRTH/my_node_id"
client_id = f'sparkplug_publisher_{random.randint(0, 1000)}'

# Sparkplug B details
namespace = "spBv1.0"  # Sparkplug namespace
group_id = "mygroup_id"
node_id = "my_node_id"
device_id = "my_device_id"


def connect_mqtt():
    client = mqtt_client.Client(client_id=client_id)
    client.connect(broker, port)
    return client


def create_payload():
    """Creates a Sparkplug B payload for publishing"""
    payload = sparkplug_b_pb2.Payload()

    # Set timestamp
    payload.timestamp = int(time.time() * 1000)

    # Add a metric (example)
    metric = payload.metrics.add()
    metric.name = "temperature"
    metric.alias = 1
    metric.timestamp = payload.timestamp
    # Assuming you want to use Int32 as the datatype for a metric
    metric.datatype = sparkplug_b_pb2.DataType.Int32

    # metric.datatype = sparkplug_b_pb2.Payload.Metric.Int32
    metric.int_value = random.randint(20, 30)  # Random temperature data

    return payload


def publish(client):
    while True:
        payload = create_payload()
        # Serialize the payload to bytes for Sparkplug B
        payload_bytes = payload.SerializeToString()
        
        # Publish the message to the MQTT broker
        result = client.publish(topic, payload_bytes)
        status = result[0]
        if status == 0:
            print(f"Sent Sparkplug message to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        
        time.sleep(5)  # Adjust the interval as needed


if __name__ == '__main__':
    client = connect_mqtt()
    publish(client)
