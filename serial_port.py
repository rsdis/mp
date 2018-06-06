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
        self.serialport = None
        try:
            #self.serialport = serial.Serial("/dev/tty8", 9600, timeout=5)
            self.serialport = serial.Serial("/dev/ttyS0", 9600, timeout=5)
        except EnvironmentError as err:
            print(err)
            self.serialport = None

    def setSystemTIme(self,datetime):
          t='SETDATE'+time.strftime('%Y%m%d%H%M%S',time.localtime(datetime))
          print(t)
          result = self.processCmd(t)
          if result is None:
            return False
          else:
            return result != "DATEFAILE8"

    def getSystemTime(self):
        cmd = 'GETDATE'
        result = self.processCmd(cmd)
        return result
    
    def getMode(self):
        cmd = 'GETMODE'
        result = self.processCmd(cmd)
        return result.decode()

    def setModeM(self):
        cmd='SETMODEM'
        result = self.processCmd(cmd)
        if result is None:
            return False
        else:
            # return result.decode()
            return True

    def setModeD(self):
        cmd='SETMODED'
        result = self.processCmd(cmd)
        if result is None:
            return False
        else:
            # return result.decode()
            return True

    def setModeN(self):
        cmd='SETMODEN'
        result = self.processCmd(cmd)
        if result is None:
            return False
        else:
            # return result.decode()
            return True


    def setDailyTIme(self,openTime,closeTime):
        if self.setModeD():
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
                if self.serialport.is_open == False:
                    self.serialport.open()
                cmd += '\r'
                self.serialport.write(cmd.encode())
                result = self.serialport.readline()
                util.log_info("fck_result", result.decode())
                return result
            return None
        except Exception as err:
            util.log_error("fck", err)
            return None

    def handleYMS(self,yms):
        arr=yms.split(':')
        return ''.join(arr)

instance=serialport()
# instance.getSystemTime()
#instance.getBat()
#instance.setSystemTIme(time.time())
instance.getMode()
#instance.setModeD()
#instance.setDailyTIme('03:19:00', '03:18:00')
