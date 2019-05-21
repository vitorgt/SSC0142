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
import serverthread


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
            serverthread.ServerThread(
                manager=self, conn=conn, addr=addr).start()

    def closeserver(self):
        try:
            self.server.close()
        except Exception as e:
            print("Server could not be closed because of", e)
            print("Closing application anyway")
        else:
            print("Server successfully closed")

    def __init__(self):

        #arrays to store collected data
        self.tempData = []
        self.humiData = []
        self.co2lData = []

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
        while True:
            if "quit" in input():
                sys.exit()


if __name__ == "__main__":
    Server()

#lock = threading.Lock()
#lock.acquire()
#do stuff
#lock.release()
