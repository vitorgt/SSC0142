import sys
import atexit
import socket
import threading


class EnviThread(threading.Thread):
    def __init__(self, manager, conn):
        self.manager = manager
        self.conn = conn
        atexit.register(EnviThread.closeconn, self)
        threading.Thread.__init__(self)

    def readID(self):
        while True:
            data = self.conn.recv(1024)
            if data:
                break
        print("envithread received: " + str(data, "utf-8"))
        data = str(data, "utf-8").split("|")
        if "CONN" == data[1]:
            return data[2]
        else:
            print(data)
            raise ConnectionRefusedError("unknown protocol received")

    def closeconn(self):
        self.conn.close()
        sys.exit(0)

    def enviNow(self, ID):
        if ID == "TEMP":  # sensor temperature
            pass
        elif ID == "HUMI":  # sensor humidity
            pass
        elif ID == "CO2L":  # sensor co2 level
            pass
        elif ID == "HEAT":  # actuator heater
            pass
        elif ID == "COOL":  # actuator cooler
            pass
        elif ID == "WATE":  # actuator watering
            pass
        elif ID == "CO2I":  # actuator co2 injector
            pass
        return "yo"

    def run(self):
        ID = EnviThread.readID(self)
        while True:
            while True:
                data = self.conn.recv(1024)
                if data:
                    break
            print("envithread received: " + str(data, "utf-8"))
            data = str(data, "utf-8").split("|")
            if "GET" == data[1]:
                self.conn.send(bytes("|POST|"+EnviThread.enviNow(self, ID)+"|", "utf-8"))
            else:
                print(data)
                raise ConnectionRefusedError("unknown protocol received")
        EnviThread.closeconn(self)