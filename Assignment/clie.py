#!/usr/bin/python3

import client


def readFloat():
    while True:
        try:
            return float(input())
        except Exception as e:
            print(e)
            print("Try again")


class Clie():

    # Sends commands to Manager
    # Gets informations from Manager
    def mana(self, client):
        while True:
            if self.manaFlag[0]:
                self.manaFlag[0] = False
                string = self.request[0]
                self.request[0] = ""
                ack = False
                while not ack:
                    if client.v:
                        print(client.ID+" -> "+client.target+": "+string)
                    try:
                        client.sck.send(bytes(string, "utf-8"))
                    except OSError:
                        print(client.target+" disconnected")
                        print(client.ID+" disconnecting from "+client.target)
                        client.sck.close()
                        return
                    data = None
                    while not data:
                        try:
                            data = client.sck.recv(1024)
                        except Exception:
                            pass
                    if client.v:
                        print(client.ID+" <- "+client.target+": "+str(data, "utf-8"))
                    data = str(data, "utf-8").split("|")
                    if string.split("|")[1] == "GET":
                        for x in range(len(data)):
                            if data[x] == "PUT":
                                print(data[x+1], data[x+2])
                        ack = True
                    else:
                        if data[1] == "ACK" and data[2] == string.split("|")[1]:
                            ack = True

    # Sends commands to Environment
    def envi(self, client):
        while True:
            if self.enviFlag[0]:
                self.enviFlag[0] = False
                string = self.request[0]
                self.request[0] = ""
                ack = False
                while not ack:
                    if client.v:
                        print(client.ID+" -> "+client.target+": "+string)
                    try:
                        client.sck.send(bytes(string, "utf-8"))
                    except OSError:
                        print(client.target+" disconnected")
                        print(client.ID+" disconnecting from "+client.target)
                        client.sck.close()
                        return
                    data = None
                    while not data:
                        try:
                            data = client.sck.recv(1024)
                        except Exception:
                            pass
                    if client.v:
                        print(client.ID+" <- "+client.target+": "+str(data, "utf-8"))
                    data = str(data, "utf-8").split("|")
                    if data[1] == "ACK":
                        ack = True

    def __init__(self, ID="CLIE"):
        self.buffer = [""]
        self.request = [""]
        self.manaFlag = [False]
        self.enviFlag = [False]
        HOST, v = client.inputs()
        if HOST != None:
            client.Client(7777, ID, "MANA", self.mana, v, HOST).start()
            client.Client(8888, ID, "ENVI", self.envi, v, HOST).start()
        else:
            client.Client(7777, ID, "MANA", self.mana, v).start()
            client.Client(8888, ID, "ENVI", self.envi, v).start()
        print("Type \"GET\" to request sensors' and actuators' status from Manager")
        print("Type \"PUT\" to request Manager to turn actuators on and off")
        print("Type \"DEF\" to change Manager's sensors' limits")
        print("Type \"ENV\" to change Environment's variables manually")
        print("In every operation, more than one number can be typed")
        while True:
            self.buffer[0] = input()
            print("\""+self.buffer[0]+"\"")
            if "GET" in self.buffer[0]:
                print("Which sensors' mesurement do you want to request?")
                print("\t1: Temperature")
                print("\t2: Humidity")
                print("\t3: CO2 Level")
                print("\t4: Heater")
                print("\t5: Cooler")
                print("\t6: Watering")
                print("\t7: CO2 Injector")
                self.buffer[0] = input()
                if "1" in self.buffer[0]:
                    self.request[0] += "|GET|TEMP|"
                if "2" in self.buffer[0]:
                    self.request[0] += "|GET|HUMI|"
                if "3" in self.buffer[0]:
                    self.request[0] += "|GET|CO2L|"
                if "4" in self.buffer[0]:
                    self.request[0] += "|GET|HEAT|"
                if "5" in self.buffer[0]:
                    self.request[0] += "|GET|COOL|"
                if "6" in self.buffer[0]:
                    self.request[0] += "|GET|WATE|"
                if "7" in self.buffer[0]:
                    self.request[0] += "|GET|CO2I|"
                self.manaFlag[0] = True
            elif "PUT" in self.buffer[0]:
                hideHEAT = hideCOOL = hideWATE = hideCO2I = False
                print("First, which actuators do you want to turn on?")
                print("\t1: Heater")
                print("\t2: Cooler")
                print("\t3: Watering")
                print("\t4: CO2 Injector")
                self.buffer[0] = input()
                if "1" in self.buffer[0]:
                    self.request[0] += "|PUT|HEAT|ON|"
                    hideHEAT = True
                if "2" in self.buffer[0]:
                    self.request[0] += "|PUT|COOL|ON|"
                    hideCOOL = True
                if "3" in self.buffer[0]:
                    self.request[0] += "|PUT|WATE|ON|"
                    hideWATE = True
                if "4" in self.buffer[0]:
                    self.request[0] += "|PUT|CO2I|ON|"
                    hideCO2I = True
                print("Now, which actuators do you want to turn off?")
                if not hideHEAT:
                    print("\t1: Heater")
                if not hideCOOL:
                    print("\t2: Cooler")
                if not hideWATE:
                    print("\t3: Watering")
                if not hideCO2I:
                    print("\t4: CO2 Injector")
                self.buffer[0] = input()
                if not hideHEAT and "1" in self.buffer[0]:
                    self.request[0] += "|PUT|HEAT|OFF|"
                if not hideCOOL and "2" in self.buffer[0]:
                    self.request[0] += "|PUT|COOL|OFF|"
                if not hideWATE and "3" in self.buffer[0]:
                    self.request[0] += "|PUT|WATE|OFF|"
                if not hideCO2I and "4" in self.buffer[0]:
                    self.request[0] += "|PUT|CO2I|OFF|"
                self.manaFlag[0] = True
            elif "DEF" in self.buffer[0]:
                print("Which of the following do you want to change?")
                print("\t1: Maximum temperature")
                print("\t2: Minimum temperature")
                print("\t3: Minimum humidity level")
                print("\t4: Minimum CO2 level")
                self.buffer[0] = input()
                if "1" in self.buffer[0]:
                    print("Change maximum temperature to: ")
                    self.request[0] += "|DEF|TEMP|MAX|"+str(readFloat())+"|"
                if "2" in self.buffer[0]:
                    print("Change minimum temperature to: ")
                    self.request[0] += "|DEF|TEMP|MIN|"+str(readFloat())+"|"
                if "3" in self.buffer[0]:
                    print("Change minimum humidity level to: ")
                    self.request[0] += "|DEF|HUMI|MIN|"+str(readFloat())+"|"
                if "4" in self.buffer[0]:
                    print("Change minimum CO2 level to: ")
                    self.request[0] += "|DEF|CO2L|MIN|"+str(readFloat())+"|"
                self.manaFlag[0] = True
            elif "ENV" in self.buffer[0]:
                print("Which of the following do you want to change?")
                print("\t1: Temperature")
                print("\t2: Humidity")
                print("\t3: CO2 Level")
                self.buffer[0] = input()
                if "1" in self.buffer[0]:
                    print("Change temperature to: ")
                    self.request[0] += "|PUT|TEMP|"+str(readFloat())+"|"
                if "2" in self.buffer[0]:
                    print("Change humidity to: ")
                    self.request[0] += "|PUT|HUMI|"+str(readFloat())+"|"
                if "3" in self.buffer[0]:
                    print("Change CO2 level to: ")
                    self.request[0] += "|PUT|CO2L|"+str(readFloat())+"|"
                self.enviFlag[0] = True
            self.buffer[0] = ""


if __name__ == "__main__":
    Clie()