# -*- coding: utf-8 -*- 
from socket import *
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
client_socket=socket(AF_INET, SOCK_STREAM)
client_socket.connect(('192.168.137.1',8004))

Motor1A = 11
Motor1B = 12
Motor2A = 13
Motor2B = 15

Motor3A = 29
Motor3B = 31
Motor4A = 33
Motor4B = 35

command =0

#print("Setting up GPIO pins")
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)

GPIO.setup(Motor3A, GPIO.OUT)
GPIO.setup(Motor3B, GPIO.OUT)
GPIO.setup(Motor4A, GPIO.OUT)
GPIO.setup(Motor4B, GPIO.OUT)
	
	
def forward():
    print("going forward ")
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor2A, GPIO.LOW)
    GPIO.output(Motor2B, GPIO.HIGH)
    

def stop():
    print("Stoping")
    GPIO.output(Motor1A, False)
    GPIO.output(Motor1B, False)
    GPIO.output(Motor2A, False)
    GPIO.output(Motor2B, False)

def right():
    print("Turning right")
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)
    
def left():
    print("Turning left")
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor2A, GPIO.LOW)
    GPIO.output(Motor2B, GPIO.HIGH)
    
def forward_right():
    print("Turning forward right")
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)

def forward_left():
    print("Turning forward left")
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor2A, GPIO.LOW)
    GPIO.output(Motor2B, GPIO.HIGH)
    
def back():
    print("Turning back")
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)
        
def back_right():
    print("Turning back right")
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)
        
def back_left():
    print("Turning back left")
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor2A, GPIO.LOW)
    GPIO.output(Motor2B, GPIO.HIGH)

def send_command(command):
	
	if command==0:
		stop()
	if command==1:
		forward()
	if command==2:
		back()
	if command==3:
		right()
	if command==4:
		left()
	if command==6:
		forward_right()
	if command==7:
		forward_left()
	if command==8:
		back_right()
	if command==9:
		back_left()

try:
	while True:
		command=int(str(client_socket.recv(1024),encoding='utf-8'))
		send_command(command)
		
finally:
    client_socket.close()
    GPIO.cleanup()
    
