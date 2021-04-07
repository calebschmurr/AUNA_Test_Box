'''
Serial Comm System:
Control interactions over serial.
'''
import codecs
import serial
import threading
from serial.tools.miniterm import unichr

import PinList
import time

import wx

'''
Full Serial manager.
'''

class SerialHandler():

    def __init__(self):
        #On initiating - pull in main class.
        #Main reference class must have a class to handle
        #receiving the messages.
        self.PinsList = PinList.PinsList()
        self.serial = serial.Serial()
        self.alive = threading.Event()
        self.thread = None
        self.serial.timeout = 0.1

        self.UI_Update_Flag = False

        self.SerialCommList = []
        self.SerialCommListUpdated = False


    def config(self):
        pass

    def write(self, inputstr):
        #Write to the serial line.
        self.serial.write(inputstr.encode('utf-8', 'replace'))
        self.SerialCommList.append(">"+inputstr)
        self.SerialCommListUpdated = True

    def startReceiverThread(self):
        self.thread = threading.Thread(target=self.receiverThread)
        self.thread.setDaemon(True)
        self.thread.daemon = True
        self.alive.set()    #Alive stuff is pretty much copied from the wxTerminal example.
        self.thread.start()
        self.serial.rts = True
        self.serial.dtr = True


    def stopReceiverThread(self):
        if self.thread is not None:
            print("Clear thread")
            self.alive.clear()
            print("Join Thread")
            self.thread.join()
            print("make thread none")
            self.thread = None

    def receiverThread(self):
        while self.alive.isSet():
            time.sleep(0.2)
            b=self.serial.read(self.serial.in_waiting or 1).decode('UTF-8', 'replace')
            if b:
                self.PinsList.parseInputInfo(b)
                print(b)
                self.SerialCommList.append(b)
                self.SerialCommListUpdated = True
                b=""
                self.UI_Update_Flag=True
                
    def resetPins(self):
        print("Resetting pins.")
        print("Writing command: {}".format(self.PinsList.getPinsResetCmd()))
        self.write(self.PinsList.getPinsResetCmd())

    def fullReset(self):
        self.write(self.PinsList.getFullResetCmd())

    def InitializePins(self):
        #Initializing pins
        print("Initializaing pins w/ command {}".format(self.PinsList.getPinsInitializeCmd()))
        self.write(self.PinsList.getPinsInitializeCmd())

    def ChangeOutputPinValue(self):
        print("Changing output pin values w/ command {}".format(self.PinsList.changePinOutputVal()))
        self.write(self.PinsList.changePinOutputVal())

    def startOutputTime(self, time):
        print("Starting time w/ command {}".format(self.PinsList.getPinsStartOutputCmd(time)))
        self.write(self.PinsList.getPinsStartOutputCmd(time))

     
#Initiate Connection
    def initiateConnection(self, rate, port):
        self.serial.baudrate = rate
        self.serial.port = port
        try:
            self.serial.open()
            self.startReceiverThread()
            time.sleep(1.5)
            return True
        except serial.SerialException as e:
            with wx.MessageDialog(self, str(e), "Serial Port Error", wx.OK | wx.ICON_ERROR)as dlg:
                dlg.ShowModal()
        else:
            return False

#Stop Connection
    def stopConnection(self):
        try:
            self.stopReceiverThread()
            self.serial.close()
            self.SerialCommList = []
        except:
            print("Error stopping connection.")
        return True

    def getSerialActive(self):
        return self.serial.isOpen()

#Send the serial comm line.

