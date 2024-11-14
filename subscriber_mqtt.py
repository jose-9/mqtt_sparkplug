import random
from paho.mqtt import client as mqtt_client
from tahu.sparkplug_b import sparkplug_b_pb2
# from sparkplug_b import sparkplug_b_pb2  # Import the generated Sparkplug B protobuf definitions

# MQTT Broker details
broker = 'broker.emqx.io'
port = 1883
topic = "spBv1.0/mygroup_id/NBIRTH/my_node_id"
client_id = f'sparkplug_subscriber_{random.randint(0, 1000)}'

def connect_mqtt():
    client = mqtt_client.Client(client_id=client_id)
    client.connect(broker, port)
    return client


def decode_payload(payload_bytes):
    """Decode a Sparkplug B payload from bytes."""
    payload = sparkplug_b_pb2.Payload()
    payload.ParseFromString(payload_bytes)
    return payload


def on_message(client, userdata, msg):
    print(f"Received message from topic `{msg.topic}`")
    # Decode the Sparkplug B payload
    payload = decode_payload(msg.payload)
    
    # Iterate over metrics in the payload and print them
    for metric in payload.metrics:
        print(f"Metric Name: {metric.name}")
        # if metric.datatype == sparkplug_b_pb2.Payload.Metric.Int32:
        if metric.datatype == sparkplug_b_pb2.DataType.Int32:
            print(f"INT32 Value: {metric.int_value}")
        # Add handling for other metric types as needed


def subscribe(client):
    client.subscribe(topic)
    client.on_message = on_message


if __name__ == '__main__':
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
