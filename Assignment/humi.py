#!/usr/bin/python3

import time
import client


# Sends humidity to Manager
def mana(client):
    while True:
        time.sleep(10)
        if client.v:
            print(client.ID, "-> MANA: |PUT|"+client.ID+"|0.6|")
        client.sck.send(bytes("|PUT|"+client.ID+"|0.6|", "utf-8"))


# Receives humidity from Environment
def envi(client):
    pass


if __name__ == "__main__":
    HOST, v = client.inputs()
    if HOST != None:
        client.Client(7777, "HUMI", "MANA", mana, v, HOST).start()
        client.Client(8888, "HUMI", "ENVI", envi, v, HOST).start()
    else:
        client.Client(7777, "HUMI", "MANA", mana, True).start()
        client.Client(8888, "HUMI", "ENVI", envi, True).start()
