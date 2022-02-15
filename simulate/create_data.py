import time
import json

import paho.mqtt.client as mqtt  # import the client1
from services.PreviousData import getPrevious

lista = getPrevious(15, 22, "trak1")

if len(lista) == 0:
    print("Lista pusta")

broker_address = "localhost"

client = mqtt.Client("client1")  # create new instance
client.connect(broker_address)  # connect to broker
client.subscribe("hala1/maszyny/wielopila1")

for i in lista:
    time.sleep(1)
    client.publish("hala1/maszyny/wielopila1", json.dumps({'nazwa': "wielopila1", 'posuw_mb': i['PRAD'], 'posuw_skok': i['POSUW_KROK'], 'prad': i['POSUW'], 'zolty_sygn': i['ZOLTY'], 'zielony_sygn': i['ZIELONY'], 'impuls': 0}))
    print("publikuje")

(i['PRAD'], 0, i['POSUW'], 0, i['ZOLTY'], i['DATA_SERWER'])