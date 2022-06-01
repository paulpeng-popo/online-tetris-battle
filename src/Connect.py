import socket
import time

HOST = '127.0.0.1'
PORT = 18642

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

i = 0
while (1):
    s.sendall("This is a client".encode('utf-8'))
    data = s.recv(1024)
    data = data.decode('utf-8')
    print("Received", data)
    if i == 10:
        s.send("END".encode('utf-8'))
        break;
    i += 1
    time.sleep(2)

s.close()
