from threading import Thread, Lock
import socket
import time
import copy
import json

class Client():

    BUFSIZ = 1024

    def __init__(self):

        try:
            with open("./game_data/ip_port.txt", "r") as f:
                lines = f.readlines()
                HOST = lines[0].strip()
                PORT = int(lines[1].strip())
        except IOError:
            print("Address file missing")

        self.HOST = HOST
        self.PORT = PORT
        self.ADDR = (HOST, PORT)

        self.active = False
        self.client_connect()

    def client_connect(self):

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.client_socket.connect(self.ADDR)
            self.active = True

            self.lock = Lock()
            self.messages = {}

            self.receive_thread = Thread(target=self.receive_messages)
            self.receive_thread.start()

            self.chat = Thread(target=self.update_messages)
            self.chat.start()

            self.send_message({"name": socket.gethostname()})
            time.sleep(0.5)

        except ConnectionRefusedError:
            self.active = False

    def receive_messages(self):

        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ)
                msg = json.loads(msg.decode("utf-8"))
                print(msg)

                if "server_response" in msg and msg["server_response"] == "END":
                    self.active = False
                    self.client_socket.close()
                    print("Socket closed")
                    break

                # make sure memory is safe to access
                keys = list(msg)
                for k in keys:
                    self.lock.acquire()
                    self.messages[k] = msg[k]
                    self.lock.release()

            except Exception as e:
                print("receive [EXCPETION]", e)
                break

    def send_message(self, msg, reconnect=True):

        try:
            msg_bytes = json.dumps(msg).encode('utf-8')
            self.client_socket.sendall(msg_bytes)
        except Exception as e:
            if reconnect:
                self.client_connect()
                return self.send_message(msg, False)
            else:
                return False

    def get_messages(self):

        if not self.active: return None

        # make sure memory is safe to access
        self.lock.acquire()
        messages_copy = copy.deepcopy(self.messages)
        self.lock.release()

        return messages_copy

    def update_messages(self):

        self.log_messages = {}
        run = True

        while run:
            time.sleep(0.1)
            new_messages = self.get_messages()
            if new_messages == None: break
            else: self.log_messages = new_messages.copy()

    def disconnect(self):
        self.send_message({"request": "{quit}"}, False)
