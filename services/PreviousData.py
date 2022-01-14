import requests
import json
import datetime
from services.read import getData

def getPrevious(od, do, maszyna):
    # prad zamieniony z posowem

    ip = getData("Adres_Brokera")
    port = "88"
    if ip[0] == "9":
        port = "888"
        data = datetime.datetime.now()
        # data -= datetime.timedelta(days=4)  # dzien poprzedni - do testowania w nocy
        data = data.strftime("%Y-%m-%d")

    r = requests.post("http://" + ip + ":" + port + "/pobierz_dane_czas.php",
        json={  'ID': "65jww4A7",
                'name': maszyna,
                'czas_od_h': od,
                'czas_do_h': do, # zawsze wykonuje sie do zmiany ponieważ powyżej odpowiedzieniego czasu nei ma juz rekordow w bazie
                'czas_od_min': 0,
                'czas_do_min': 0,
                'data': data # dzisiejsza data w formacie yyyy-mm-dd
             })
    return json.loads(r.text)
