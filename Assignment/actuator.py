import time
import client


class Actuator():

    # Receives commands from Manager
    def mana(self, client):
        while True:
            data = None
            while not data:
                try:
                    data = client.sck.recv(1024)
                except Exception:
                    pass
            if client.v:
                print(client.ID+" <- "+client.target+": "+str(data, "utf-8"))
            data = str(data, "utf-8").split("|")
            if data[1] == "PUT" and data[2] == client.ID:
                if data[3] == "ON":
                    self.on[0] = True
                else:
                    self.on[0] = False
                # Acknowledgement
                string = "|ACK|PUT|"
                if client.v:
                    print(client.ID, "-> "+client.target+": "+string)
                client.sck.send(bytes(string, "utf-8"))

    # Sends commands to Environment
    def envi(self, client):
        while True:
            if self.on[0]:
                string = "|PUT|"+client.ID+"|"+str(self.strength)+"|"
                if client.v:
                    print(client.ID+" -> "+client.target+": "+string)
                client.sck.send(bytes(string, "utf-8"))
                time.sleep(1)

    def __init__(self, ID, strength):
        self.on = [False]
        self.strength = strength
        HOST, v = client.inputs()
        if HOST != None:
            client.Client(7777, ID, "MANA", self.mana, v, HOST).start()
            client.Client(8888, ID, "ENVI", self.envi, v, HOST).start()
        else:
            client.Client(7777, ID, "MANA", self.mana, v).start()
            client.Client(8888, ID, "ENVI", self.envi, v).start()
