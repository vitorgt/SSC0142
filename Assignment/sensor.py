import time
import client


class Sensor():

    # Sends data to Manager
    def mana(self, client):
        while len(self.info) == 0:
            pass
        while True:
            string = "|PUT|"+client.ID+"|"+str(self.info[0])+"|"
            if client.v:
                print(client.ID+" -> "+client.target+": "+string)
            client.sck.send(bytes(string, "utf-8"))
            time.sleep(1)

    # Receives data from Environment
    def envi(self, client):
        while True:
            while True:
                try:
                    data = client.sck.recv(1024)
                except Exception:
                    pass
                if data:
                    break
            if client.v:
                print(client.ID+" <- "+client.target+": "+str(data, "utf-8"))
            data = str(data, "utf-8").split("|")
            if data[1] == "PUT" and data[2] == client.ID:
                if len(self.info) == 0:
                    self.info.append(float(data[3]))
                else:
                    self.info[0] = float(data[3])

    def __init__(self, ID):
        self.info = []
        HOST, v = client.inputs()
        if HOST != None:
            client.Client(7777, ID, "MANA", self.mana, v, HOST).start()
            client.Client(8888, ID, "ENVI", self.envi, v, HOST).start()
        else:
            client.Client(7777, ID, "MANA", self.mana, v).start()
            client.Client(8888, ID, "ENVI", self.envi, v).start()
