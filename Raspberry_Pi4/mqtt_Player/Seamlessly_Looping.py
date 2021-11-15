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

player1 = OMXPlayer(VIDEO_PATH+VIDEO_IDLE,args='--loop --aspect-mode fill --no-osd' ,dbus_name='org.mpris.MediaPlayer2.omxplayer1')
# player2 = OMXPlayer(VIDEO_PATH+VIDEO_IDLE,args='' ,dbus_name='org.mpris.MediaPlayer2.omxplayer2')
# player1.pause()
# player2.pause()
# player1.play()
while True:
    try:
        player2 = OMXPlayer(VIDEO_PATH+VIDEO_B,args='--aspect-mode fill' ,dbus_name='org.mpris.MediaPlayer2.omxplayer2')
        player2.pause()
        while player1.position()<2.8:
            pass
        player2.play()
        player1.set_position(0)
        player1.pause()
        # player2.play()
        
#         # player1.set_position(0)
#         # player1.pause()
#         # player2.play()
        while player2.position()<5.8:
            pass
        player2.quit()
        player1.play()
#         # player2.set_position(0)
#         # player2.pause()
#         # player1.play()
    except Exception as e:
      print("Program terminated: ", e)