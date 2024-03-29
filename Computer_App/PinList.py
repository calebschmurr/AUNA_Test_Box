#PinStorage
'''
Store the pin list:
Keep track of active pins by name
Each pin also has associated properties: Input or Output, Pin Number, Value.

Also contains the methods for retrieiving commands that send information
between Computer and TestBox Arduino.

'''
import json
import logging

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def getPinsFromDict(dict):
    #In the dict, create a new pin for each item.
    retVal = []
    for x in dict:
        if (x['pin'] > 53) and (x['pin'] < 66): #Pin is an input pin.
            logging.debug("Got the pin check code into retVal for pin {} as {}".format(x['pin'], x['check_code']))
            retVal.append(pin(x['pin'], 1, x['expected_value'], "", x['check_code']))
        else: #Pin is an output pin.
            retVal.append(pin(x['pin'], 2, x['expected_value'], "", 0))

    logging.debug("retVal Output:")
    for x in retVal:
        logging.debug("Pin: {}, Check_Code: {}".format(x.getPinNumber(), x.getCheckCode()))
    return retVal

    


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
        self.check_code = check_code

    def getCurrentValue(self):
        return self.current_value
    
    def getExpectedValue(self):
        return self.expected_value

    def getCheckCode(self):
        return self.check_code

    def getMode(self):
        return self.mode
    
    def getPinNumber(self):  #Make sure getPinNumber returns an int.
        return int(self.pin)
    
    def getDescription(self):
        return self.description

    def setExpectedValue(self, value):
        if self.mode!=0:
            self.expected_value = int(value)
            print("New value set of ")
            print(value)
            return True
        #Throw error - pin not the right value.
        print("Error not the right mode for ")
        print(self.pin)
        return False
    
    def setCurrentValue(self, value):
        self.current_value = int(value)

    def setCheckCode(self, code):
        if self.mode==1:
            self.check_code = code
            print("Check code set for {} to {}".format(self.pin, code))
            return True
        #Else - throw error, return false.
        return False

    #Check Code Standards:
    # 0 - do nothing
    # 1 - less than
    # 2 - greater than
    # 3 - equal to
    def checkPin(self):
        logging.debug("CheckPin Called for pin {}".format(self.pin))
        logging.debug("Values found are: current_value {}, expected_value {}".format(self.current_value, self.expected_value))
        if self.check_code == 0:
            logging.debug("Check code is 0 for pin {}".format(self.pin))
            return True
        elif self.check_code == 1:
            logging.debug("Check code is 1 for pin {}".format(self.pin))
            return self.current_value < self.expected_value
        elif self.check_code == 2:
            logging.debug("Check code is 2 for pin {}".format(self.pin))
            return self.current_value > self.expected_value
        elif self.check_code == 3:
            logging.debug("Check code is 3 for pin {}".format(self.pin))
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
                print("Unable to add pin {} to list, it already exists.".format(pin_num))
                return False
        self.PinList.append(pin(pin_num, mode, val, desc))
        print("Added pin {} to PinList with mode {} val {}.".format(pin_num, mode, val))
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
        self.PinList = []
    #changePinExpectedValue - find the pin in internal list, change the stored
    #value of pin.
    def changePinExpectedValue(self, num, value):
        for x in self.PinList:
            if x.getPinNumber()==num:
                print("Reached change pin expected value for:")
                print(num)
                return x.setExpectedValue(value)
        print("Error setting expected value for ")
        print(num)
        return False

    def changePinCheckCode(self, num, check_code):
        for x in self.PinList:
            if x.getPinNumber()==num:
                print("Reached setting check code for {} to {}".format(num, check_code))
                return x.setCheckCode(check_code)
        print("Error setting check code for {}".format(num))
        return False

    #changeCurrentValue - find the pin in internal list, and update
    #the CurrentValue accordingly.
    #CurrentValue is just the value of the pin itself.
    def changePinCurrentValue(self, num, value):
        logging.debug("changePinCurrentValue called within PinList")
        for x in self.PinList:
            if x.getPinNumber()==num:
                logging.debug("Changing value of pin {} to {}".format(num, value))
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

    def getPinCheckCode(self, num):
        for x in self.PinList:
            if x.getPinNumber()==num:
                return x.getCheckCode()
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
        return "0\n"
    #changePinOutputVal() - 
    #Change the output value of an input pin.

    def getFullResetCmd(self):
        print("full reset command accessed.")
        return "4\n"

    def changePinOutputVal(self):
        output="3:"
        for x in self.PinList:
            if x.getMode()==2:
                if int(x.getPinNumber())<10:
                    output+="0"
                output+=str(x.getPinNumber())
                output+="."
                if int(x.getExpectedValue())<100:
                    output+="0"
                if int(x.getExpectedValue())<10:
                    output+="0"
                output+=str(int(x.getExpectedValue()))
                output+=","
        output+="!\n"
        return output

#parseInputInfo() - method to 
#Receive the input information from serial,
#Decode into usable info.

    def parseInputInfo(self, inputstr):
        logging.debug("Reached parseInputInfo.")
        #Parse the input from Arduino:
        #Sample input:   * 1;01:2.2;02:3.2;05:1.2;07:1.8;
        if (inputstr[0:2]=="#1"):
            logging.debug("Beginning to parse pins.")
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
                    logging.debug("Pin received: {}".format(z[0]))
                    if self.checkIfPin(int(z[0])):
                        logging.debug("Pin is a valid pin....")
                        self.changePinCurrentValue(int(z[0]), float(z[1]))
                        logging.debug("Finished changePinCurrentValue for {}".format(z[0]))
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
        output = []
        for x in self.PinList:
            output.append(x.getDict())
        
        return output

    def getTestStageDict(self):
        output = []
        for x in self.PinList:
            output.append(x.getTestStageDict())
        return output

    def getTestSequenceDict(self):
        output = []
        for x in self.PinList:
            output.append(x.getTestSequenceDict())
        return output