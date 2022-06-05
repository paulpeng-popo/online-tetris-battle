from threading import Thread, Lock
import socket, time, signal, sys

class Player:

    def __init__(self, addr, client):
        self.addr = addr
        self.client = client
        self.ready = False
        self.name = None

    def set_name(self, name):

        self.name = name

class Server():

    # HOST = "172.29.116.72"
    HOST = "127.0.0.1"
    PORT = 18642
    ADDR = (HOST, PORT)
    MAX_CONNECTIONS = 100
    BUFSIZ = 1024

    def __init__(self):

        self.master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.master_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.master_socket.bind(self.ADDR)

        self.players = []
        self.lock = Lock()
        self.run = True

    def listen_for_connections(self):

        self.master_socket.listen(self.MAX_CONNECTIONS)
        print("Waiting for players join ...")
        self.accept_thread = Thread(target=self.wait_for_connection)
        self.accept_thread.start()

    def server_stop(self):

        self.lock.acquire()
        self.run = False
        self.lock.release()

    def server_state(self):

        self.lock.acquire()
        state = self.run
        self.lock.release()

        return state

    def wait_for_connection(self):

        self.master_socket.settimeout(1.0)
        while self.server_state():
            try:
                client, addr = self.master_socket.accept()

                player = Player(addr, client)
                self.players.append(player)

                datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print(f"[CONNECT] {addr} connected at {datetime}")
                Thread(target=self.client_communication, args=(player,)).start()
            except socket.timeout:
                pass
            except Exception as e:
                print("wait [EXCEPTION]", e)
                print("SERVER CRASHED")
                break

    def client_communication(self, player):

        client = player.client

        name = client.recv(self.BUFSIZ).decode("utf-8")
        player.set_name(name)

        # msg = bytes(f"{name} has joined the public room", "utf8")
        # self.broadcast(msg, "")

        while True:
            msg = client.recv(self.BUFSIZ)

            if msg == bytes("{quit}", "utf8"):
                client.send(bytes("END", "utf8"))
                client.close()
                self.players.remove(player)

                # self.broadcast(bytes(f"{name} has left the public room", "utf8"), "")
                print(f"[DISCONNECT] {name} disconnected")
                break
            else:
                self.broadcast(msg, name+": ")
                # print(f"{name}: ", msg.decode("utf8"))

    def broadcast(self, msg, name):

        for player in self.players:
            client = player.client
            try:
                client.send(bytes(name, "utf8") + msg)
            except Exception as e:
                print("broadcast [EXCEPTION]", e)
                sys.exit(1)

    def handler(self, signum, args):
        self.server_stop()
        print("")
        print("Wait for listen thread closing ... ")
        self.accept_thread.join()
        print("Listen thread closed")
        self.master_socket.close()
        print("SERVER CLOSED")


if __name__ == '__main__':

    server = Server()
    server.listen_for_connections()
    signal.signal(signal.SIGINT, server.handler)
