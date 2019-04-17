__author__ = 'yxt'

import numpy as np
import cv2
import pygame
from pygame.locals import *
import time
import os
import threading
import socketserver


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
                time.sleep(0.2)

        finally:
            print("Connection closed on control thread")


class DataHandler(socketserver.StreamRequestHandler):

    def handle(self):

        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1

        self.send_inst = True

        pygame.init()
        pygame.display.set_mode((250, 250))
        self.collect_image()

    def collect_image(self):

        global prediction
        prediction = 0

        saved_frame = 0
        total_frame = 0

        # collect images for training
        print('Start collecting images...')
        print("Press 'q' or 'x' to finish...")
        e1 = cv2.getTickCount()
        image_array = np.zeros((1, 38400))
        label_array = np.zeros((1, 4), 'float')

        # stream video frames one by one
        try:
            stream_bytes = b' '
            frame = 1
            while self.send_inst:
                stream_bytes += self.rfile.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

                    # select lower half of the image
                    height, width = image.shape
                    roi = image[int(height / 2):height, :]

                    # cv2.imshow('roi_image', roi)
                    cv2.imshow('image', image)

                    # reshape the roi image into one row array
                    temp_array = roi.reshape(1, 38400).astype(np.float32)

                    frame += 1
                    total_frame += 1

                    # get input from human driver
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            key_input = pygame.key.get_pressed()

                            # complex orders
                            if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                                print("Forward Right")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[1]))
                                saved_frame += 1
                                prediction = 6

                            elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                                print("Forward Left")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[0]))
                                saved_frame += 1
                                prediction = 7

                            elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                                print("Reverse Right")
                                prediction = 8

                            elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                                print("Reverse Left")
                                prediction = 9

                            # simple orders
                            elif key_input[pygame.K_UP]:
                                print("Forward")
                                saved_frame += 1
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[2]))
                                prediction = 1

                            elif key_input[pygame.K_DOWN]:
                                print("Reverse")
                                saved_frame += 1
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[3]))
                                prediction = 2

                            elif key_input[pygame.K_RIGHT]:
                                print("Right")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[1]))
                                saved_frame += 1
                                prediction = 3

                            elif key_input[pygame.K_LEFT]:
                                print("Left")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[0]))
                                saved_frame += 1
                                prediction = 4

                            elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                                print('exit')
                                self.send_inst = False
                                prediction = 0
                                break

                        elif event.type == pygame.KEYUP:
                            prediction = 0

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        break

            # save training data as a numpy file
            file_name = str(int(time.time()))
            directory = "training_data"
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                np.savez(directory + '/' + file_name + '.npz', train=image_array, train_labels=label_array)
            except IOError as e:
                print(e)

            e2 = cv2.getTickCount()
            # calculate streaming duration
            time0 = (e2 - e1) / cv2.getTickFrequency()
            print('Streaming duration:', time0)

            print(image_array.shape)
            print(label_array.shape)
            print('Total frame:', total_frame)
            print('Saved frame:', saved_frame)
            print('Dropped frame', total_frame - saved_frame)

        finally:
            print("Connection closed on data thread")


class Server(object):

    def __init__(self, host, port1, port2):
        self.host = host
        self.port1 = port1
        self.port2 = port2

    def collect_data(self, host, port):
        s = socketserver.TCPServer((host, port), DataHandler)
        s.serve_forever()

    def control_stream(self, host, port):
        s = socketserver.TCPServer((host, port), ControlHandler)
        s.serve_forever()

    def start(self):

        video_thread = threading.Thread(target=self.collect_data, args=(self.host, self.port1))
        video_thread.daemon = True
        video_thread.start()

        control_thread = threading.Thread(target=self.control_stream, args=(self.host, self.port2))
        control_thread.daemon = True
        control_thread.start()
        #self.video_stream(self.host, self.port1)


if __name__ == '__main__':
    h, p1, p2 = "192.168.137.1", 8000, 8004
    ts = Server(h, p1, p2)
    ts.start()