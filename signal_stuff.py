#!/usr/bin/python

from DataPacket import DataPacket
import time

def retrieve_status(did):
    packet=DataPacket(id=did,instr=0x01,data=[0x01])
    a=packet.getCharPacket()
    packet.writeToSerial(a)
    time.sleep(0.03)
    temp=packet.readSerial(6)
    ret=[]
    for i in range(0,6):
        ret.append(ord(temp[i]))
        
    return ret[4] 
    
def change_did(old_did,new_did):
    packet=DataPacket(id=old_did,instr=0x02,data=[0x04,new_did])
    a=packet.getCharPacket()
    packet.writeToSerial(a)
    
    return retrieve_status(new_did)

def change_led(did,value):
    
    
    cmd=0x03
    
    if value=='TOGGLE':
        cmd = 0x02
    if value == 'ON':
        cmd = 0x01
    if value == 'OFF':
        cmd = 0x00
    packet=DataPacket(id=did,instr=0x02,data=[0x05,cmd])
    a=packet.getCharPacket()
    packet.writeToSerial(a)
    
    return retrieve_status(did)
    
def dispense(did):
    packet=DataPacket(id=did,instr=0x02,data=[0x01])
    a=packet.getCharPacket()
    packet.writeToSerial(a)
    
def retract(did):
    packet=DataPacket(id=did,instr=0x02,data=[0x02])
    a=packet.getCharPacket()
    packet.writeToSerial(a)    