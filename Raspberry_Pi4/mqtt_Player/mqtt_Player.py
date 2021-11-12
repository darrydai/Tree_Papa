import sys
import queue
import threading
import trace
import queue
import subprocess
import os
import signal
import configparser
import paho.mqtt.client as mqtt
from omxplayer.player import OMXPlayer
from time import sleep

# init config file
config = configparser.ConfigParser()
config.read('/home/pi/Documents/mqtt_Player/mqtt_Player.ini')

# video
VIDEO_PATH = config['video']['VIDEO_PATH']
VIDEO_IDLE = config['video']['VIDEO_IDLE']
VIDEO_A = config['video']['VIDEO_A']
VIDEO_B = config['video']['VIDEO_B']
VIDEO_C = config['video']['VIDEO_C']

black = 'sudo fbi -noverbose -d -a /dev/fb0 -T 1 /home/pi/Documents/mqtt_Player/data/backGround/Idle_00000.jpg'

# init video number
video_Num = 1

video_State = '0'

# init RFID reader
reader_Num = '0'


class thread_with_trace(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # 將訂閱主題寫在on_connet中
    # 如果我們失去連線或重新連線時
    # 地端程式將會重新訂閱
    client.subscribe("park/board/1/RFID/1/playback")

# 當接收到從伺服器發送的訊息時要進行的動作


def on_message(client, userdata, msg):
    global reader_Num
    reader_Num = msg.payload.decode('utf-8')
    # 轉換編碼utf-8才看得懂中文
    print(msg.topic+" " + msg.payload.decode('utf-8'))


# 連線設定
# 初始化地端程式
client = mqtt.Client()

# 設定連線的動作
client.on_connect = on_connect

# 設定接收訊息的動作
client.on_message = on_message

# 設定登入帳號密碼
# client.username_pw_set("try","xxxx")

# 設定連線資訊(IP, Port, 連線時間)
client.connect("192.168.1.110", 1883, 120)

# 開始連線，執行設定的動作和處理重新連線問題
# 也可以手動使用其他loop函式來進行連接
# client.loop_forever()
client.loop_start()


def playerExit(code, num):
    global video_Num
    video_Num = num


# blackBG = subprocess.Popen(black, shell=True)
# player = OMXPlayer(VIDEO_PATH+VIDEO_IDLE, args='--loop --orientation 270')
idel = OMXPlayer(VIDEO_PATH+VIDEO_IDLE,args='--loop')
# player.exitEvent += lambda _, exit_code: playerExit(exit_code, 'beep')
sleep(5)
idel.play()
client.publish("park/board/1/videoState", '0')
print("hi")
while True:
    # print(player.position())
    try:
      if reader_Num == '1':
        # while video_Num != 'beep':
        #     # print("video5")
        #     pass
        client.publish("park/board/1/videoState", '1')
        while idel.position() < 5.8:
            # print("video5")
            pass
        idel.quit()
        #player = OMXPlayer(VIDEO_PATH+VIDEO_A,args='--orientation 270')
        playera = OMXPlayer(VIDEO_PATH+VIDEO_A)
        playera.exitEvent += lambda _, exit_code: playerExit(exit_code, 'VIDEO_A_END')
        sleep(1)
        playera.play()
        while video_Num != 'VIDEO_A_END':
            # print("video5")
            pass
        # player = OMXPlayer(VIDEO_PATH+VIDEO_IDLE,args='--loop --orientation 270')
        idel = OMXPlayer(VIDEO_PATH+VIDEO_IDLE,args='--loop')
        # player.exitEvent += lambda _, exit_code: playerExit(exit_code, 'beep')
        sleep(1)
        idel.play()
        reader_Num = '0'
        sleep(3)
        client.publish("park/board/1/videoState", '0')
      elif reader_Num == '2':
        client.publish("park/board/1/videoState", '1')
        while idel.position() < 5.8:
            # print("video5")
            pass
        idel.quit()
        # player = OMXPlayer(VIDEO_PATH+VIDEO_B,args='--orientation 270')
        playerb = OMXPlayer(VIDEO_PATH+VIDEO_B)
        playerb.exitEvent += lambda _, exit_code: playerExit(exit_code, 'VIDEO_B_END')
        sleep(1)
        playerb.play()
        while video_Num != 'VIDEO_B_END':
            # print("video5")
            pass
        # player = OMXPlayer(VIDEO_PATH+VIDEO_IDLE,args='--loop --orientation 270')
        idel = OMXPlayer(VIDEO_PATH+VIDEO_IDLE,args='--loop')
        # player.exitEvent += lambda _, exit_code: playerExit(exit_code, 'beep')
        sleep(1)
        idel.play()
        reader_Num = '0'
        sleep(3)
        client.publish("park/board/1/videoState", '0')
      elif reader_Num == '3':
        client.publish("park/board/1/videoState", '1')
        while idel.position() < 5.8:
            # print("video5")
            pass
        idel.quit()
        # player = OMXPlayer(VIDEO_PATH+VIDEO_C,args='--orientation 270')
        playerc = OMXPlayer(VIDEO_PATH+VIDEO_C)
        playerc.exitEvent += lambda _, exit_code: playerExit(exit_code, 'VIDEO_C_END')
        sleep(1)
        playerc.play()
        while video_Num != 'VIDEO_C_END':
            # print("video5")
            pass
        # player = OMXPlayer(VIDEO_PATH+VIDEO_IDLE,args='--loop --orientation 270')
        idel = OMXPlayer(VIDEO_PATH+VIDEO_IDLE,args='--loop')
        # player.exitEvent += lambda _, exit_code: playerExit(exit_code, 'beep')
        sleep(1)
        idel.play()
        reader_Num = '0'
        sleep(3)
        client.publish("park/board/1/videoState", '0')
    except Exception as e:
      client.publish("park/board/1/videoState", '0')
      print("Program terminated: ", e)
