
#!/usr/bin/python3

import time
import server
from random import random


temperature = 40
humidity = 0.6
co2level = 550


def temp(st):
    print("yi from new temp")
    while True:
        time.sleep(10)
        if st.server.v:
            print(st.server.ID, "-> "+st.server.ID+": |PUT|"+st.server.ID+"|"+temperature+"|")
        st.conn.send(bytes("|PUT|"+st.server.ID+"|"+temperature+"|", "utf-8"))


def humi():
    print("yi from new humi")


functions = {
    "TEMP": temp,
    "HUMI": humi
}


def envi(serverThread):
    functions[serverThread.ID](serverThread)

@server.threaded
def tempRand(temperature):
    temperature += random()*2-1

if __name__ == "__main__":
    tempRand(temperature)
    environment = server.Server(8888, "ENVI", envi)
