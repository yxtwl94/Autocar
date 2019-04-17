from picamera import PiCamera, Color
from time import sleep



demoCamera = PiCamera()
demoCamera.start_preview()    #打开摄像头预览
demoCamera.annotate_background = Color('white')
demoCamera.annotate_foreground = Color('red') 
demoCamera.resolution = (480, 320)      #设置摄像头的分辨率
demoCamera.framerate = 60                 #设定摄像头的帧率
sleep(2) 
demoCamera.capture('/home/pi/Desktop/chess16.jpg')    #拍下并保存一张照片
demoCamera.stop_preview()      #关闭摄像头预览
