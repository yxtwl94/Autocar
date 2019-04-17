
import threading
import socketserver
import cv2
import numpy as np
import time
from model import NeuralNetwork

# distance data measured by ultrasonic sensor
sensor_data = " "
prediction = 0


class ControlHandler(socketserver.BaseRequestHandler):

    def handle(self):

        print('New connection for Control:', self.client_address)

        try:
            while True:

                command = str(prediction)
                command = command.encode()
                self.request.send(command)
                if prediction == 0:
                    print("stopping")
                if prediction == 1:
                    print("going forward")
                if prediction == 2:
                    print("going back")
                if prediction == 3:
                    print("right")
                if prediction == 4:
                    print("left")
                if prediction == 6:
                    print("forward_right")
                if prediction == 7:
                    print("forward_left")
                if prediction == 8:
                    print("back_right")
                if prediction == 9:
                    print("back_left")

                #发送指令间隔
                time.sleep(0.1)

        finally:
            print("Connection closed on thread 3")


class SensorDataHandler(socketserver.BaseRequestHandler):

    data = " "

    def handle(self):
        print('New connection for Sensor:', self.client_address)
        global sensor_data

        try:
            while self.data:
                self.data = self.request.recv(1024)
                sensor_data = round(float(self.data), 1)
                # print "{} sent:".format(self.client_address[0])
                print(sensor_data, " cm")
        finally:
            print("Connection closed on thread 2")


class VideoStreamHandler(socketserver.StreamRequestHandler):

    nn = NeuralNetwork()
    nn.load_model("saved_model/nn_model.xml")

    def handle(self):

        print('New connection for Video:', self.client_address)

        global prediction
        global sensor_data

        stream_bytes = b' '

        # stream video frames one by one
        try:
            while True:
                stream_bytes += self.rfile.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    gray = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    # lower half of the image
                    height, width = gray.shape
                    roi = gray[int(height / 2):height, :]

                    cv2.imshow('image', image)

                    # reshape image
                    image_array = roi.reshape(1, int(height / 2) * width).astype(np.float32)

                    # neural network makes prediction
                    prediction = int(self.nn.predict(image_array))

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("car stopped")
                    prediction = 0
                    break

        finally:
            cv2.destroyAllWindows()
            print("Connection closed on thread 1")


class Server(object):
    def __init__(self, host, port1, port2, port3):
        self.host = host
        self.port1 = port1
        self.port2 = port2
        self.port3 = port3

    def video_stream(self, host, port):
        s = socketserver.TCPServer((host, port), VideoStreamHandler)
        s.serve_forever()

    def sensor_stream(self, host, port):
        s = socketserver.TCPServer((host, port), SensorDataHandler)
        s.serve_forever()

    def control_stream(self, host, port):
        s = socketserver.TCPServer((host, port), ControlHandler)
        s.serve_forever()

    def start(self):

        video_thread = threading.Thread(target=self.video_stream, args=(self.host, self.port1))
        video_thread.daemon = True
        video_thread.start()

        sensor_thread = threading.Thread(target=self.sensor_stream, args=(self.host, self.port2))
        sensor_thread.daemon = True
        sensor_thread.start()

        control_thread = threading.Thread(target=self.control_stream, args=(self.host, self.port3))
        control_thread.daemon = True
        control_thread.start()
        #self.video_stream(self.host, self.port1)


if __name__ == '__main__':
    h, p1, p2, p3 = "192.168.137.1", 8000, 8002, 8004
    ts = Server(h, p1, p2, p3)
    ts.start()