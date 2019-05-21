import sys
import atexit
import socket
import threading


class ServerThread(threading.Thread):
    def __init__(self, manager, conn, addr):
        self.manager = manager
        self.conn = conn
        self.addr = addr
        self.id = None
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
        self.id.conn = False  # update manager's info
        self.conn.close()
        sys.exit(0)

    def run(self):
        ID = ServerThread.readID(self)
        handler = None
        if ID == "TEMP":  # sensor temperature
            self.id = self.manager.temp  # link to manager's info
            self.id.conn = self.addr
            import server_temp
            handler = server_temp.handler
        '''
        elif ID == "HUMI":  # sensor humidity
            import server_humi
            handler = server_humi.handler
        elif ID == "CO2L":  # sensor co2 level
            import server_co2l
            handler = server_co2l.handler
        elif ID == "HEAT":  # actuator heater
            import server_heat
            handler = server_heat.handler
        elif ID == "COOL":  # actuator cooler
            import server_cool
            handler = server_cool.handler
        elif ID == "WATE":  # actuator watering
            import server_wate
            handler = server_wate.handler
        elif ID == "CO2I":  # actuator co2 injector
            import server_co2i
            handler = server_co2i.handler
        '''
        handler(self, self.manager)
        ServerThread.closeconn(self)

#seerver
#   data = conn.recv(1024)
#   conn.sendall(data)
#client
#   s.sendall(b'text')
#   data = s.recv(1024)
