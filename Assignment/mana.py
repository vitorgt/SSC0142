#!/usr/bin/python3

import server


class Storage:
    def __init__(self):
        self.on = False
        self.data = []


storage = {
    "TEMP": Storage(),
    "HUMI": Storage(),
    "CO2L": Storage(),
    "HEAT": Storage(),
    "COOL": Storage(),
    "WATE": Storage(),
    "CO2I": Storage()
}


def readID(st):
    while True:
        data = st.conn.recv(1024)
        if data:
            break
    data = str(data, "utf-8").split("|")
    if st.manager.v:
        print("MANA received:", data)
    if "CON" == data[1]:
        if st.manager.v:
            print("MANA sending:  |ACK"+"|".join(data))
        st.conn.send(bytes("|ACK"+"|".join(data), "utf-8"))
        return data[2]
    else:
        print(data)
        raise ConnectionRefusedError("unknown protocol received")


def mana(serverThread):
    try:
        ID = readID(serverThread)
    except Exception as e:
        print(e)
    else:
        clientStorage = storage[ID]


if __name__ == "__main__":
    manager = server.Server(7777, mana)

# maybe it'll be necessary
#https://realpython.com/python-sockets/
