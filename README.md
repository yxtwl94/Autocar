# Autocar

# 硬件部分

树莓派3B+
L298N*2
超声波HC-SR04
线材若干

树莓派连接2个L298N,分别控制两对电机

L298N不用PWM调速，不用接使能端口

L298N用9V电池供电，树莓派用充电宝供电

树莓派连接超声波

# 软件部分
基于python3

树莓派有三个客户端，分别传输超声波，视频，电机控制数据

电脑端服务器三个线程，接收到图像和超声波(1,2线程)，通过神经网络和超声波数据输出动作指令(global prediction)给3线程

神经网络为MLP三层网络，采用回溯法确定参数，输入参数为120*320，是树莓派图像分辨率的下一半，因只取下半部分道路有效数据

# 操作部分

先测试看看各功能是否正常工作

1.电脑端运行camera_regist.py 树莓派运行camera_cali.py拍棋盘照，最好拍20个，电脑端参数应与棋盘格子数匹配

2.电脑端运行collect_training_data.py，树莓派运行motor.py和stream_client.py，控制小车在预定轨道行走，收集的数据会自动保存在training_data文件夹(新生成)下

3.电脑端运行mlp_training.py,确定生成的模型保存在saved_model文件下

4.电脑端运行rc_drive.py,树莓派运行ultrasonic_client.py，stream_client.py，motor.py 小车自动运行


# by yxt: yxtwl95@hotmail.com
