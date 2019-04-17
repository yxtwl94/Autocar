import socket
import time


class ControlTest(object):
    def __init__(self, host, port):

        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.control()

    def control(self):

        command = input('command is :')
        command = command.encode()

        try:
            print("Host: ", self.host_name + ' ' + self.host_ip)
            print("Connection from: ", self.client_address)

            while True:
                self.connection.send(command)
                # 发送指令间隔
                time.sleep(1)
                print("command is ", command.decode())

        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    h, p = "192.168.137.1", 8004
    ControlTest(h, p)