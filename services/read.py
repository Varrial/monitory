def getData(wartosc):
    f = open("/home/pi/Monitory/properties.txt", "r").read().split('\n')
    for line in f:
        if not line.find(wartosc):
            return line[len(wartosc)+2:]
