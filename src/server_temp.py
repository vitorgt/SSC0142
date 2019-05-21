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
        data = str(data, "utf-8").split("|")
        if data[1] == "POST" and data[2] == "TEMP":
            if data[4] == "C":
                pass
            elif data[4] == "F":
                data[3] = (data[3] - 32) * 5 / 9
            elif data[4] == "K":
                data[3] = data[3] - 273.15
            manager.temp.data.append(data[3])
