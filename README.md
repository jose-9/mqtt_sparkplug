# Installation

## To start playing in a Windows environment
> git clone https://github.com/jose-9/mqtt_sparkplug.git

> pip install -r requirements.txt

> mkdir .\protoc-28.3-win64;  tar -xf protoc-28.3-win64.zip -C .\protoc-28.3-win64

> git clone https://github.com/eclipse/tahu.git

### inside requirements
*protoc-28.3-win64.zip is being used to have a standard project, not garanted to work for others versions

1. Automatic installation of all needed packages
protobuf paho-mqtt
*protobuf library must be use within linux*

*Sparkplug B Python Library: Ensure you have access to the sparkplug_b_pb2 module, which typically comes from Sparkplug B’s Protocol Buffer schema. You might need to compile the .proto file from the Eclipse Tahu GitHub repository if it’s not already available.*

2. Define the Sparkplug B Payload: Use Sparkplug B’s standard format with protobuf for encoding.


## HOW
### Step 1: Install Protocol Buffers Compiler
To generate the Python code from the Sparkplug B .proto files, you first need the Protocol Buffers compiler (protoc).


### Step 2: Download the Sparkplug B .proto File
The Sparkplug B .proto files are available in the Eclipse Tahu repository.

Clone the Tahu repository:

*bash*
git clone https://github.com/eclipse/tahu.git
Navigate to the directory containing the .proto files:

*bash*
cd tahu/proto
Step 3: Generate Python Code from the .proto File
Use the protoc command to generate Python classes from the .proto file:

*bash*
protoc --python_out=. sparkplug_b.proto


# How to use
python publisher.py


# Trouble shooting
### File location
Here are the steps:

Navigate to the Directory: Change to the tahu directory where the .proto file is located:

*bash*
cd path/to/tahu
Run the protoc Command with Path: Now, generate the Python file by running:

*bash*
protoc --python_out=. sparkplug_b/sparkplug_b.proto


### File version
The error you're seeing suggests that the protobuf version installed is incompatible with the generated sparkplug_b_pb2.py file. Here are a few ways to resolve it:

Solution 2: Regenerate the sparkplug_b_pb2.py File
If you have protoc installed (version >= 3.19.0), you can regenerate the .py file to ensure compatibility with the latest protobuf version.

Navigate to the directory containing your .proto file (e.g., tahu/sparkplug_b/) and run:

*bash*
protoc --python_out=. sparkplug_b.proto

### Datatype error
Here's how you might update your publisher_mqtt.py script:

python
'''
 Assuming you want to use Int32 as the datatype for a metric
metric.datatype = sparkplug_b_pb2.DataType.Int32
Make sure each datatype assignment in your script matches exactly with the DataType names defined in the .proto file, like Int8, Int16, Int32, etc.
'''

Re-generate the Python Bindings (If Not Done Already)
If you haven’t done this after defining the .proto file, use protoc to generate the updated Python bindings:

*bash*
protoc --python_out=. tahu/sparkplug_b/sparkplug_b.proto