#!/usr/bin/python3

import sys
import time
import socket


class temp:  # sensor temperature
    HOST = "127.0.0.1"
    v = False
    for x in range(len(sys.argv)):
        if "-ip" in sys.argv[x]:
            HOST = sys.argv[x+1]
        if "-v" in sys.argv[x]:
            v = True

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, 7777))
    except ConnectionRefusedError:
        print("Server is not online, trying again")
        while True:
            try:
                client.connect((HOST, 7777))
            except ConnectionRefusedError:
                pass
            else:
                break
    if v:
        print("temp sending: |CONN|TEMP|")
    client.send(bytes("|CONN|TEMP|", "utf-8"))
    while True:
        data = client.recv(1024)
        if data:
            break
    if v:
        print("temp received: " + str(data, "utf-8"))
    data = str(data, "utf-8").split("|")
    if data[1] == "ACK" and data[2] == "CONN" and data[3] == "TEMP":
        i = 4
        while i > 0:
            i -= 1
            time.sleep(2)
            if v:
                print("temp sending: |TEMP|40|C|")
            client.send(bytes("|TEMP|40|C|", "utf-8"))
