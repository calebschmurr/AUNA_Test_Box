#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.6 on Tue Jan 12 16:32:59 2021
#

import wx
import threading

import PinControlUI

import time

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

class Frame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Frame.__init__        
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((480, 300))
        self.Blower_Speed_Display = wx.TextCtrl(self, wx.ID_ANY, "")
        self.Temperature_Status = wx.TextCtrl(self, wx.ID_ANY, "")
        self.Louver_Setting = wx.TextCtrl(self, wx.ID_ANY, "")
        self.AC_SW_Display = wx.TextCtrl(self, wx.ID_ANY, "")
        

        self.__set_properties()
        self.__do_layout()
        self.PinControl = PinControlUI.Pin_Control(None, wx.ID_ANY, "")
        self.PinControl.Show()
        # end wxGlade
        self.thread = None
        self.alive = threading.Event()

        self.PinsConfigured = False

        self.thread = threading.Thread(target=self.UpdateLoop)
        self.thread.setDaemon(True)
        self.alive.set()
        self.thread.start()


    def __set_properties(self):
        # begin wxGlade: Frame.__set_properties
        self.SetTitle("frame")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Frame.__do_layout
        Main_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        AC_Setting = wx.BoxSizer(wx.VERTICAL)
        Louver_Sizer = wx.BoxSizer(wx.VERTICAL)
        Temp_Status_Sizer = wx.BoxSizer(wx.VERTICAL)
        Blower_Speed_Sizer = wx.BoxSizer(wx.VERTICAL)
        Blower_Speed_Setting = wx.StaticText(self, wx.ID_ANY, "Blower Speed Status:")
        Blower_Speed_Sizer.Add(Blower_Speed_Setting, 0, 0, 0)
        Blower_Speed_Sizer.Add(self.Blower_Speed_Display, 0, 0, 0)
        Main_Sizer.Add(Blower_Speed_Sizer, 1, wx.EXPAND, 0)
        Temp_Poti_Setting = wx.StaticText(self, wx.ID_ANY, "Temperature Status:")
        Temp_Status_Sizer.Add(Temp_Poti_Setting, 0, 0, 0)
        Temp_Status_Sizer.Add(self.Temperature_Status, 0, 0, 0)
        Main_Sizer.Add(Temp_Status_Sizer, 1, wx.EXPAND, 0)
        Louver_Setting_Status_Label = wx.StaticText(self, wx.ID_ANY, "Seat Setting:")
        Louver_Sizer.Add(Louver_Setting_Status_Label, 0, 0, 0)
        Louver_Sizer.Add(self.Louver_Setting, 0, 0, 0)
        Main_Sizer.Add(Louver_Sizer, 1, wx.EXPAND, 0)
        AC_SW_Label = wx.StaticText(self, wx.ID_ANY, "AC Switch Setting")
        AC_Setting.Add(AC_SW_Label, 0, 0, 0)
        AC_Setting.Add(self.AC_SW_Display, 0, 0, 0)
        Main_Sizer.Add(AC_Setting, 1, wx.EXPAND, 0)
        self.SetSizer(Main_Sizer)
        self.Layout()
        # end wxGlade

# end of class Frame

    def UpdateLoop(self):
        while(True):
            if self.PinControl.SerialLine.alive.isSet():
                if self.PinsConfigured:
                    #Receive and check pin inputs
                    #Cycle through all pin inputs, and update the status of the display as configured.
                    if self.PinControl.SerialLine.PinsList.getPinValue(54)>900:
                        self.Blower_Speed_Display.Value = "Speed 1"
                    elif self.PinControl.SerialLine.PinsList.getPinValue(55)>900:
                        self.Blower_Speed_Display.Value = "Speed 2"
                    elif self.PinControl.SerialLine.PinsList.getPinValue(56)>900:
                        self.Blower_Speed_Display.Value = "Speed 3"
                    else:
                        self.Blower_Speed_Display.Value = "Speed 0"

                    if self.PinControl.SerialLine.PinsList.getPinValue(57)>900:
                        self.AC_SW_Display.Value = "On"
                    else:
                        self.AC_SW_Display.Value = "Off"
                    if self.PinControl.SerialLine.PinsList.getPinValue(58)>900:
                        self.Louver_Setting.Value = "Head"
                    elif self.PinControl.SerialLine.PinsList.getPinValue(59)>900:
                        self.Louver_Setting.Value = "Defrost"
                    elif self.PinControl.SerialLine.PinsList.getPinValue(60)>900:
                        self.Louver_Setting.Value = "Feet&Defrost"
                    else:
                        self.Louver_Setting.Value = "Head&Feet"
                    
                    self.Temperature_Status.Value = str(self.PinControl.SerialLine.PinsList.getPinValue(61))
                    
                else:
                    self.SendPinConfig()
                    self.PinsConfigured = True
            time.sleep(.5)

    
    def SendPinConfig(self):
        #Use as input Analog 54 through 61
        for i in range(54,62):
            self.PinControl.externalAddPin(i, 0)

        #Pin Layout:
        #54:A0 is BlowerStep1
        #55:A1 is BlowerStep2
        #56:A2 is BlowerStep3
        #57:A3 is AC Signal
        #58:A4 is Air Flap Sig1
        #59:A5 is Air Flap Sig 2
        #60:A6 is Air Flap Sig3
        #61:A7 is WV Poti Sig


class MyApp(wx.App):
    def OnInit(self):
        self.Control_Panel_Test = Frame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.Control_Panel_Test)
        self.Control_Panel_Test.Show()
        return True

    

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
