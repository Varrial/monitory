import paho.mqtt.client as mqtt  # import the client1

from services.read import getData

BROKER_ADDRESS = getData("Adres_Brokera")
TOPIC = getData("Topic")
L = getData("Lewy")
P = getData("Prawy")

class MqttService:
    def __init__(self, client_id, userdata, clean_session=True):
        self.client = mqtt.Client(client_id=client_id, userdata=userdata,
                                  clean_session=clean_session)  # create new instance
        self.client.on_connect = self.onConnect

    def connect(self):
        self.client.connect(BROKER_ADDRESS)

    def onConnect(self, client, userdata, flags, rc):
        self.client.subscribe(TOPIC + L)
        self.client.subscribe(TOPIC + P)