import socket


def handler(skt, manager):
    if manager.v:
        print("sensor temperature handler actvated")
    while True:
        while True:
            data = skt.conn.recv(1024)
            if data:
                break
        if manager.v:
            print("temp handler received: " + str(data, "utf-8"))
        instance = str(data, "utf-8").split("|")
        if instance[1] == "TEMP":
            if instance[3] == "C":
                pass
            elif instance[3] == "F":
                instance[2] = (instance[2] - 32) * 5 / 9
            elif instance[3] == "K":
                instance[2] = instance[2] - 273.15
            manager.temp.data.append(instance[2])
