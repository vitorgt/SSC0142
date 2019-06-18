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
            serverData.append(int(data[3]))


def humi(st, serverData):
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


def co2L(st, serverData):
    print("hi co2 level from server")

def heat(st, serverData):
    while True:
        if len(tempData) != 0 and tempData[-1] < min_temp and not serverData:
            serverData = True
            if st.server.v:
                print(st.server.ID+" -> "+st.ID+": "+"|PUT|HEAT|ON|")
            st.conn.send(bytes("|PUT|HEAT|ON|", "utf-8"))
        if len(tempData) != 0 and tempData[-1] > min_temp and serverData:
            serverData = False
            if st.server.v:
                print(st.server.ID+" -> "+st.ID+": "+"|PUT|HEAT|OFF|")
            st.conn.send(bytes("|PUT|HEAT|OFF|", "utf-8"))

def cool(st, serverData):
    while True:
        if len(tempData) != 0 and tempData[-1] > max_temp and not serverData:
            serverData = True
            if st.server.v:
                print(st.server.ID+" -> "+st.ID+": "+"|PUT|COOL|ON|")
            st.conn.send(bytes("|PUT|COOL|ON|", "utf-8"))
        if len(tempData) != 0 and tempData[-1] < max_temp and serverData:
            serverData = False
            if st.server.v:
                print(st.server.ID+" -> "+st.ID+": "+"|PUT|COOL|OFF|")
            st.conn.send(bytes("|PUT|COOL|OFF|", "utf-8"))


tempData = []
humiData = []
co2lData = []
heatData = False
coolData = False
wateData = False
co2iData = False
max_temp = 32
min_temp = 15

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
    "HUMI": humi,
    "CO2L": co2L,
    "HEAT": heat,
    "COOL": cool
}


def mana(serverThread):
    functions[serverThread.ID](serverThread, storage[serverThread.ID])


if __name__ == "__main__":
    manager = server.Server(7777, "MANA", mana)
