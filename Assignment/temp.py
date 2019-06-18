#!/usr/bin/python3

import time
import client

# Sends temperatures to Manager


def mana(client):
    while True:
        time.sleep(10)
        if client.v:
            print(client.ID, "-> MANA: |PUT|"+client.ID+"|40|")
        client.sck.send(bytes("|PUT|"+client.ID+"|40|", "utf-8"))


# Receives temperature from Environment
def envi(client):
    pass


if __name__ == "__main__":
    HOST, v = client.inputs()
    if HOST != None:
        client.Client(7777, "TEMP", "MANA", mana, v, HOST).start()
        client.Client(8888, "TEMP", "ENVI", envi, v, HOST).start()
    else:
        client.Client(7777, "TEMP", "MANA", mana, True).start()
        client.Client(8888, "TEMP", "ENVI", envi, True).start()
