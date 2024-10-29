import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, client_id, broker_address="127.0.0.1", broker_port=1883):
        self.client = mqtt.Client(client_id)
        self.broker_address = broker_address
        self.broker_port = broker_port

        # Connect to the local MQTT broker
        self.client.connect(self.broker_address, self.broker_port)
        self.client.loop_start()  # Start the loop to process network traffic

    def subscribe(self, topic):
        self.client.subscribe(topic)
        self.client.on_message = self.on_message_callback

    def on_message_callback(self, client, userdata, message):
        self.last_message = message.payload.decode("utf-8")

    def get_data(self):
        return getattr(self, 'last_message', None)
