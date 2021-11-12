import configparser
import paho.mqtt.client as mqtt
from omxplayer.player import OMXPlayer
import keyboard
import subprocess
from pathlib import Path
from time import sleep

# init config file
config = configparser.ConfigParser()
config.read('/home/pi/mqtt_Player/mqtt_Player.ini')

background = 'sudo fbi -noverbose -d -a /dev/fb0 -T 1 /home/pi/mqtt_Player/data/backGround/Idle.jpg'
# video
VIDEO_PATH = config['video']['VIDEO_PATH']
VIDEO_IDLE = config['video']['VIDEO_idle']
VIDEO_A = config['video']['VIDEO_A']
VIDEO_B = config['video']['VIDEO_B']
VIDEO_C = config['video']['VIDEO_C']

# init video number
video_Num = 1
# init video State
video_State = '0'
# init RFID reader
reader_Num = '0'

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
treePaPa = subprocess.Popen(background, shell=True)

# def playerExit(code, num):
#     player.load(VIDEO_PATH+VIDEO)

player1 = OMXPlayer(VIDEO_PATH+VIDEO_IDLE,args='--loop' ,dbus_name='org.mpris.MediaPlayer2.omxplayer1')
# player.exitEvent += lambda _, exit_code: playerExit(exit_code, 'VIDEO_A_END')

while True:
    try:
        if reader_Num == '1':
            client.publish("park/board/1/videoState", '1')
            while player1.position() < 2.85:
                pass
            # player.load(VIDEO_PATH+VIDEO_C)
            player1.pause()
            player1.set_position(0)
            player2 = OMXPlayer(VIDEO_PATH+VIDEO_A,dbus_name='org.mpris.MediaPlayer2.omxplayer2')
            sleep(0.1)
            while player2.position() < 5.85:
                pass
            player2.quit()
            sleep(0.1)
            player1.play()
            reader_Num=0
            client.publish("park/board/1/videoState", '0')
        if reader_Num == '2':
            client.publish("park/board/1/videoState", '1')
            while player1.position() < 2.85:
                pass
            # player.load(VIDEO_PATH+VIDEO_C)
            player1.pause()
            player1.set_position(0)
            player3 = OMXPlayer(VIDEO_PATH+VIDEO_B,dbus_name='org.mpris.MediaPlayer2.omxplayer3')
            sleep(0.1)
            while player3.position() < 5.85:
                pass
            player3.quit()
            sleep(0.1)
            player1.play()
            reader_Num=0
            client.publish("park/board/1/videoState", '0')
        if reader_Num == '3':
            client.publish("park/board/1/videoState", '1')
            while player1.position() < 2.85:
                pass
            # player.load(VIDEO_PATH+VIDEO_C)
            player1.pause()
            player1.set_position(0)
            player4 = OMXPlayer(VIDEO_PATH+VIDEO_C,dbus_name='org.mpris.MediaPlayer2.omxplayer2')
            sleep(0.1)
            while player4.position() < 5.85:
                pass
            player4.quit()
            sleep(0.1)
            player1.play()
            reader_Num=0
            client.publish("park/board/1/videoState", '0')
        # if keyboard.is_pressed('q'):
        #     player1.quit()
        #     break
    except Exception as e:
      print("Program terminated: ", e)