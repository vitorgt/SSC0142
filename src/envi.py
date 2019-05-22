#!/usr/bin/python3

import sys
import time
import atexit
import socket
import threading
import envi_thread


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.daemon = True  # to kill the thread when closing the program
        thread.start()
    return wrapper


class Environment:

    @threaded
    def connectionslistener(self):
        while True:
            conn, addr = self.server.accept()
            del addr
            envi_thread.EnviThread(manager=self, conn=conn).start()

    @threaded
    def tempModif(self):
        def tempFunc(x):
            return ((4270108*x**3)/1245037605 - (18942894*x**2)/147996071 +
                    (29729284*x)/25753755 - 56192225/49559952 - 0.033328043332542)
        while True:
            self.temp += tempFunc(int(time.time() - self.startTime) % 24)
            print("temp now:", int(time.time() - self.startTime) % 24, self.temp)
            time.sleep(1)

    def closeserver(self):
        try:
            self.server.close()
        except Exception as e:
            print("Environment's server could not be closed because of", e)
            print("Closing application anyway")
        else:
            print("Environment's server successfully closed")

    def __init__(self):

        for x in range(len(sys.argv)):
            if "-t" in sys.argv[x]:
                self.temp = sys.argv[x+1]

        self.startTime = time.time()

        self.temp = 16
        self.humi = 0.7
        self.co2 = 500
        self.o2 = 500

        self.tempModif()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', 8888))  # '' to accept any connection
        self.server.listen()

        # when exiting application, close server
        atexit.register(Environment.closeserver, self=self)

        self.connectionslistener()

        while True:
            data = input().split(" ")
            for x in range(len(data)):
                if "temp" in data[x]:
                    self.temp += int(data[x+1])



if __name__ == "__main__":
    Environment()
