
#!/usr/bin/python3

import time
import server
import random


class Environment():
    def __init__(self):
        self.temperature = 40
        self.humidity = 0.6
        self.co2level = 550


def temp(st):
    print("yi from new temp")
    while True:
        time.sleep(10)
        if st.server.v:
            print(st.server.ID, "-> "+st.server.ID+": |PUT|"+st.server.ID+"|"+str(temperature)+"|")
        st.conn.send(bytes("|PUT|"+st.server.ID+"|"+str(temperature)+"|", "utf-8"))
        temperature -= 1


def humi():
    print("yi from new humi")


functions = {
    "TEMP": temp,
    "HUMI": humi
}


def envi(serverThread):
    functions[serverThread.ID](serverThread)

@server.threaded
def tempRand(data):
    while True:
        data.temperature += random.randint(-1, 1)

if __name__ == "__main__":
    data = Environment()
    tempRand(data)
    environment = server.Server(8888, "ENVI", envi)
