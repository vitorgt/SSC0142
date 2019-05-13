#!/usr/bin/python3

import sys
import atexit
import socket
import threading

class ServerThread(threading.Thread):
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        print("New connection with", addr[0])
        atexit.register(ServerThread.closeconn, self)
        threading.Thread.__init__(self)

    def readID(self):
        while True:
            data = self.conn.recv(1024)
            if data: break
        print(str(data, 'utf-8'))
        #self.conn.sendall(b'ACK|ID')
        return str(data, 'utf-8')

    def closeconn(self):
        print("Closing connection with", self.addr[0])
        self.conn.close()
        sys.exit(0)

    def run(self):
        ID = ServerThread.readID(self)
        if   ID == "temp": # sensor temperature
            tempH() # handler
        elif ID == "humi": # sensor humidity
            humiH()
        elif ID == "co2l": # sensor co2 level
            co2lH()
        elif ID == "heat": # actuator heater
            heatH()
        elif ID == "cool": # actuator cooler
            coolH()
        elif ID == "wate": # actuator watering
            wateH()
        elif ID == "co2i": # actuator co2 injector
            co2iH()
        ServerThread.closeconn(self)

#seerver
#   data = conn.recv(1024)
#   conn.sendall(data)
#client
#   s.sendall(b'text')
#   data = s.recv(1024)
