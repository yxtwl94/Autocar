# Autocar

# Hardware

Raspberry 3B+
L298N*2
Ultraschallsensor HC-SR04
Kabel

motors ist angetrieben von L298N

kein PWM

9V voltage für L298N


# Software
mit python3

es gibt 3 Server für Bilder und Ultraschallsensor Daten Übertragung und RC Control.

In PC gibt es 2 Server, um Daten von Rpi zu empfangen und die Command zu Rpi geben

Neuro Network haben 3 Ebenen und benutzt MLP

# Test


1.In PC run 'camera_regist.py' Rpi run 'camera_cali.py' mache Bild registrierung

2.Pc run 'collect_training_data.py' ，Rpi run 'motor.py' und 'stream_client.py'，use keyboard to control motor and collect photos，the photos will automatisch stored

3.pc run 'mlp_training.py' ,and generate model

4.PC run 'rc_drive.py' ,Rpi run 'ultrasonic_client.py'，'stream_client.py'，'motor.py' and the car will run itself


# by yxt: yxtwl95@hotmail.com
