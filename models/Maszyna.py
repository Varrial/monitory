import datetime
from services.read import getData


class maszyna:
    def __init__(self, nazwa, refresh, ilosc_mb=0, c_faktycznej_pracy=0, c_pracy_na_pusto=0, c_wyl_maszyny=0):


        if (nazwa[:-1] == "wielopila"):
            if nazwa[-1:] == '1':
                self.wartosc_minimalna_amperow = float(getData("Ampery WieloPila1"))
            elif nazwa[-1:] == '2':
                self.wartosc_minimalna_amperow = float(getData("Ampery WieloPila2"))
            self.wspolczynnik = 0.9  # wielopila1, 2 i 3
            self.nazwa = "WieloPiła" + " " + nazwa[-1:]

        elif (nazwa[:-1] == "trak"):
            self.wartosc_minimalna_amperow = float(getData("Ampery Traki"))
            if nazwa[-1:] == '1':
                self.wspolczynnik = 0.66
            elif nazwa[-1:] == '3':
                self.wspolczynnik = 0.64
            self.nazwa = "Trak" + " " + nazwa[-1:]


        # pusta godzina rozpoczecia
        self.czas_rozpoczecia = " "
        self.czas_nieliczony = 0

        # Wszystkie czasy wyrazane są w sekundach
        self.ilosc_mb = ilosc_mb
        self.c_faktycznej_pracy = float(c_faktycznej_pracy)
        self.c_pracy_na_pusto = float(c_pracy_na_pusto)
        self.c_wyl_maszyny = float(c_wyl_maszyny)

        self.nazwa_wew = nazwa
        self.prev_czas = datetime.datetime.now()
        self.prady = 0  # suma wszystkich pradow
        self.prady_ilosc = 0 # ilosc pradow - po podzieleniu srednia

    def wyrownaj_czas(self, czas):
        tmp = czas.seconds + ((czas.microseconds)/1000000)
        self.c_wyl_maszyny += tmp

    def czas_text(self, typ_urz):
        tmp = self.c_faktycznej_pracy

        if (typ_urz == "c_pracy_na_pusto"):
            tmp = self.c_pracy_na_pusto
        elif (typ_urz == "c_wyl_maszyny"):
            tmp = self.c_wyl_maszyny

        # if tmp < 0:  # sytuacja po odzyskiwaniu rekordów - brak ustalonego obecnego czasu
        #     tmp = 28000 + tmp BLAD NAPRAWIONY

        s = int(tmp)

        procent = int(round(s / 28800 * 100, 0))


        czas = ""
        m = 0
        h = 0
        if s >= 60:
            m = s // 60
            s -= m * 60
        if m >= 60:
            h = m // 60
            m -= h * 60

        if h > 0:
            czas += f"{h}h "
        # if m > 0 or h > 0:
        czas += f"{m}m "
        # czas += f"{s}s" sekundy

        czas += f"({procent}%)"

        return czas

    def dodajInfo(self, posuw_mb, posuw_skok, prad, impuls, zolty, data=datetime.datetime.now().__str__()):
        posuw_mb = float(posuw_mb)
        # posuw_skok = float(posuw_skok)
        prad = float(prad)
        # impuls = int(impuls)
        zolty = int(zolty)

        if prad > self.wartosc_minimalna_amperow:
            if self.nazwa_wew != "wielopila2" or posuw_mb > 3.6:
                if zolty == 1:
                    self.c_pracy_na_pusto += 1.0
                else:
                    if self.czas_rozpoczecia == " ":
                        if self.czas_nieliczony < 60:
                            self.czas_nieliczony += 1
                        else:
                            # if data == "null":
                            #     data = data=datetime.datetime.now().__str__()
                            # Kamil odkomentowanie tego oraz ustawienie daty domyslnej na "null" (string) prawdopodobnie
                            # rozwiązuje moj problem, ale troche jestem ciekawy kiedy tu zajrzysz ;-)
                            self.czas_rozpoczecia = data[11:16]
                    self.c_faktycznej_pracy += 1.0
                    self.ilosc_mb += posuw_mb / 60 * self.wspolczynnik
                    self.prady += prad
                    self.prady_ilosc += 1

                self.c_wyl_maszyny -= 1.0

    def sr_prad_pracy (self):
        if self.prady_ilosc == 0:
            return "0 A"
        return str(round(self.prady/self.prady_ilosc, 1)) + " A"

    def clear (self):  # obecnie nie używane
        self.prady = 0
        self.prady_ilosc = 0
        self.ilosc_mb = 0
        self.c_faktycznej_pracy = 0
        self.c_pracy_na_pusto = 0
        self.c_wyl_maszyny = 0
