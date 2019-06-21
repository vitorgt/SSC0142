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
heatManu = [False]
coolManu = [False]
wateManu = [False]
co2iManu = [False]
max_temp = [32]
min_temp = [20]
min_humi = [0.6]
min_co2l = [550]

limits = {
    "TEMP": {
        "MAX": max_temp,
        "MIN": min_temp
    },
    "HUMI": {
        "MIN": min_humi
    },
    "CO2L": {
        "MIN": min_co2l
    }
}

mannuals = {
    "HEAT": heatManu,
    "COOL": coolManu,
    "WATE": wateManu,
    "CO2I": co2iManu
}

actuators = {
    "HEAT": [tempData, operator.lt, min_temp, heatData, operator.gt, heatManu],
    "COOL": [tempData, operator.gt, max_temp, coolData, operator.lt, coolManu],
    "WATE": [humiData, operator.lt, min_humi, wateData, operator.gt, wateManu],
    "CO2I": [co2lData, operator.lt, min_co2l, co2iData, operator.gt, co2iManu]
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
        data = None
        while not data:
            try:
                data = sck.conn.recv(1024)
            except Exception:
                pass
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
        try:
            if (len(infos[0]) != 0 and infos[1](infos[0][-1], infos[2][0]) and not infos[3][0]) or infos[5][0]:
                sendActuatorSwitch(sck, infos, "ON")
            if len(infos[0]) != 0 and infos[4](infos[0][-1], infos[2][0]) and infos[3][0] and not infos[5][0]:
                sendActuatorSwitch(sck, infos, "OFF")
        except OSError:
            print(sck.ID+" disconnected")
            print(sck.server.ID+" disconnecting from "+sck.ID)
            sck.conn.close()
            return

def clie(sck):
    if sck.server.v:
        print(sck.ID+" logged in")
    while True:
        data = None
        while not data:
            try:
                data = sck.conn.recv(1024)
            except Exception:
                pass
        if sck.server.v:
            print(sck.server.ID+" <- "+sck.ID+": "+str(data, "utf-8"))
        data = str(data, "utf-8").split("|")
        response = ""
        for x in range(len(data)):
            if data[x] == "GET":
                if len(storage[data[x+1]]) > 0:
                    if data[x+1] in actuators:
                        response += "|PUT|"+data[x+1]+"|"+["OFF","ON"][storage[data[x+1]][-1]]+"|"
                    else:
                        response += "|PUT|"+data[x+1]+"|"+str(storage[data[x+1]][-1])+"|"
                else:
                    response += "|PUT|"+data[x+1]+"|None|"
            elif data[x] == "PUT":
                mannuals[data[x+1]][0] = (data[x+2] == "ON")
                if sck.server.v:
                    print("Client",sck.addr,"mannually setting",data[x+1],data[x+2])
                response = "|ACK|PUT|"
            elif data[x] == "DEF":
                limits[data[x+1]][data[x+2]][0] = float(data[x+3])
                if sck.server.v:
                    print("Client",sck.addr,"mannually setting",data[x+2],data[x+1],"to",data[x+3])
                response = "|ACK|DEF|"
        if sck.server.v:
            print(sck.server.ID+" <- "+sck.ID+": "+response)
        try:
            sck.conn.send(bytes(response, "utf-8"))
        except OSError:
            print(sck.ID+" disconnected")
            print(sck.server.ID+" disconnecting from "+sck.ID)
            sck.conn.close()
            return


def mana(serverThread):
    if serverThread.ID in actuators:
        actuator(serverThread, actuators[serverThread.ID])
    elif serverThread.ID == "CLIE":
        clie(serverThread)
    else:
        sensor(serverThread)


if __name__ == "__main__":
    manager = server.Server(7777, "MANA", mana)
