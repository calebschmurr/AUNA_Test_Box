#PinStorage
'''
Store the pin list:
Keep track of active pins by name
Each pin also has associated properties: Input or Output, Pin Number, Value.

Also contains the methods for retrieiving commands that send information
between Computer and TestBox Arduino.

'''
import json

#mode: 0 is unused, 1 is input, 2 is output.
class pin:
    #CONSTANTS
    #The EqualValueVariant is used when checking if the pin is 'equal' to its
    #expected value.  This gives the software a little 'wiggle room', to account for
    #slight acceptable inconsistencies.  Lower or raise this tolerance for greater
    #or lesser accuracy.
    EqualValueVariant = 25


    #CLASS VARIABLES
    pin=0
    mode=0
    current_value=0
    description = ""
    check_code = 0
    expected_value = 0

    def __init__(self, pin, mode, expected_value, description="", check_code = 0):
        self.pin = pin
        self.mode = mode
        self.expected_value = expected_value
        self.description = description

    def getCurrentValue(self):
        return self.current_value
    
    def getExpectedValue(self):
        return self.expected_value

    def getMode(self):
        return self.mode
    
    def getPinNumber(self):  #Make sure getPinNumber returns an int.
        return int(self.pin)
    
    def getDescription(self):
        return self.description

    def setExpectedValue(self, value):
        if self.mode==2:
            self.expected_value = value
            return True
        #Throw error - pin not the right value.
        return False
    def setCheckCode(self, code):
        if self.mode==1:
            self.check_code = code
            return True
        #Else - throw error, return false.
        return False

    #Check Code Standards:
    # 0 - do nothing
    # 1 - less than
    # 2 - greater than
    # 3 - equal to
    def checkPin(self):
        if self.check_code == 0:
            return True
        elif self.check_code == 1:
            return self.current_value < self.expected_value
        elif self.check_code == 2:
            return self.current_value > self.expected_value
        elif self.check_code == 3:
            return (self.current_value - self.EqualValueVariant > self.expected_value) or (self.current_value + self.EqualValueVariant > self.expected_value)
        else:
            #Error - return false.
            return False

    def __getitem__(self, val):
        return getattr(self, val)

    def getDict(self):
        return {"pin": self.pin, "mode": self.mode, "description": self.description, "check_code" : self.check_code, "expected_value": self.expected_value}
        #Do not store the current_Value when getting dictionary value - the current value only matters within pin structure.

    #Store the pin number, the check code, and the expected value.
    def getTestStageDict(self):
        return {"pin": self.pin, "check_code": self.check_code, "expected_value": self.expected_value}

    #testSequenceDict - store the pins used and their description.
    def getTestSequenceDict(self):
        return {"pin": self.pin, "description": self.description}


class PinsList:
    PinList = []

    #addPin() - method to add pin values.
    #Pretty simple addPin method.

    def addPin(self, pin_num, mode, val=0, desc="", check_code=0):
        #Check to see if pin already exists:
        for x in self.PinList:
            if x.getPinNumber()==pin_num:
                return False
        self.PinList.append(pin(pin_num, mode, val, desc))
        return True

    #removePin() - method to remove a pin from the internal pin list.
    def removePin(self, num):
        for x in self.PinList:
            if x.getPinNumber()==num:
                self.PinList.remove(x)
                return True
        return False

    def clearList(self):
        #Clear all pins on the pinlist.
        self.pinList = []
    #changePinExpectedValue - find the pin in internal list, change the stored
    #value of pin.
    def changePinExpectedValue(self, num, value):
        for x in self.PinList:
            if x.getPinNumber()==num:
                return x.setExpectedValue(value)
        return False

    def changePinCheckCode(self, num, check_code):
        for x in self.PinList:
            if x.getPinNumber()==num:
                return x.setCheckCode(check_code)
        return False

    #changeCurrentValue - find the pin in internal list, and update
    #the CurrentValue accordingly.
    #CurrentValue is just the value of the pin itself.
    def changePinCurrentValue(self, num, value):
        for x in self.PinList:
            if x.getPinNumber()==num:
                return x.setCurrentValue(value)
        return False


    def getPinCurrentValue(self, num):
        for x in self.PinList:
            if x.getPinNumber()==num:
                return x.getCurrentValue()
        return -1
    
    def getPinExpectedValue(self, num):
        for x in self.PinList:
            if x.getPinNumber()==num:
                return x.getExpectedValue()
        return -1

    #checkIfPin() - method to see if the pin exists.
    def checkIfPin(self, num):
        for x in self.PinList:
            if x.getPinNumber()==num:
                return True
        return False

    #getPinsStartOutputCmd() - 
    #Method to return the command which will signal
    #Arduino/Elegoo to output the time.
    def getPinsStartOutputCmd(self, time):
        output = "2:1."
        output+=str(time)
        output+="!\n"
        return output

    #getPinsEndOutputCmd() - 
    #Return value that tells the output to stop sending cmd.
    def getPinsEndOutputCmd(self):
        return "2:0.0!\n"

    #getPinsInitializeCmd() - 
    #Return the pins initialize cmd.
    #Fixed 6/9/21 to match new standard.
    def getPinsInitializeCmd(self):
        output = "1:"
        for x in self.PinList:
            if x.getPinNumber()<10:
                output+="0"
                output+=f"{x.getPinNumber()}"
            else:
                output+=f"{x.getPinNumber()}"
            output+=";"
        output+="!\n"
        return output
        
    def getPinsResetCmd(self):
        return "0"
    #changePinOutputVal() - 
    #Change the output value of an input pin.

    def getFullResetCmd(self):
        print("full reset command accessed.")
        return "4"

    def changePinOutputVal(self):
        output="3:"
        for x in self.PinList:
            if x.getMode()==1:
                if x.getPinNumber()<10:
                    output+="0"
                output+=str(x.getPinNumber())
                output+="."
                if x.getValue()<100:
                    output+="0"
                if x.getValue()<10:
                    output+="0"
                output+=str(int(x.getValue()))
                output+=","
        output+="!\n"
        return output

#parseInputInfo() - method to 
#Receive the input information from serial,
#Decode into usable info.

    def parseInputInfo(self, inputstr):
        #Parse the input from Arduino:
        #Sample input:   * #1;01:2.2;02:3.2;05:1.2;07:1.8;
        if (inputstr[0:2]=="#1"):
            #If the input command is starting with one,
            #Cut out the beginning of the string:
            inputstr = inputstr[3:len(inputstr)]
            #Begin parsing:
            #Split up line by ;
            inputstr = inputstr.split(",")
            #For each pin mentioned, update the pin value:
            for z in inputstr:
                    #Check if the pin is an active pin.
                try:
                    if(z[0]=='!'):
                        break
                    z = z.split(":")
                    if z[0][0]=='A':
                        z[0][0]=8
                    elif z[0][1]=='A':
                        z[0][1]=8
                    if self.checkIfPin(int(z[0])):
                        self.changePinCurrentValue(int(z[0]), float(z[1]))
                    else:
                        print("Error - unable to change value of pin {}".format(z[0]))
                except:
                    print("error - retrying later.")
                        #Throw error
                    
                #Parse by the :
                #Check if the pin is enabled or not.
                #If not, throw an error.
                #If yes, then change the value.

        #Update UI?


    def getDict(self):
        output = {"pins":[]}
        for x in self.PinList:
            output["pins"].append(x.getDict())
        
        return output

    def getTestStageDict(self):
        output = {"pins":[]}
        for x in self.PinList:
            output["pins"].append(x.getTestStageDict())
        return output

    def getTestSequenceDict(self):
        output = {"pins":[]}
        for x in self.PinList:
            output["pins"].append(x.getTestSequenceDict())
        return output