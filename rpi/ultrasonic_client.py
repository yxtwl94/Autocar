'''
yxt
'''

from socket import *
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

client_socket=socket(AF_INET, SOCK_STREAM)
client_socket.connect(('192.168.137.1',8002))

def measure():
    """
    measure distance
    """
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00015)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()

    while GPIO.input(GPIO_ECHO)==0:
        pass
    start = time.time()

    while GPIO.input(GPIO_ECHO)==1:
        pass
    stop = time.time()
        
    distance = ((stop-start) * 34300)/2

    return distance
    
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 20
GPIO_ECHO    = 21

GPIO.setup(GPIO_TRIGGER,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(GPIO_ECHO,GPIO.IN)

try:    
    while True:
        distance = measure()
        print("Distance : %.2f cm" % distance)
        
        distance = str(distance)  #convert float to str
        # send data to the host every 0.3 sec
        client_socket.send(distance.encode())  #encode
        time.sleep(0.2)
finally:
    client_socket.close()
    GPIO.cleanup()
    
