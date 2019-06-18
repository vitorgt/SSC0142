#!/usr/bin/python3

import server
import operator


tempData = []
humiData = []
co2lData = []
heatData = [False]
coolData = [False]
wateData = [False]
co2iData = [False]
max_temp = [32]
min_temp = [15]
min_co2l = [6]
min_wate = [0.9]

actuators = {
    "HEAT": [tempData, operator.lt, min_temp, heatData, operator.gt],
    "COOL": [tempData, operator.gt, max_temp, coolData, operator.lt],
    "WATE": [humiData, operator.lt, min_wate, wateData, operator.gt],
    "CO2I": [co2lData, operator.lt, min_co2l, co2iData, operator.gt]
}

storage = {
    "TEMP": tempData,
    "HUMI": humiData,
    "CO2L": co2lData,
    "HEAT": heatData,
    "COOL": coolData,
    "WATE": wateData,
    "CO2I": co2iData
}


def sensor(sck):
    if sck.server.v:
        print(sck.ID+" logged in")
    while True:
        while True:
            data = sck.conn.recv(1024)
            if data:
                break
        if sck.server.v:
            print(sck.server.ID+" <- "+sck.ID+": "+str(data, "utf-8"))
        data = str(data, "utf-8").split("|")
        if data[1] == "PUT" and data[2] == sck.ID:
            storage[sck.ID].append(float(data[3]))


def actuator(sck, infos):
    if sck.server.v:
        print(sck.ID+" logged in")
    while True:
        if len(infos[0]) != 0 and infos[1](infos[0][-1], infos[2]) and not infos[3]:
            infos[3][0] = True
            string = "|PUT|"+sck.ID+"|ON|"
            if sck.server.v:
                print(sck.server.ID+" -> "+sck.ID+": "+string)
            sck.conn.send(bytes(string, "utf-8"))
        if len(infos[0]) != 0 and infos[4](infos[0][-1], infos[2]) and infos[3]:
            infos[3][0] = False
            string = "|PUT|"+sck.ID+"|OFF|"
            if sck.server.v:
                print(sck.server.ID+" -> "+sck.ID+": "+string)
            sck.conn.send(bytes(string, "utf-8"))


def mana(serverThread):
    if serverThread.ID in actuators:
        actuator(serverThread, actuators[serverThread.ID])
    else:
        sensor(serverThread)


if __name__ == "__main__":
    manager = server.Server(7777, "MANA", mana)
