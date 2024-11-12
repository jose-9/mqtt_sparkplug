# Use a lightweight Python image as the base
FROM python:3.11-slim

# Install paho-mqtt
RUN pip install paho-mqtt==1.6.1

# Copy both scripts to the container
COPY publisher_mqtt.py /app/publisher_mqtt.py
COPY subscriber_mqtt.py /app/subscriber_mqtt.py

# Set the working directory
WORKDIR /app

# Default command to run the script (can be overridden by the `docker run` command)
CMD ["python", "publisher_mqtt.py"]
