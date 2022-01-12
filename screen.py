import datetime
import json
import random

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import paho.mqtt.client as mqtt  # import the client1

import textlabel
from services.DataMQTT import MqttService
from services.read import getData
from services.PreviousData import getPrevious
from models.Maszyna import maszyna

REFRESH = int(getData("Odswiezanie"))
#zmianaI = int(getData("zmiana1"))
#zmianaII = int(getData("zmiana2"))

class Screen(BoxLayout):
    L = maszyna(getData("Lewy"), REFRESH)
    P = maszyna(getData("Prawy"), REFRESH)
    tekst1 = getData("Tekst1")
    tekst2 = getData("Tekst2")
    tekst3 = getData("Tekst3")
    tekst4 = getData("Tekst4")
    tekst5 = getData("Tekst5")
    tekst6 = getData("Tekst6")
    tekst7 = getData("Tekst7")
    font = getData("RozmiarTekstu")

    def Pplus(self):
        now = datetime.datetime.now()
        czas = now - self.P.prev_czas
        
        #if self.P.prev_czas.hour == zmianaI-1 and now.hour == zmianaI:
        #    self.P.clear()
        #elif self.P.prev_czas.hour == zmianaII-1 and now.hour == zmianaII:
        #    self.P.clear()   Przesuniete do crontab -e

        self.P.prev_czas = now
        self.P.wyrownaj_czas(czas)
        self.ids.Psr_prad_pracy.text = str(self.P.sr_prad_pracy())
        self.ids.Pilosc_mb.text = str(int(self.P.ilosc_mb))
        self.ids.Pc_faktycznej_pracy.text = self.P.czas_text("c_faktycznej_pracy")
        self.ids.Pc_pracy_na_pusto.text = self.P.czas_text("c_pracy_na_pusto")
        self.ids.Pc_wyl_maszyny.text = self.P.czas_text("c_wyl_maszyny")
        self.ids.Pgodz_rzpoczecia.text = self.P.czas_rozpoczecia

    def Lplus(self):
        now = datetime.datetime.now()
        czas = now - self.L.prev_czas
        
        

        #if self.L.prev_czas.hour == zmianaI-1 and now.hour == zmianaI:
        #    self.L.clear()
        #elif self.L.prev_czas.hour == zmianaII-1 and now.hour == zmianaII:
        #    self.L.clear()

        self.L.prev_czas = now
        self.L.wyrownaj_czas(czas)
        self.ids.Lsr_prad_pracy.text = str(self.L.sr_prad_pracy())
        self.ids.Lilosc_mb.text = str(int(self.L.ilosc_mb))
        self.ids.Lc_faktycznej_pracy.text = self.L.czas_text("c_faktycznej_pracy")
        self.ids.Lc_pracy_na_pusto.text = self.L.czas_text("c_pracy_na_pusto")
        self.ids.Lc_wyl_maszyny.text = self.L.czas_text("c_wyl_maszyny")
        self.ids.Lgodz_rzpoczecia.text = self.L.czas_rozpoczecia

    def start(self):
# ten fragment odpowiada za uzupełnianie rekordów z bazy jesli nastąpiła awaria
        # godzina = datetime.datetime.now().hour
        # godzina = 8  # do testowania
        # if 6 < godzina and 22 > godzina:
        #     tabL = []
        #     tabP = []
        #     if 14 > godzina: #pierwsza zmiana
        #         tabL = getPrevious(6, 14, self.L.nazwa_wew)
        #         tabP = getPrevious(6, 14, self.P.nazwa_wew)
        #     else:           # druga zmiana
        #         tabL = getPrevious(14, 22, self.L.nazwa_wew)
        #         tabP = getPrevious(14, 22, self.P.nazwa_wew)
        #
        #     for i in tabL:
        #         self.L.dodajInfo(i['PRAD'], 0, i['POSUW'], 0, i['ZOLTY'], i['DATA_SERWER'])
        #
        #     for i in tabP:
        #         self.P.dodajInfo(i['PRAD'], 0, i['POSUW'], 0, i['ZOLTY'], i['DATA_SERWER'])
# koniec fragmentu

        Clock.schedule_interval(self.zegar, REFRESH)

    def zegar(self, dt):
        self.Pplus()
        self.Lplus()


class ScreenApp(App):

    def build(self):
        self.scr = Screen()
        self.scr.start()
        # self.mqtt_service = MqttService()

        return self.scr

    def on_start(self):
        def onMessage(client, userdata, msg):  # co z odbieranymi danymi
            wiadomosc = json.loads(msg.payload)
            nazwa = wiadomosc["nazwa"]
            posuw_mb = wiadomosc["posuw_mb"]
            posuw_skok = wiadomosc["posuw_skok"]
            prad = wiadomosc["prad"]
            zolty_sygnal = wiadomosc["zolty_sygn"]
            zielony_sygnal = wiadomosc["zielony_sygn"]
            impuls = wiadomosc["impuls"]

            if (nazwa == userdata['self'].scr.L.nazwa_wew):
                userdata['self'].scr.L.dodajInfo(posuw_mb, posuw_skok, prad, impuls, zolty_sygnal)
                
            
            elif (nazwa == userdata['self'].scr.P.nazwa_wew):
                userdata['self'].scr.P.dodajInfo(posuw_mb, posuw_skok, prad, impuls, zolty_sygnal)

            # print(msg.payload)

        parameters = {'self': self}

        try:
            mqttc = MqttService(client_id=getData("Klient"), clean_session=True, userdata=parameters)
            mqttc.client.on_message = onMessage

            mqttc.connect()
            mqttc.client.loop_start()  # start loop to process callbacks! (new thread!)
        except:
            print("no mqtt ")


if __name__ == '__main__':
    if (getData("Fullscreen") == "T" or getData("Fullscreen") == "t"):
        # Window.size = (1920, 1080)
        Window.fullscreen = True
        Window.show_cursor = False

    ScreenApp().run()
