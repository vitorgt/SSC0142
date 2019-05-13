import sys
import socket

class temp: # sensor temperature
    for x in range(len(sys.argv)):
        if "-ip" in sys.argv[x]:
            HOST = sys.argv[x+1]

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, 7777))
    except ConnectionRefusedError:
        print("Server is not online, trying again")
        while True:
            try:
                client.connect((HOST, 7777))
            except ConnectionRefusedError: pass
            else: break
    #client.sendall(b'hiiii')
    client.send(bytes("hii",'utf-8'))
