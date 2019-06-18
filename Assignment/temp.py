#!/usr/bin/python3

import time
import client

temp = 0


# Sends temperatures to Manager
def mana(client):
    while True:
        time.sleep(10)
        if client.v:
            print(client.ID, "-> MANA: |PUT|"+client.ID+"|"+temp+"|")
        client.sck.send(bytes("|PUT|"+client.ID+"|"+temp+"|", "utf-8"))


# Receives temperature from Environment
def envi(client):
    while True:
        while True:
            data = client.sck.recv(1024)
            if data:
                break
        if client.v:
            print(client.ID+" <- "+client.target+": "+str(data, "utf-8"))
        data = str(data, "utf-8").split("|")
        if data[1] == "PUT" and data[2] == client.ID:
            temp = data[3]


if __name__ == "__main__":
    HOST, v = client.inputs()
    if HOST != None:
        client.Client(7777, "TEMP", "MANA", mana, v, HOST).start()
        client.Client(8888, "TEMP", "ENVI", envi, v, HOST).start()
    else:
        client.Client(7777, "TEMP", "MANA", mana, v).start()
        client.Client(8888, "TEMP", "ENVI", envi, v).start()
