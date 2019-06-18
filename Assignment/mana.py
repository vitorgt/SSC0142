#!/usr/bin/python3

import server


class Storage:
    def __init__(self):
        self.on = False
        self.data = []


storages = {
    "TEMP": Storage(),
    "HUMI": Storage(),
    "CO2L": Storage(),
    "HEAT": Storage(),
    "COOL": Storage(),
    "WATE": Storage(),
    "CO2I": Storage()
}


def mana(serverThread):
    clientStorage = storages[serverThread.ID]
    clientStorage.on = True


if __name__ == "__main__":
    manager = server.Server(7777, "MANA", mana)
