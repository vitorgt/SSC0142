#!/usr/bin/python3

import time
import client

# Sends CO2 to Manager
on = False


def mana(client):
    while True:
        data = client.sck.recv(1024)
        if data:
            break
    if client.v:
        print(client.ID+" <- "+client.target+": "+str(data, "utf-8"))
    data = str(data, "utf-8").split("|")
    if data[1] == "PUT" and data[2] == client.ID:
        if data[3] == "ON":
            on = True
        else:
            on = False


# Receives CO2 from Environment
def envi(client):
    if on:
        while True:
            time.sleep(10)
            if client.v:
                print(client.ID, "-> ENVI: |PUT|"+client.ID+"|3|")
            client.sck.send(bytes("|PUT|"+client.ID+"|3|", "utf-8"))


if __name__ == "__main__":
    HOST, v = client.inputs()
    if HOST != None:
        client.Client(7777, "CO2I", "MANA", mana, v, HOST).start()
        client.Client(8888, "CO2I", "ENVI", envi, v, HOST).start()
    else:
        client.Client(7777, "CO2I", "MANA", mana, v).start()
        client.Client(8888, "CO2I", "ENVI", envi, v).start()
