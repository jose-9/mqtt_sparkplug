import random
from paho.mqtt import client as mqtt_client
from sparkplug_b import sparkplug_b_pb2  # Import the Sparkplug B protobuf schema

# MQTT Broker details
broker = '127.0.0.1'  # Replace with your broker's IP
port = 1883

# Sparkplug B topic details
group_id = "myGroup"
message_type = "NDATA"  # "NDATA" for node data
edge_node_id = "myEdgeNode"
device_id = "myDevice"
topic = f"spBv1.0/{group_id}/{message_type}/{edge_node_id}/{device_id}"
client_id = f'subscriber-{random.randint(0, 100)}'

def connect_mqtt():
    client = mqtt_client.Client(client_id=client_id)

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def parse_sparkplug_payload(payload):
    # Deserialize the Sparkplug B payload
    sparkplug_payload = sparkplug_b_pb2.Payload()
    sparkplug_payload.ParseFromString(payload)
    
    # Display received metrics
    print("Received Sparkplug B message:")
    print(f"Timestamp: {sparkplug_payload.timestamp}")
    for metric in sparkplug_payload.metrics:
        print(f"Metric Name: {metric.name}")
        print(f"Alias: {metric.alias}")
        print(f"Value: {metric.int_value if metric.HasField('int_value') else 'N/A'}")
        print("-" * 30)

def subscribe(client):
    def on_message(client, userdata, msg):
        print(f"Received message from topic `{msg.topic}`")
        parse_sparkplug_payload(msg.payload)  # Parse and display the Sparkplug B payload

    client.subscribe(topic)
    client.on_message = on_message

if __name__ == '__main__':
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
