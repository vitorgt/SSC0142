#!/usr/bin/python3

import server


def temp(st, serverData):
    if st.server.v:
        print(st.ID+" activated")
    while True:
        while True:
            data = st.conn.recv(1024)
            if data:
                break
        if st.server.v:
            print(st.server.ID+" <- "+st.ID+": "+str(data, "utf-8"))
        data = str(data, "utf-8").split("|")
        if data[1] == "PUT" and data[2] == st.ID:
            serverData.append(data[3])



def humi(st, serverData):
    print("hi humi from server")


tempData = []
humiData = []
co2lData = []
heatData = False
coolData = False
wateData = False
co2iData = False

storage = {
    "TEMP": tempData,
    "HUMI": humiData,
    "CO2L": co2lData,
    "HEAT": heatData,
    "COOL": coolData,
    "WATE": wateData,
    "CO2I": co2iData
}

functions = {
    "TEMP": temp,
    "HUMI": humi
}


def mana(serverThread):
    functions[serverThread.ID](serverThread, storage[serverThread.ID])


if __name__ == "__main__":
    manager = server.Server(7777, "MANA", mana)
