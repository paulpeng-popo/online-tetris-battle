from threading import Thread, Lock
import socket, time

class Client():

    # HOST = "172.29.116.72"
    HOST = "127.0.0.1"
    PORT = 18642
    ADDR = (HOST, PORT)
    BUFSIZ = 1024

    def __init__(self, name):

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client_socket.connect(self.ADDR)

            self.active = True
            self.messages = []

            self.idle_limit = 3
            self.lock = Lock()

            self.receive_thread = Thread(target=self.receive_messages)
            self.receive_thread.start()

            self.chat = Thread(target=self.update_messages)
            self.chat.start()

            self.name = name
            self.send_message(name)
        except ConnectionRefusedError:
            print("GameServer is not runing!!")
            self.active = False

    def receive_messages(self):

        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf-8")

                if msg == "END": break
                # make sure memory is safe to access
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()

            except Exception as e:
                print("receive [EXCPETION]", e)
                break

    def send_message(self, msg):

        try:
            self.client_socket.send(msg.encode("utf-8"))
            if msg == "{quit}":
                self.receive_thread.join()
                self.client_socket.close()
                self.active = False
                print("Client " + self.name + " socket closed")
        except Exception as e:
            if msg != "{quit}": print("[Not sent message]: " + msg)

    def get_messages(self):

        messages_copy = self.messages[:]

        # make sure memory is safe to access
        self.lock.acquire()
        self.messages = []
        self.lock.release()

        return messages_copy

    def update_messages(self):

        # messages = []
        run = True
        start_time = -1

        while run:

            time.sleep(0.01)
            new_messages = self.get_messages()
            if new_messages == []:
                if start_time == -1:
                    start_time = time.monotonic()
                    continue
                else:
                    check_time = time.monotonic()
                    if round(check_time-start_time, 2) >= self.idle_limit:
                        run = False
            else:
                start_time = -1
                # messages.extend(new_messages)
                for msg in new_messages:
                    print(msg)

        if self.active: print("Idling!! Closing automatically!!")
        print("Thread closed")
        self.disconnect()

    def disconnect(self):
        self.send_message("{quit}")
