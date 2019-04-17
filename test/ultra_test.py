import socket
import time


class SensorStreamingTest(object):
    def __init__(self, host, port):

        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.streaming()

    def streaming(self):

        try:
            print("Host: ", self.host_name + ' ' + self.host_ip)
            print("Connection from: ", self.client_address)

            while True:

                sensor_data = self.connection.recv(1024)
                #传入数据
                sensor_data = float(sensor_data.decode())
                #先解码，在转换为float

                print("Distance: %0.1f cm" % sensor_data)

        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    h, p = "192.168.137.1", 8002
    SensorStreamingTest(h, p)