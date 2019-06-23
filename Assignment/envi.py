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
    """Send status to Sensors."""
    if sck.server.v:
        print(sck.ID + " logged in")
    while True:
        string = "|PUT|" + sck.ID + "|" + str(status[sck.ID]) + "|"
        if sck.server.v:
            print(sck.server.ID + " -> " + sck.ID + ": " + string)
        try:
            sck.conn.send(bytes(string, "utf-8"))
        except OSError:  # If connection error:
            print(sck.ID + " disconnected")
            print(sck.server.ID + " disconnecting from " + sck.ID)
            sck.conn.close()
            return
        time.sleep(0.5)


def actuator(sck):
    """Receive status' changes from Actuators."""
    if sck.server.v:
        print(sck.ID + " logged in")
    while True:
        data = None
        while not data:
            try:
                data = sck.conn.recv(1024)
            except Exception:
                pass
        if sck.server.v:
            print(sck.server.ID + " <- " + sck.ID + ": " + str(data, "utf-8"))
        data = str(data, "utf-8").split("|")
        if data[1] == "PUT" and data[2] == sck.ID:
            status[actuators[sck.ID][0]] = actuators[sck.ID][1](
                status[actuators[sck.ID][0]], float(data[3]))


def clie(sck):
    """Receive status' changes from Client and reply."""
    if sck.server.v:
        print(sck.ID + " logged in")
    while True:
        data = None
        while not data:
            try:
                data = sck.conn.recv(1024)
            except Exception:
                pass
        if sck.server.v:
            print(sck.server.ID + " <- " + sck.ID + ": " + str(data, "utf-8"))
        data = str(data, "utf-8").split("|")
        response = ""
        for x in range(len(data)):
            if data[x] == "PUT":
                status[data[x + 1]] = float(data[x + 2])
                if sck.server.v:
                    print("Client", sck.addr, "manually setting",
                          data[x + 1], "to", data[x + 2])
                response = "|ACK|PUT|"
        if sck.server.v:
            print(sck.server.ID + " <- " + sck.ID + ": " + response)
        try:
            sck.conn.send(bytes(response, "utf-8"))
        except OSError:  # If connection error:
            print(sck.ID + " disconnected")
            print(sck.server.ID + " disconnecting from " + sck.ID)
            sck.conn.close()
            return


def envi(serverThread):
    """Categorize which function to call based on connection's ID."""
    if serverThread.ID in actuators:
        actuator(serverThread)
    elif serverThread.ID == "CLIE":
        clie(serverThread)
    else:
        sensor(serverThread)


@server.threaded
def enviRand(status):
    """Change status randomly."""
    while True:
        status["TEMP"] += random.random()*2-1  # [-1, 1]
        status["HUMI"] += random.random()*0.25-0.125  # [-0.125, 0.125]
        if status["HUMI"] > 1:
            status["HUMI"] = 1
        if status["HUMI"] < 0:
            status["HUMI"] = 0
        status["CO2L"] += random.random()*500-350  # [-350, 150]
        if status["CO2L"] < 0:
            status["CO2L"] = 0
        time.sleep(random.randint(0, 3))


if __name__ == "__main__":
    enviRand(status)
    server.Server(8888, "ENVI", envi)
