import config
import util
from threading import Thread
import time
import subprocess
import time
import json
import time
import serial 


class serialport:
    def __init__(self):
        self.serialport=None
        try:
            serialport = serial.Serial("/dev/ttyS1",9600,timeout=2)
        except EnvironmentError as err:
            print(err)
            serialport=None

    def setSystemTIme(self,datetime):
          t='SETDATE'+time.strftime('%Y%m%d%H%M%S',time.localtime(datetime))
          print(t)
          result = self.processCmd(t)
          if result is None:
            return False
          else:
            return result != "DATEFAILE8"

    def getSystemTime(self):
        cmd='GETDATE'
        result = self.processCmd(cmd)
        return result

    def setModeM(self):
        cmd='SETMODEM'
        result = self.processCmd(cmd)
        if result is None:
            return False
        else:
            return result != "MODEFAIL"

    def setModeD(self):
        cmd='SETMODED'
        result = self.processCmd(cmd)
        if result is None:
            return False
        else:
            return result != "MODEFAIL"

    def setModeN(self):
        cmd='SETMODEN'
        result = self.processCmd(cmd)
        if result is None:
            return False
        else:
            return result != "MODEFAIL"


    def setDailyTIme(self,openTime,closeTime):
        if self.setModeD:
            cmd='SETOPEN'+self.handleYMS(openTime)
            result=self.processCmd(cmd)
            if result is not None and result != "OPENFAIL":
               cmd='SETSTOP'+self.handleYMS(closeTime)
               result=self.processCmd(cmd)
               return result is not None and result != 'STOPFAIL'
        return False
    
    def getBat(self):
        cmd='GETBAT'
        result=self.processCmd(cmd)
        if result is not None and result!='通信超时':
            return result
        return None

    def processCmd(self,cmd):
        try:
            if self.serialport is not None:
                if not self.serialport.is_open():
                    self.serialport.open()
                    cmd+='\r'
                    self.serialport.write(cmd)
                    result=self.serialport.readline()
                    return result
            return None
        except EnvironmentError as err:
            print(err)
            return None
    def handleYMS(self,yms):
        arr=yms.split(':')
        return ''.join(arr)

instance=serialport()


