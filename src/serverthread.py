#!/usr/bin/python3

import sys
import atexit
import socket
import threading


class ServerThread(threading.Thread):
    def __init__(self, manager, conn, addr):
        self.manager = manager
        self.conn = conn
        self.addr = addr
        print("New connection with", addr[0])
        atexit.register(ServerThread.closeconn, self)
        threading.Thread.__init__(self)

    def readID(self):
        while True:
            data = self.conn.recv(1024)
            if data:
                break
        if self.manager.v:
            print("serverthread received: " + str(data, "utf-8"))
        data = str(data, "utf-8").split("|")
        if "CONN" == data[1]:
            if self.manager.v:
                print("serverthread sending: |ACK"+"|".join(data))
            self.conn.send(bytes("|ACK"+"|".join(data), "utf-8"))
            return data[2]
        else:
            print(data)
            raise ConnectionRefusedError("unknown protocol received")

    def closeconn(self):
        print("Closing connection with", self.addr[0])
        self.conn.close()
        sys.exit(0)

    def run(self):
        ID = ServerThread.readID(self)
        handler = None
        if ID == "TEMP":  # sensor temperature
            import temp
            handler = temp.handler
        elif ID == "HUMI":  # sensor humidity
            import humi
            handler = humi.handler
        elif ID == "CO2L":  # sensor co2 level
            import co2l
            handler = co2l.handler
        elif ID == "HEAT":  # actuator heater
            import heat
            handler = heat.handler
        elif ID == "COOL":  # actuator cooler
            import cool
            handler = cool.handler
        elif ID == "WATE":  # actuator watering
            import wate
            handler = wate.handler
        elif ID == "CO2I":  # actuator co2 injector
            import co2i
            handler = co2i.handler
        handler(self, self.manager)
        ServerThread.closeconn(self)

#seerver
#   data = conn.recv(1024)
#   conn.sendall(data)
#client
#   s.sendall(b'text')
#   data = s.recv(1024)
