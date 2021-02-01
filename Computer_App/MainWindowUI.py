#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.1 on Mon Feb  1 14:46:47 2021
#

import wx


###########################################################################
######Include this as well in the MainWindowUI#############################
import PinList
import SerialMonitor
import TestSequence
import PinControlUI

import logging

from pathlib import Path

#Change current directory to location of python file.
#Need to do this to load in tests properly.
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


###########################################################################
##################Finish Importing Logging#################################



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
        self.SetTitle("frame")

        self.Notebook = wx.Notebook(self, wx.ID_ANY)

        self.Load_Existing_Test_Tab = wx.Panel(self.Notebook, wx.ID_ANY)
        self.Notebook.AddPage(self.Load_Existing_Test_Tab, "Load Test")

        self.Tab_Sizer = wx.BoxSizer(wx.VERTICAL)

        self.List_Of_Tests = wx.ListBox(self.Load_Existing_Test_Tab, wx.ID_ANY, choices=["choice 1"])
        self.List_Of_Tests.SetMinSize((500, 200))
        self.Tab_Sizer.Add(self.List_Of_Tests, 0, 0, 0)

        self.Load_Test = wx.Button(self.Load_Existing_Test_Tab, wx.ID_ANY, "Load Test")
        self.Tab_Sizer.Add(self.Load_Test, 0, 0, 0)

        self.Com_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Tab_Sizer.Add(self.Com_Sizer, 1, wx.EXPAND, 0)

        self.COM_Port_Label = wx.StaticText(self.Load_Existing_Test_Tab, wx.ID_ANY, "Serial Port:")
        self.Com_Sizer.Add(self.COM_Port_Label, 0, 0, 0)

        self.Port_Connect = wx.ComboBox(self.Load_Existing_Test_Tab, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        self.Com_Sizer.Add(self.Port_Connect, 0, 0, 0)

        self.Connect_Button = wx.Button(self.Load_Existing_Test_Tab, wx.ID_ANY, "Connect")
        self.Com_Sizer.Add(self.Connect_Button, 0, 0, 0)

        self.Disconnect_Button = wx.Button(self.Load_Existing_Test_Tab, wx.ID_ANY, "Disconnect")
        self.Com_Sizer.Add(self.Disconnect_Button, 0, 0, 0)

        self.ShowPinUI_Button = wx.Button(self.Load_Existing_Test_Tab, wx.ID_ANY, "Show Pin UI")
        self.Tab_Sizer.Add(self.ShowPinUI_Button, 0, 0, 0)

        self.Test_Tab = wx.Panel(self.Notebook, wx.ID_ANY)
        self.Notebook.AddPage(self.Test_Tab, "Test")

        self.Test_Tab_Sizer = wx.BoxSizer(wx.VERTICAL)

        self.Current_Test_Label = wx.StaticText(self.Test_Tab, wx.ID_ANY, "Current Test:")
        self.Test_Tab_Sizer.Add(self.Current_Test_Label, 0, 0, 0)

        self.Next_Step_Image = wx.StaticBitmap(self.Test_Tab, wx.ID_ANY, wx.Bitmap("C:\\Users\\USER\\Documents\\Test_Box\\AUNA_Test_Box\\Computer_App\\demo_img.png", wx.BITMAP_TYPE_ANY))
        self.Next_Step_Image.SetMinSize((1000, 500))
        self.Test_Tab_Sizer.Add(self.Next_Step_Image, 0, 0, 0)

        self.Test_Status_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Test_Tab_Sizer.Add(self.Test_Status_Sizer, 1, wx.EXPAND, 0)

        self.Test_Status_Label = wx.StaticText(self.Test_Tab, wx.ID_ANY, "Status:")
        self.Test_Status_Label.SetMinSize((200, 16))
        self.Test_Status_Sizer.Add(self.Test_Status_Label, 0, 0, 0)

        self.Stage_Description_Label = wx.StaticText(self.Test_Tab, wx.ID_ANY, "Operation:")
        self.Stage_Description_Label.SetMinSize((200, 16))
        self.Test_Status_Sizer.Add(self.Stage_Description_Label, 0, 0, 0)

        self.Next_Step_Button = wx.Button(self.Test_Tab, wx.ID_ANY, "Next Step")
        self.Test_Status_Sizer.Add(self.Next_Step_Button, 0, 0, 0)

        self.New_Test_Initiator_Tab = wx.Panel(self.Notebook, wx.ID_ANY)
        self.Notebook.AddPage(self.New_Test_Initiator_Tab, "New Test")

        self.Creator_Sizer = wx.BoxSizer(wx.VERTICAL)

        self.New_Test_Creator = wx.Panel(self.Notebook, wx.ID_ANY)
        self.Notebook.AddPage(self.New_Test_Creator, "New Test Creator")

        self.Result_Viewer = wx.Panel(self.Notebook, wx.ID_ANY)
        self.Notebook.AddPage(self.Result_Viewer, "Result Viewer")

        self.New_Test_Initiator_Tab.SetSizer(self.Creator_Sizer)

        self.Test_Tab.SetSizer(self.Test_Tab_Sizer)

        self.Load_Existing_Test_Tab.SetSizer(self.Tab_Sizer)

        self.Layout()
        # end wxGlade


#### To be placed under init of MainWindowUI ############################################################################################################
##########################################################################################################################################################
        
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

        self.stopClose = False
        self.testActive = False

        self.PinControl = PinControlUI.Pin_Control(None, wx.ID_ANY, "")
        
        #Load up combo box.
        preferred_index = -1
        self.Port_Connect.Clear()
        for n, (portname, desc, hwid) in enumerate(sorted(PinControlUI.SerialComm.serial.tools.list_ports.comports())):
            self.Port_Connect.Append(u'{} - {}'.format(portname, desc))
            
        self.Port_Connect.SetSelection(preferred_index)
        self.__attach_events()
        self.loadTests()


        self.test = None #Currently loaded test
        self.currentStage = None #Currently loaded stage.

    def __attach_events(self):

        self.Connect_Button.Bind(wx.EVT_BUTTON, self.ConnectPort)
        self.ShowPinUI_Button.Bind(wx.EVT_BUTTON, self.showPinUI)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Load_Test.Bind(wx.EVT_BUTTON, self.LoadTestPushed)
        self.Next_Step_Button.Bind(wx.EVT_BUTTON, self.nextStepPushed)
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

    def OnClose(self, event):
        if self.stopClose:
            if wx.MessageBox("File has not been saved, continue closing?", "Please confirm below.", wx.ICON_QUESTION | wx.YES_NO) != wx.YES:
                event.veto()
                return

        #self.PinControl.stopUIThread()
        self.PinControl.closeSelf()
        self.Destroy()
        exit(0)

    #Load in the files for the test sequence after button click.
    def loadTestSequence(self, path):
        #Get a list of all files within the test folder
        if path.exists():
            logging.info("path exists")
            for x in path.iterdir():
                if x.is_file():
                    logging.debug("x is file")
                    if x.suffix == '.txt':
                        logging.debug("txt file found.")
                        self.test = TestSequence.TestSequence(self.PinControl.SerialLine.PinsList, x)
                    if x.suffix == '.png' or x.suffix == '.jpg' or x.suffix == '.bmp':
                        #If the suffix is an image,
                        pass
        else:
            print("Error  - file not found/path does not exist.")

        #Find the .txt, then parse in as json
        #Load the rest of the images, store in image container.
        #Need to make a class to contain it.

    #Load the Test selected, or say no test selected/display test error.
    def LoadTestPushed(self, event):
        #On load of test, open the test tab.
        if (self.List_Of_Tests.GetSelection()==-1):
            wx.MessageBox("Nothing selected.  No action able to be performed", "No Selected Test",  wx.OK | wx.ICON_INFORMATION)
            return
        #Initiate loading test in new tab.
        #Switch tab
        p = Path('.')
        p = p/"Tests"/self.List_Of_Tests.GetStringSelection()
        logging.debug(p)
        self.loadTestSequence(p)
        #logging.info(self.test.exportJsonFile())
        self.Notebook.SetSelection(1)
        self.testActive = True
        self.test.FolderPath = p
        self.startTest()


    #next step pushed
    def nextStepPushed(self, event):
        if self.testActive:
            if self.test.isNextTest():
                if self.currentStage.passPinCheck():
                    self.loadNextTestStage()
                else:
                    #Does not pass check
                    #Code this in.
                    pass
            else:
                self.finishTest()
        


    def startTest(self):
        self.Current_Test_Label.SetLabel("Current Test: {}".format(self.test.name))
        self.loadNextTestStage()

    def loadNextTestStage(self):
        self.currentStage = self.test.getNextTest()
        #Load in the image
        
        for x in self.test.FolderPath.iterdir():
            logging.debug("Checking for image {}".format(self.currentStage.imgpath))
            if x.is_file():
                logging.debug(x.name)
                if x.name==self.currentStage.imgpath:
                    logging.debug("Found image, updating.")
                    self.Next_Step_Image.SetBitmap(wx.Bitmap(str(x.resolve()), wx.BITMAP_TYPE_ANY))
        #Load in the test stage number, and adjust the status below
        self.Test_Status_Label.SetLabel("Stage {} out of {}".format(self.test.current_test, self.test.getNumStages()))
        #Change Operation to say Description.
        self.Stage_Description_Label.SetLabel("{}".format(self.currentStage.description))
        pass

    def finishTest(self):
        pass

###############################################################################################################################################

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
