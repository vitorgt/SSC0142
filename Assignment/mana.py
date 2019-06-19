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
max_temp = [22]
min_temp = [20]
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
            try:
                data = sck.conn.recv(1024)
            except Exception:
                pass
            if data:
                break
        if sck.server.v:
            print(sck.server.ID+" <- "+sck.ID+": "+str(data, "utf-8"))
        data = str(data, "utf-8").split("|")
        if data[1] == "PUT" and data[2] == sck.ID:
            storage[sck.ID].append(float(data[3]))


def sendActuatorSwitch(sck, infos, onoff):
    ack = False
    while not ack:
        string = "|PUT|"+sck.ID+"|"+onoff+"|"
        if sck.server.v:
            print(sck.server.ID+" -> "+sck.ID+": "+string)
        sck.conn.send(bytes(string, "utf-8"))
        data = None
        try:
            data = sck.conn.recv(1024)
        except Exception:
            print("Timed out: \""+sck.server.ID+" -> "+sck.ID+": "+string+"\"")
            print("Retrying")
        if data:
            if sck.server.v:
                print(sck.server.ID+" <- "+sck.ID+": "+str(data, "utf-8"))
            data = str(data, "utf-8").split("|")
            if data[1] == "ACK" and data[2] == "PUT":
                ack = True
                infos[3][0] = (onoff == "ON")  # if "ON" it stores True, else False


def actuator(sck, infos):
    if sck.server.v:
        print(sck.ID+" logged in")
    while True:
        if len(infos[0]) != 0 and infos[1](infos[0][-1], infos[2][0]) and not infos[3][0]:
            sendActuatorSwitch(sck, infos, "ON")
        if len(infos[0]) != 0 and infos[4](infos[0][-1], infos[2][0]) and infos[3][0]:
            sendActuatorSwitch(sck, infos, "OFF")


def mana(serverThread):
    if serverThread.ID in actuators:
        actuator(serverThread, actuators[serverThread.ID])
    elif serverThread.ID == "CLIE":
        pass
    else:
        sensor(serverThread)


if __name__ == "__main__":
    manager = server.Server(7777, "MANA", mana)
