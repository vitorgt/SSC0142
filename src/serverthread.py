import socket

class serverthread:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        print 'New connection with ', addr
        main()
        print 'Closing connection with ', addr
        conn.close()

    def main():
        ID = readID()
        if   (ID == "temp"):
            tempH()
        elif (ID == "humi"):
            humiH()
        elif (ID == "co2l"):
            co2lH()
        elif (ID == "heat"):
            heatH()
        elif (ID == "cool"):
            coolH()
        elif (ID == "wate"):
            wateH()
        elif (ID == "co2i"):
            co2iH()

#seerver
#   data = conn.recv(1024)
#   conn.sendall(data)
#client
#   s.sendall(b'text')
#   data = s.recv(1024)
