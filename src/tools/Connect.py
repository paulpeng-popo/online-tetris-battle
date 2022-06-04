import socket
import time

class ConnectServer():
    
    def __init__(self):

        HOST = "172.29.116.72"
        PORT = 18642
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        
    def run():

        i = 0
        while (True):
            self.sock.sendall("This is a client".encode('utf-8'))
            data = self.sock.recv(1024)
            data = data.decode('utf-8')
            print("Received", data)
            
            if i == 10:
                s.send("END".encode('utf-8'))
                break;
            i += 1
            
            time.sleep(2)
            
    def close():

        self.sock.close()
        print("socket clsoed")
        
