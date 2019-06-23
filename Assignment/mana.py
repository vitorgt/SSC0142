#!/usr/bin/python3

import server
import operator


storage = {
    "TEMP": [],
    "HUMI": [],
    "CO2L": [],
}

limits = {
    "TEMP": {
        "MAX": [32.0],
        "MIN": [20.0]
    },
    "HUMI": {
        "MIN": [0.6]
    },
    "CO2L": {
        "MIN": [550.0]
    }
}

actuators = {
    "HEAT": {
        "on": False,
        "manualOn": False,
        "sensorData": storage["TEMP"],
        "limit": limits["TEMP"]["MIN"],
        "startConditional": operator.lt,
        "endConditional": operator.gt,
    },
    "COOL": {
        "on": False,
        "manualOn": False,
        "sensorData": storage["TEMP"],
        "limit": limits["TEMP"]["MAX"],
        "startConditional": operator.gt,
        "endConditional": operator.lt,
    },
    "WATE": {
        "on": False,
        "manualOn": False,
        "sensorData": storage["HUMI"],
        "limit": limits["HUMI"]["MIN"],
        "startConditional": operator.lt,
        "endConditional": operator.gt,
    },
    "CO2I": {
        "on": False,
        "manualOn": False,
        "sensorData": storage["CO2L"],
        "limit": limits["CO2L"]["MIN"],
        "startConditional": operator.lt,
        "endConditional": operator.gt,
    }
}


def sensor(sck):
    """Receive `PUT` from Sensors."""
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
            storage[sck.ID].append(float(data[3]))


def sendActuatorSwitch(sck, onoff):
    """Send `PUT` to Actuators."""
    ack = False
    while not ack:
        string = "|PUT|" + sck.ID + "|" + onoff + "|"
        if sck.server.v:
            print(sck.server.ID + " -> " + sck.ID + ": " + string)
        sck.conn.send(bytes(string, "utf-8"))
        data = None
        try:
            data = sck.conn.recv(1024)
        except Exception:
            print("Timed out: \"" + sck.server.ID +
                  " -> " + sck.ID + ": " + string + "\"")
            print("Retrying")
        if data:
            if sck.server.v:
                print(sck.server.ID + " <- " +
                      sck.ID + ": " + str(data, "utf-8"))
            data = str(data, "utf-8").split("|")
            if data[1] == "ACK" and data[2] == "PUT":
                ack = True
                # if onoff is "ON" it stores True, else False
                actuators[sck.ID]["on"] = (onoff == "ON")


def actuator(sck):
    """Check conditions to turn Actuators on and off."""
    if sck.server.v:
        print(sck.ID + " logged in")
    act = actuators[sck.ID]
    while True:
        try:
            # It can be turned on:
            # If it's not on
            if not act["on"]:
                # If it's manually set on
                if act["manualOn"]:
                    sendActuatorSwitch(sck, "ON")
                # If there's data to compare to the limit
                if len(act["sensorData"]) != 0:
                    # If the data violates the conditional
                    if act["startConditional"](
                            act["sensorData"][-1],
                            act["limit"][0]
                    ):
                        sendActuatorSwitch(sck, "ON")
            # It can be turned off:
            # If it's on
            else:
                # If it isn't manually set on
                if not act["manualOn"]:
                    # If there's data to compare to the limit
                    if len(act["sensorData"]) != 0:
                        # If the data doesn't violates the conditional
                        if act["endConditional"](
                            act["sensorData"][-1],
                            act["limit"][0]
                        ):
                            sendActuatorSwitch(sck, "OFF")
        except OSError:  # If connection error:
            print(sck.ID + " disconnected")
            print(sck.server.ID + " disconnecting from " + sck.ID)
            sck.conn.close()
            return


def clie(sck):
    """Receive protocols from Client, send proper replies."""
    if sck.server.v:
        print(sck.ID + " logged in")
    while True:
        # Receives query
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
        # Parse query, building the reply
        for x in range(len(data)):
            if data[x] == "GET":
                if data[x + 1] in actuators:
                    response += "|PUT|" + data[x + 1] + "|"
                    response += ["OFF", "ON"][actuators[data[x + 1]]["on"]]
                    response += "|"
                else:
                    if len(storage[data[x + 1]]) > 0:
                        response += "|PUT|" + data[x + 1] + "|"
                        response += str(storage[data[x + 1]][-1]) + "|"
                    else:
                        response += "|PUT|" + data[x + 1] + "|None|"
            elif data[x] == "PUT":
                actuators[data[x + 1]]["manualOn"] = (data[x + 2] == "ON")
                if sck.server.v:
                    print("Client", sck.addr, "manually setting",
                          data[x + 1], data[x + 2])
                response = "|ACK|PUT|"
            elif data[x] == "DEF":
                limits[data[x + 1]][data[x + 2]][0] = float(data[x + 3])
                if sck.server.v:
                    print("Client", sck.addr, "manually setting",
                          data[x + 2], data[x + 1], "to", data[x + 3])
                response = "|ACK|DEF|"
        if sck.server.v:
            print(sck.server.ID + " <- " + sck.ID + ": " + response)
        try:
            sck.conn.send(bytes(response, "utf-8"))
        except OSError:  # If connection error:
            print(sck.ID + " disconnected")
            print(sck.server.ID + " disconnecting from " + sck.ID)
            sck.conn.close()
            return


def mana(serverThread):
    """Categorize which function to call based on connection's ID."""
    if serverThread.ID in actuators:
        actuator(serverThread)
    elif serverThread.ID == "CLIE":
        clie(serverThread)
    else:
        sensor(serverThread)


if __name__ == "__main__":
    server.Server(7777, "MANA", mana)
