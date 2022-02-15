import paho.mqtt.client as mqtt

def on_messag(client, userdata, msg):
    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg

broker_address="localhost"

client = mqtt.Client("P299")  # create new instance
client.on_message = on_messag
client.connect(broker_address)  # connect to broker
client.subscribe("hala1/maszyny/wielopila1")
client.subscribe("test")

client.loop_forever()
client.loop_stop()