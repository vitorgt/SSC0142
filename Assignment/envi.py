#!/usr/bin/python3

import time
import server
import random
import operator


status = {
    "TEMP": 10.0,
    "HUMI": 0.6,
    "CO2L": 550.0
}

actuators = {
    "HEAT": ["TEMP", operator.add],
    "COOL": ["TEMP", operator.sub],
    "WATE": ["HUMI", operator.add],
    "CO2I": ["CO2L", operator.add]
}


def sensor(sck):
    if sck.server.v:
        print(sck.ID+" logged in")
    while True:
        string = "|PUT|"+sck.ID+"|"+str(status[sck.ID])+"|"
        if sck.server.v:
            print(sck.server.ID+" -> "+sck.ID+": "+string)
        try:
            sck.conn.send(bytes(string, "utf-8"))
        except BrokenPipeError:
            print(sck.ID+" disconnected")
            print(sck.server.ID+" disconnecting from "+sck.ID)
            sck.conn.close()
        time.sleep(1)


def actuator(sck):
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
            status[actuators[sck.ID][0]] = actuators[sck.ID][1](
                status[actuators[sck.ID][0]], float(data[3]))


def envi(serverThread):
    if serverThread.ID in actuators:
        actuator(serverThread)
    elif serverThread.ID == "CLIE":
        pass
    else:
        sensor(serverThread)


@server.threaded
def enviRand(status):
    while True:
        status["TEMP"] += random.random()*2-1  # [-1, 1]
        status["HUMI"] += random.random()*0.25-0.125  # [-0.125, 0.125]
        if status["HUMI"] > 1:
            status["HUMI"] = 1
        if status["HUMI"] < 0:
            status["HUMI"] = 0
        status["CO2L"] += random.random()*500-250  # [-250, 250]
        if status["CO2L"] < 0:
            status["CO2L"] = 0
        time.sleep(random.randint(0, 3))


if __name__ == "__main__":
    enviRand(status)
    environment = server.Server(8888, "ENVI", envi)
