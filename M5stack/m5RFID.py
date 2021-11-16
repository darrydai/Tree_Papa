from m5stack import *
from m5stack_ui import *
from uiflow import *
import wifiCfg
from m5mqtt import M5mqtt
import unit



screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xb87272)

pahub_0 = unit.get(unit.PAHUB, unit.PORTA)
neopixel_0 = unit.get(unit.NEOPIXEL, unit.PORTB, 9)
neopixel_0.setBrightness(100)
neopixel_0.setColorFrom(1, 9, 0xff0000)
rfid0 = unit.get(unit.RFID, unit.PAHUB0)
rfid1 = unit.get(unit.RFID, unit.PAHUB1)
rfid2 = unit.get(unit.RFID, unit.PAHUB2)

pahub_0.select(0, 1)
pahub_0.select(1, 1)
pahub_0.select(2, 1)

playState = '0'
rfidNum = 0
IDs = [0, 0, 0,0,0]

RFID_1 = M5Label('RFID_1:', x=23, y=53, color=0xffffff, font=FONT_MONT_28, parent=None)
RFID_2 = M5Label('RFID_2', x=23, y=83, color=0xffffff, font=FONT_MONT_28, parent=None)
RFID_3 = M5Label('RFID_3', x=23, y=113, color=0xffffff, font=FONT_MONT_28, parent=None)

ID_1 = M5Label('ID_1', x=150, y=53, color=0xffffff, font=FONT_MONT_28, parent=None)
ID_2 = M5Label('ID_2', x=150, y=83, color=0xffffff, font=FONT_MONT_28, parent=None)
ID_3 = M5Label('ID_3', x=150, y=113, color=0xffffff, font=FONT_MONT_28, parent=None)


videostate = M5Label('videoState =', x=12, y=184, color=0xffffff, font=FONT_MONT_28, parent=None)
state = M5Label('state', x=200, y=184, color=0xffffff, font=FONT_MONT_28, parent=None)

wifiCfg.doConnect('Jicms-Mesh', 'Jicms@tpe')
while not (wifiCfg.wlan_sta.isconnected()):
  pass

def fun_park_board_1_videoState_(topic_data):
  global playState
  playState = topic_data
  state.set_text(playState)
  pass

m5mqtt = M5mqtt('', '192.168.10.115', 1883, '', '', 300)
m5mqtt.subscribe(str('park/board/1/videoState'), fun_park_board_1_videoState_)
m5mqtt.start()
neopixel_0.setColorFrom(1, 9, 0x00000)
screen.set_screen_bg_color(0x8a2828)

# def rfidRead():
#   global rfidNum
#   if playState =='0':
#     neopixel_0.setColorFrom(1, 3, 0x00000)
#     if rfid0.isCardOn():
#       IDs[0] = str((rfid0.readUid()))
#       ID_1.set_text(str(IDs[0]))
#       rfidNum = 1
#       speaker.playTone(311, 1)
#       if IDs[0] != '':
#         m5mqtt.publish(str('park/registration/in/rfid/id'),str(IDs[0]))
#         m5mqtt.publish(str('park/board/1/RFID/1/playback'),str(1))
#         neopixel_0.setColorFrom(1, 1, 0x009900)
#         wait(1)
#         neopixel_0.setColorFrom(1, 1, 0xffffff)
#     elif rfid1.isCardOn():
#       IDs[1] = str((rfid1.readUid()))
#       ID_2.set_text(str(IDs[1]))
#       rfidNum = 2
#       speaker.playTone(311, 1)
#       if IDs[1] != '':
#         m5mqtt.publish(str('park/registration/in/rfid/id'),str(IDs[1]))
#         m5mqtt.publish(str('park/board/1/RFID/1/playback'),str(2))
#         neopixel_0.setColorFrom(2, 2, 0x009900)
#         wait(1)
#         neopixel_0.setColorFrom(2, 2, 0xffffff)
#     elif rfid2.isCardOn():
#       IDs[2] = str((rfid2.readUid()))
#       ID_3.set_text(str(IDs[2]))
#       rfidNum = 3
#       speaker.playTone(311, 1)
#       if IDs[2] != '':
#         m5mqtt.publish(str('park/registration/in/rfid/id'),str(IDs[2]))
#         m5mqtt.publish(str('park/board/1/RFID/1/playback'),str(3))
#         neopixel_0.setColorFrom(3, 3, 0x009900)
#         wait(1)
#         neopixel_0.setColorFrom(3, 3, 0xffffff)
#   else:
#     if rfid0.isCardOn() and rfidNum != 1:
#       speaker.playTone(311, 1)
#       neopixel_0.setColorFrom(1, 1, 0xffcc00)
#       wait(1)
#       neopixel_0.setColorFrom(1, 1, 0x00000)
#     elif rfid1.isCardOn() and rfidNum != 2:
#       speaker.playTone(311, 1)
#       neopixel_0.setColorFrom(2, 2, 0xffcc00)
#       wait(1)
#       neopixel_0.setColorFrom(2, 2, 0x00000)
#     elif rfid2.isCardOn() and rfidNum != 3:
#       speaker.playTone(311, 1)
#       neopixel_0.setColorFrom(3, 3, 0xffcc00)
#       wait(1)
#       neopixel_0.setColorFrom(3, 3, 0x00000)

while True:
  try :
    # rfidRead()
    if playState =='0':
      neopixel_0.setColorFrom(1, 9, 0xffffff)
      if rfid0.isCardOn():
        IDs[0] = str((rfid0.readUid()))
        ID_1.set_text(str(IDs[0]))
        rfidNum = 1
        if IDs[0] != '':
          m5mqtt.publish(str('park/registration/in/rfid/id'),str(IDs[0]))
          m5mqtt.publish(str('park/board/1/RFID/1/playback'),str(1))
          speaker.playTone(311, 1)
          neopixel_0.setColorFrom(1, 3, 0x009900)
          wait(1)
          neopixel_0.setColorFrom(1, 3, 0xffffff)
      elif rfid1.isCardOn():
        IDs[1] = str((rfid1.readUid()))
        ID_2.set_text(str(IDs[1]))
        rfidNum = 2
        if IDs[1] != '':
          m5mqtt.publish(str('park/registration/in/rfid/id'),str(IDs[1]))
          m5mqtt.publish(str('park/board/1/RFID/1/playback'),str(2))
          speaker.playTone(311, 1)
          neopixel_0.setColorFrom(4, 6, 0x009900)
          wait(1)
          neopixel_0.setColorFrom(4, 6, 0xffffff)
      elif rfid2.isCardOn():
        IDs[2] = str((rfid2.readUid()))
        ID_3.set_text(str(IDs[2]))
        rfidNum = 3
        if IDs[2] != '':
          m5mqtt.publish(str('park/registration/in/rfid/id'),str(IDs[2]))
          m5mqtt.publish(str('park/board/1/RFID/1/playback'),str(3))
          speaker.playTone(311, 1)
          neopixel_0.setColorFrom(7, 9, 0x009900)
          wait(1)
          neopixel_0.setColorFrom(7, 9, 0xffffff)
    else:
      if rfid0.isCardOn() and rfidNum != 1:
        speaker.playTone(311, 1)
        neopixel_0.setColorFrom(1, 3, 0xffcc00)
        wait(1)
        neopixel_0.setColorFrom(1, 3, 0xffffff)
      elif rfid1.isCardOn() and rfidNum != 2:
        speaker.playTone(311, 1)
        neopixel_0.setColorFrom(4, 6, 0xffcc00)
        wait(1)
        neopixel_0.setColorFrom(4, 6, 0xffffff)
      elif rfid2.isCardOn() and rfidNum != 3:
        speaker.playTone(311, 1)
        neopixel_0.setColorFrom(7, 9, 0xffcc00)
        wait(1)
        neopixel_0.setColorFrom(7, 9, 0xffffff)

  except Exception as e:
    print(str(e))
