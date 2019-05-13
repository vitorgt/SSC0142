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
import serverthread as st


def connectionslistener(server):
    while True:
        conn, addr = server.accept()
        st.ServerThread(conn, addr).start()

def closeserver(server):
    try:
        server.close()
    except Exception as e:
        print("Server could not be closed because of", e)
        print("Closing application anyway")
    else:
        print("Server successfully closed")

def main():

    ##################### GETTING SERVER'S IP ######################
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print("Server's IP:", s.getsockname()[0])
    s.close()
    ################################################################

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', 7777)) #'' to accept any connection
    server.listen()
    #listen's arg is the max connections
    #can be the number of sensors+actuators
    atexit.register(closeserver, server) # when exiting application, close server

    cl = threading.Thread(target=connectionslistener, args=(server,))
    cl.daemon = True # to kill the thread when closing the program
    cl.start()

    print("Type q to quit at anytime")
    while True:
        if "q" in input():
            sys.exit()

if __name__ == "__main__":
    main()

#lock = threading.Lock()
#lock.acquire()
#do stuff
#lock.release()
