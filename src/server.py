#!/usr/bin/python3

#REFERENCE
#https://en.wikibooks.org/wiki/Python_Programming/Threading
#https://docs.python.org/2/tutorial/classes.html
#https://docs.python.org/3/tutorial/modules.html
#https://wiki.python.org.br/SocketBasico
#https://www.geeksforgeeks.org/multithreading-in-python-set-2-synchronization/
#https://docs.python.org/3/library/socket.html
#https://www.afternerd.com/blog/wp-content/uploads/2017/11/SMTP-sequence-diagram.png

import sys
import atexit
import socket
import threading
import server_thread


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.daemon = True  # to kill the thread when closing the program
        thread.start()
    return wrapper


class Server:

    @threaded
    def connectionslistener(self):
        while True:
            conn, addr = self.server.accept()
            server_thread.ServerThread(
                manager=self, conn=conn, addr=addr).start()

    def closeserver(self):
        try:
            self.server.close()
        except Exception as e:
            print("Server could not be closed because of", e)
            print("Closing application anyway")
        else:
            print("Server successfully closed")

    def status(self):
        if self.temp.conn:
            print("Temperature: "+self.temp.data[-1]+"°C")
        if self.humi.conn:
            print("Humidity: "+self.humi.data[-1]+"%")
        if self.co2l.conn:
            print("CO2 level: "+self.co2l.data[-1]+"ppm")
        if self.heat.conn:
            print("Heater "+("off", "on")[self.heat.on])
        if self.cool.conn:
            print("Cooler "+("off", "on")[self.cool.on])
        if self.wate.conn:
            print("Watering "+("off", "on")[self.wate.on])
        if self.co2i.conn:
            print("CO2 injector "+("off", "on")[self.co2i.on])

    def __init__(self):

        #Server's data
        class Storage:
            def __init__(self):
                self.conn = False
                self.on = False
                self.data = []
        self.temp = Storage()
        self.humi = Storage()
        self.co2l = Storage()
        self.heat = Storage()
        self.cool = Storage()
        self.wate = Storage()
        self.co2i = Storage()

        self.v = False
        for x in range(len(sys.argv)):
            if "-v" in sys.argv[x]:
                self.v = True

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', 7777))  # '' to accept any connection
        self.server.listen()

        # when exiting application, close server
        atexit.register(Server.closeserver, self=self)

        Server.connectionslistener(self)

        if self.v:
            print("Type \"quit\" to quit at anytime")
            print("Type \"status\" to show sensors' instant mesurement")
        while True:
            if "quit" in input():
                sys.exit()
            if "status" in input():
                self.status()


if __name__ == "__main__":
    Server()

#lock = threading.Lock()
#lock.acquire()
#do stuff
#lock.release()
