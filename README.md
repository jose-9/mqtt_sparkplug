# ideal-waffle

## using sparkplub

1. install all needed packages
pip install protobuf paho-mqtt
*protobuf library must be use within linux*

*Sparkplug B Python Library: Ensure you have access to the sparkplug_b_pb2 module, which typically comes from Sparkplug B’s Protocol Buffer schema. You might need to compile the .proto file from the Eclipse Tahu GitHub repository if it’s not already available.*


2. Define the Sparkplug B Payload: Use Sparkplug B’s standard format with protobuf for encoding.

3. Set Up Topic Structure: Sparkplug B topic format follows spBv1.0/{group_id}/{message_type}/{edge_node_id}/{device_id}.


## HOW
### Step 1: Install Protocol Buffers Compiler
To generate the Python code from the Sparkplug B .proto files, you first need the Protocol Buffers compiler (protoc).

On Debian/Ubuntu:

*bash*
sudo apt update
sudo apt install -y protobuf-compiler


On Windows:

Download the appropriate protoc binary from GitHub’s releases page for Protobuf.
Extract the downloaded file and add the directory containing protoc.exe to your system's PATH.


On Mac:

*bash*
brew install protobuf

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




### Trouble shooting
#### File location
Here are the steps:

Navigate to the Directory: Change to the tahu directory where the .proto file is located:

*bash*
cd path/to/tahu
Run the protoc Command with Path: Now, generate the Python file by running:

*bash*
protoc --python_out=. sparkplug_b/sparkplug_b.proto


#### File version
The error you're seeing suggests that the protobuf version installed is incompatible with the generated sparkplug_b_pb2.py file. Here are a few ways to resolve it:

Solution 1: Downgrade the protobuf Version
One common workaround is to downgrade the protobuf library to a compatible version, such as 3.20.x. You can install it with the following command:

*bash*
pip install protobuf==3.20.*
Solution 2: Regenerate the sparkplug_b_pb2.py File
If you have protoc installed (version >= 3.19.0), you can regenerate the .py file to ensure compatibility with the latest protobuf version.

Navigate to the directory containing your .proto file (e.g., tahu/sparkplug_b/) and run:

*bash*
protoc --python_out=. sparkplug_b.proto