
import time
import sys
import json
import network
import espnow
from neopixel import NeoPixel
import _thread

from machine import  Pin,I2C,RTC
#from ssd1306 import SSD1306_I2C
pinnp=Pin(33,Pin.OUT)
np=NeoPixel(pinnp,1)
np[0]=(10,10,10)
np.write()
pin1=Pin(34,Pin.IN,Pin.PULL_UP)
pin2=Pin(35,Pin.IN,Pin.PULL_UP)
pin3=Pin(32,Pin.IN,Pin.PULL_UP)
# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.WLAN.IF_STA)  # Or network.WLAN.IF_AP
sta.active(True)
#sta.disconnect()      # For ESP8266

e = espnow.ESPNow()
e.active(True)

peer = b'\x10\x00;Pz\xc8'   # MAC address of peer's wifi interface
e.add_peer(peer)      # Must add_peer() before send()
e.send(peer, "Starting...")
a=False 
while True :
   host, msg = e.recv(5)
   if msg:
       if msg==b'okk':
           np[0]=(200,0,0)
           np.write()
   #------------------------------------------
       if msg==b'signon':
           np[0]=(0,250,0)
           np.write()
       if msg==b'signoff':
           np[0]=(0,0,25)
           np.write()    
#================transeiver===================           
   if(pin1.value()==0):
      e.send(peer,"pin1")
    
      print("pin1")
   #------------------------------  
   if(pin2.value()==0):
       a=not a
       
       if a:        
          e.send(peer,"pinon")
          print(a)
       if a==False:
          e.send(peer,"pinoff")
          print(a)
   #-------------------------------       
   if(pin3.value()==0):
      e.send(peer,"pin3")
     
   time.sleep(0.1)
   
#e.send(peer, b'end')