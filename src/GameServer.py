from threading import Thread, Lock
import socket
import signal
import string
import random
import time
import json
import sys

class Player:

    def __init__(self, addr, client):
        self.addr = addr
        self.client = client
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

        self.players = { "public": [] }
        self.lock = Lock()
        self.list_lock = Lock()
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

                self.list_lock.acquire()
                self.players["public"].append(player)
                self.list_lock.release()

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
        client.settimeout(30.0)

        addr = player.addr
        room = "public"

        name = client.recv(self.BUFSIZ)
        name = json.loads(name.decode("utf-8"))["name"]
        player.set_name(name)

        while True:
            try:
                msg = client.recv(self.BUFSIZ)
                msg = json.loads(msg.decode("utf-8"))["request"]
                if msg == "CREATE":
                    for room_name in list(self.players):
                        if self.leave_room(room_name, addr):
                            break
                    room = self.new_room(addr, player)
                    response = json.dumps({"room": room}).encode('utf-8')
                    client.sendall(response)

                    timeout_time = time.time() + 30

                    while time.time() < timeout_time:

                        num_of_player = 2
                        in_room_players = len(self.players[room])

                        if num_of_player == in_room_players:
                            res = json.dumps({"server_response": True}).encode('utf-8')
                            client.sendall(res)
                            self.communicate(client, addr, room)
                            break

                elif msg == "JOIN":
                    while True:
                        message = client.recv(self.BUFSIZ)
                        message = json.loads(message.decode("utf-8"))
                        if "room" in list(message):
                            room = message["room"]
                        if "server_response" in list(message):
                            command = message["server_response"]

                        if command == "RETURN":
                            break
                        elif room in list(self.players):
                            response = json.dumps({"server_response": True}).encode('utf-8')
                            client.sendall(response)
                            self.leave_room("public", addr)
                            self.list_lock.acquire()
                            self.players[room].append(player)
                            self.list_lock.release()
                            self.communicate(client, addr, room)
                            break
                        else:
                            response = json.dumps({"server_response": False}).encode('utf-8')
                            client.sendall(response)
                elif msg == "{quit}":
                    self.client_leave(client, room, addr, name)
                    break
                else:
                    pass
            except socket.timeout:
                self.client_leave(client, room, addr, name)
                break

    def client_leave(self, client, room, addr, name):
        response = json.dumps({"server_response": "END"}).encode('utf-8')
        try:
            client.sendall(response)
            client.close()
        except Exception as e:
            pass

        self.leave_room(room, addr)
        datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(f"[DISCONNECT] {name} {addr} disconnected at {datetime}")

    def new_room(self, addr, player):
        while True:
            all_chars = list(string.digits)
            random.shuffle(all_chars)
            room = ''.join(all_chars[:8])
            if room not in self.players:
                self.leave_room("public", addr)
                self.list_lock.acquire()
                self.players[room] = [player]
                self.list_lock.release()
                return room

    def leave_room(self, room_name, addr):
        delete_suc = False
        self.list_lock.acquire()
        for player in self.players[room_name]:
            if player.addr == addr:
                self.players[room_name].remove(player)
                delete_suc = True
                break
        if room_name != "public" and len(self.players[room_name]) == 0:
            self.players.pop(room_name)
        self.list_lock.release()
        return delete_suc

    def communicate(self, client, addr, room):
        while True:
            message = client.recv(self.BUFSIZ)
            print(message)
            check = json.loads(message.decode("utf-8"))
            self.broadcast(room, message, addr)
            if "winner" in check:
                break

    def broadcast(self, room, msg, addr):
        for player in self.players[room]:
            if player.addr != addr:
                client = player.client
                try:
                    client.sendall(msg)
                except Exception as e:
                    print("broadcast [EXCEPTION]", e)
                    print("Communication thread closed")
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
