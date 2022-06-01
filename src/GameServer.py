import socket
import time
import socketserver
import threading

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        BUFSIZE = 1024
        print('Connect from: {0}:{1}'.format(self.client_address[0], self.client_address[1]))
        while(True):
            data = self.request.recv(BUFSIZE)
            bdata = data.decode('utf-8')
            if bdata == "END":
                break;
            self.request.sendall(data)
            time.sleep(0.1)

    def finish(self):
        print("client {0}:{1} disconnect!".format(self.client_address[0],self.client_address[1]))

def connect():
    HOST = socket.gethostname()
    PORT = 18642
    server = ThreadedTCPServer(("127.0.0.1", PORT), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    print('Server is starting up...')
    print('Host: {0}, listen to port: {1}'.format(HOST,PORT))

if __name__=='__main__':
    connect()
