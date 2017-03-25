# coding: UTF-8

#from  daemon import DaemonContext
#from daemon.pidlockfile import PIDLockFile

import serial
import sys
import time
import binascii
import os
import numpy as np
import json

#from numba import jit
import paho.mqtt.client as mqtt
from numpy import arange

def func():
    #パラメータをファイルから読み込み
    f = open("serial_test_param.json","r")
    param = json.load(f)

    host = param["MQTT_IP"]
    port = param["MQTT_PORT"]
    serial_com = param["BLUETOOTH_COM"]


    topic = 'mouse'
    elapsed_time = 0.0
    # インスタンス作成時に protocol v3.1.1 を指定します
    client = mqtt.Client(protocol=mqtt.MQTTv311)

    client.connect(host, port=port, keepalive=60)
    client.publish("TEST", "this is python script")

    #fo = open('spam.txt', 'w')
    #sys.stdout = fo

    try:
        ser = serial.Serial(serial_com,timeout = 5)
        print(serial_com +" is opend.")
        client.publish("TEST", "Connected Bluetooth ")
    except:
        print (serial_com +" cannot open.")
        client.publish("TEST", "Cannot connect Bluetooth")
        client.disconnect()
        return

    client.publish("TEST", "data send start!")

    func2(client,ser)

def func2(client,ser):
    buff = np.array([],dtype="uint8")
    s = np.array([],dtype="uint8")
    st = np.array([],dtype="uint8")
    st_bytes=b""
    length = 0
    i      = 0
    start  = 0
    timestamp = 0
    timestamp_pre = 0
    message_len = 250

    print (len(buff))
    while True:
        start = time.time()
        #for ele in ser.read(100):
        #    s = np.append(s,ele)
        s = [ele for ele in ser.read(250)]
        #print(s)
        buff = np.r_[buff,s]
        length = buff.size
        
        for i in range(length-4):

            if  (length-i > message_len) and (buff[i] == 0xff)  and \
                (buff[i+1] == 0xff) and (buff[i+2]==0x48) and (buff[i+3]==0x45) and \
                (buff[i+4] == 0x41) and (buff[i+5]==0x44) :
                timestamp_pre = timestamp
                timestamp = buff[11] 
                st = buff[i:i+message_len]
                st_bytes = binascii.hexlify(bytes(list(st)))
                chk_sum = 0
                for k in range(7,250):
                    chk_sum =  chk_sum + st[k]
                # print (chk_sum%256 ,st[6] ,st[11],  st_bytes)
                if chk_sum%256 != st[6]:
                    print("bad!")
                print(chk_sum%256,st[6],st[11])
                client.publish("mouse", bytes(list(st)))
                buff = buff[i+message_len:]
                break
        elapsed_time = time.time() - start
        print (elapsed_time,buff.size,timestamp, (timestamp-timestamp_pre+256)%256  )

        if(elapsed_time > 5.0):
            ser.close()
            
            print("COM" + " is busy.")
            client.publish("TEST", "COM" +" is busy!")
            client.disconnect()
            print("exit!")
            sys.exit()
            return

if __name__ == "__main__":
     while True:
         func()
