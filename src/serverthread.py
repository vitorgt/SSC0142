import socket
import threading

class serverthread(threading.Thread):
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        print 'New connection with ', addr

    def run(self):
        ID = readID()
        if   (ID == "temp"):# sensor temperature
            tempH()# handler
        elif (ID == "humi"):# sensor humidity
            humiH()
        elif (ID == "co2l"):# sensor co2 level
            co2lH()
        elif (ID == "heat"):# actuator heater
            heatH()
        elif (ID == "cool"):# actuator cooler
            coolH()
        elif (ID == "wate"):# actuator water
            wateH()
        elif (ID == "co2i"):# actuator co2 injector
            co2iH()
        print 'Closing connection with ', addr
        conn.close()

    def readID():
        while True:
            data = conn.recv(1024)
            if data: break
        print data.split("|")
        conn.sendall(b'ACK|ID')
        return data[1]

#seerver
#   data = conn.recv(1024)
#   conn.sendall(data)
#client
#   s.sendall(b'text')
#   data = s.recv(1024)
