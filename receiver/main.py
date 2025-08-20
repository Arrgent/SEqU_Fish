import time
import json
import sys
import socket
import  _thread
import network
import espnow
from rotary_irq_esp import RotaryIRQ
from machine import Pin, I2C,RTC,PWM,Timer
from neopixel import NeoPixel
#import ssd1306big
from ssd1306 import SSD1306_I2C
#------------------------------------
rtc=RTC()
print(rtc.datetime()[3])
timer1=Timer(1)
#------------------------------------
dt1=Pin(42,Pin.IN)
rele=Pin(39,Pin.OUT)
#------------------------------------
pin=Pin(48,Pin.OUT)
np=NeoPixel(pin,2)
np[0]=(10,10,10)
np.write()
#====================================
print("setting up i2c")
sda = Pin(8)
scl = Pin(9)
id = 0

i2c = I2C(sda=sda, scl=scl)
print(i2c.scan())
#----------------------------------------
# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.WLAN.IF_STA)
sta.active(True)
#sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)
print(sta.config('mac') )
peer = b'\xff\xff\xff\xff\xff\xff'   # MAC address of peer's wifi interface
e.add_peer(peer)      # Must add_peer() before send()
#----------------------------------------
oled=SSD1306_I2C(128,64,i2c,addr=0x3C)
#oled=ssd1306big
#oled.wrap('1')
oled.text('text,text',0,0,1)
oled.show()

#------------------------------------
r = RotaryIRQ(pin_num_clk=12, 
              pin_num_dt=13, 
              min_val=0, 
              max_val=5, 
              reverse=False, 
              range_mode=RotaryIRQ.RANGE_WRAP)
              
val_old = r.value()
#===========================================================
nx1=(0,200,200)
nx2=(200,10,20)
nx3=(10,200,20)
nx4=(200,200,20)
dtnx=(250,100,250)
pwm0=PWM(Pin(40),freq=20,duty_u16=32768)
pwm0.deinit()
#-----------------------------------------------------------
def context(command,color):
    if msg==command:
        np[0]=color
        np.write()
        e.send(peer,b'okk')
        print(msg)
    return
#------------------------------
def signalon(command,color):
    if msg==command:
        np[0]=color
        np.write()
        pwm0.init(freq=1000,duty_u16=32768)
    return
#------------------------------
def signaloff(command,color):
    if msg==command:
        np[0]=color
        np.write()
        pwm0.deinit()
    return
#====================================
def signaler(t):
    pwm0.deinit()
    rele.off()
    np[0]=(0,0,10)
    np.write()
        
    e.send(peer,b'signoff')
#------------------------------
def dtmuving(color):
    if dt1.value() ==1:
        
        timer1.init(mode=Timer.ONE_SHOT,period=2000,callback=signaler)
        pwm0.init(freq=600,duty_u16=32768)
        np[0]=color
        np.write()
        rele.on()
        e.send(peer,b'signon')

    return    
#-----------------------------------------------------------
a=False
while True:
    
    dtmuving(dtnx)
    host, msg = e.recv(1)
    if msg:             # msg == None if timeout in recv()
        print(host, msg)
        context(b'pin1',nx1)
        context(b'pin3',nx2)   
        signalon(b'pinon',nx3)
        signaloff(b'pinoff',nx4)                        
        #---------------------    
        if msg == b'end':
           print( "bimgo")

#=============================================================        
    val_new = r.value()
    
    if val_old != val_new:
        val_old = val_new
        print('result =', val_new)
        oled.fill(0)
        oled.text(str(val_new), 0, 0, 1)
        oled.show()
    time.sleep_ms(50)
#------------------------------------
    continue   
#==========================================================

       