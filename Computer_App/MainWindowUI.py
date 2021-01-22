#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.1 on Tue Jan 19 13:49:40 2021
#
# Caleb Schmurr
# schmurrcaleb@gmail.com


import wx
from pathlib import Path

import PinControlUI

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MainWindow(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainWindow.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1200, 800))
        self.SetTitle("AUNA Testing Software")        


        self.Notebook = wx.Notebook(self, wx.ID_ANY)

        self.Load_Existing_Test_Tab = wx.Panel(self.Notebook, wx.ID_ANY)
        self.Notebook.AddPage(self.Load_Existing_Test_Tab, "Load Test")

        Tab_Sizer = wx.BoxSizer(wx.VERTICAL)

        self.List_Of_Tests = wx.ListBox(self.Load_Existing_Test_Tab, wx.ID_ANY)
        self.List_Of_Tests.SetMinSize((500, 200))
        Tab_Sizer.Add(self.List_Of_Tests, 0, 0, 0)

        self.Load_Test = wx.Button(self.Load_Existing_Test_Tab, wx.ID_ANY, "Load Test")
        Tab_Sizer.Add(self.Load_Test, 0, 0, 0)

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        Tab_Sizer.Add(sizer_1, 1, wx.EXPAND, 0)

        COM_Port_Label = wx.StaticText(self.Load_Existing_Test_Tab, wx.ID_ANY, "Serial Port:")
        sizer_1.Add(COM_Port_Label, 0, 0, 0)

        self.Port_Connect = wx.ComboBox(self.Load_Existing_Test_Tab, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        sizer_1.Add(self.Port_Connect, 0, 0, 0)

        self.Connect_Button = wx.Button(self.Load_Existing_Test_Tab, wx.ID_ANY, "Connect")
        sizer_1.Add(self.Connect_Button, 0, 0, 0)

        self.Disconnect_Button = wx.Button(self.Load_Existing_Test_Tab, wx.ID_ANY, "Disconnect")
        sizer_1.Add(self.Disconnect_Button, 0, 0, 0)

        self.ShowPinUI_Button = wx.Button(self.Load_Existing_Test_Tab, wx.ID_ANY, "Show Pin UI")
        Tab_Sizer.Add(self.ShowPinUI_Button, 0, 0, 0)

        self.Test_Tab = wx.Panel(self.Notebook, wx.ID_ANY)
        self.Notebook.AddPage(self.Test_Tab, "Test")

        Test_Tab_Sizer = wx.BoxSizer(wx.VERTICAL)

        Current_Test_Label = wx.StaticText(self.Test_Tab, wx.ID_ANY, "Current Test:")
        Test_Tab_Sizer.Add(Current_Test_Label, 0, 0, 0)

        Next_Step_Image = wx.StaticBitmap(self.Test_Tab, wx.ID_ANY, wx.Bitmap("C:\\Users\\USER\\Documents\\Test_Box\\AUNA_Test_Box\\Computer_App\\demo_img.png", wx.BITMAP_TYPE_ANY))
        Test_Tab_Sizer.Add(Next_Step_Image, 0, 0, 0)

        Test_Status_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Test_Tab_Sizer.Add(Test_Status_Sizer, 1, wx.EXPAND, 0)

        label_2 = wx.StaticText(self.Test_Tab, wx.ID_ANY, "Status:")
        Test_Status_Sizer.Add(label_2, 0, 0, 0)

        label_3 = wx.StaticText(self.Test_Tab, wx.ID_ANY, "Operation:")
        Test_Status_Sizer.Add(label_3, 0, 0, 0)

        self.Next_Step_Button = wx.Button(self.Test_Tab, wx.ID_ANY, "Next Step")
        Test_Status_Sizer.Add(self.Next_Step_Button, 0, 0, 0)

        self.New_Test_Initiator_Tab = wx.Panel(self.Notebook, wx.ID_ANY)
        self.Notebook.AddPage(self.New_Test_Initiator_Tab, "New Test")

        Creator_Sizer = wx.BoxSizer(wx.VERTICAL)

        self.New_Test_Creator = wx.Panel(self.Notebook, wx.ID_ANY)
        self.Notebook.AddPage(self.New_Test_Creator, "New Test Creator")

        self.Result_Viewer = wx.Panel(self.Notebook, wx.ID_ANY)
        self.Notebook.AddPage(self.Result_Viewer, "Result Viewer")

        self.New_Test_Initiator_Tab.SetSizer(Creator_Sizer)

        self.Test_Tab.SetSizer(Test_Tab_Sizer)

        self.Load_Existing_Test_Tab.SetSizer(Tab_Sizer)

        self.Layout()
        # end wxGlade



#### To be placed under init of MainWindowUI ############################################################################################################
##########################################################################################################################################################
        
        

        self.PinControl = PinControlUI.Pin_Control(None, wx.ID_ANY, "")
        
        #Load up combo box.
        preferred_index = -1
        self.Port_Connect.Clear()
        for n, (portname, desc, hwid) in enumerate(sorted(PinControlUI.SerialComm.serial.tools.list_ports.comports())):
            self.Port_Connect.Append(u'{} - {}'.format(portname, desc))
            
        self.Port_Connect.SetSelection(preferred_index)
        self.__attach_events()
        self.loadTests()

    def __attach_events(self):

        self.Connect_Button.Bind(wx.EVT_BUTTON, self.ConnectPort)
        self.ShowPinUI_Button.Bind(wx.EVT_BUTTON, self.showPinUI)

        #self.PortConnect()

    #loadTests - load in the test procedures located in test folder.
    #Then populate the list with them.
    def loadTests(self):
        p = Path('.') #Using pathlib - replacement of os.
        p2 = p / "Tests"
        if p2.exists():
            for x in p2.iterdir():
                if x.is_dir():
                    self.List_Of_Tests.Append(x.name)
        else:
            print("error - Tests directory not found.")            

        

    def ConnectPort(self, events):
        self.PinControl.ExternalStartSerial(self.Port_Connect.GetSelection())
        #Disable the connect button.

    def showPinUI(self, events):
        self.PinControl.Show()
        #TODO: Change the PinControlUI to be able to be 'closed', made
        #not visible anymore and then able to be made visible again.


##################################################################################################################################################################

# end of class MainWindow

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainWindow(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
