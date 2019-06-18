#!/usr/bin/python3

import time
import server
import random


temperature = 40.0
humidity = 0.6
co2level = 550.0


def temp(st):
    print("yi from new temp")
    while True:
        time.sleep(10)
        if st.server.v:
            print(st.server.ID, "-> "+st.ID+": |PUT|"+st.server.ID+"|"+str(temperature)+"|")
        st.conn.send(bytes("|PUT|"+st.ID+"|"+str(temperature)+"|", "utf-8"))


def humi():
    print("yi from new humi")


functions = {
    "TEMP": temp,
    "HUMI": humi
}


def envi(serverThread):
    functions[serverThread.ID](serverThread)


@server.threaded
def enviRand():
    temperature += random.random()*2-1  # [-1, 1]
    humidity += random.random()-0.5  # [-0.5, 0.5]
    if humidity > 1:
        humidity = 1
    co2level += random.random()*4-2  # [-2, 2]


if __name__ == "__main__":
    enviRand()
    environment = server.Server(8888, "ENVI", envi)
