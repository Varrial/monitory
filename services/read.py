def getData(wartosc):
    try:
        f = open("properties.txt", "r").read().split('\n')  # wywołanie przez folder w ktorym znajduje sie program
    except:
        f = open("/home/pi/monitory/properties.txt", "r").read().split('\n')  # wywołanie przez crontab
    finally:
        for line in f:
            if not line.find(wartosc):
                return line[len(wartosc)+2:]
