#PinStorage
'''
Store the pin list:
Keep track of active pins by name
Each pin also has associated properties: Input or Output, Pin Number, Value.

'''

class pin:
    pin_number=0
    mode='I'
    value=0
    description = ""

    def __init__(self, num, mode, value, description=""):
        self.pin_number = num
        self.mode = mode
        self.value = value
        self.description = description

    def getValue(self):
        return self.value
    def getMode(self):
        return self.mode
    def getPinNumber(self):
        return int(self.pin_number)
    def getDescription(self):
        return self.description

    def setValue(self, value):
        if self.mode=='I':
            self.value = value
            return True
        #Throw error - pin not the right value.
        return False


class PinsList:
    PinList = []

    #addPin() - method to add pin values.
    #Pretty simple addPin method.

    def addPin(self, num, mode, val=0, desc=""):
        #Check to see if pin already exists:
        for x in self.PinList:
            if x.getPinNumber()==num:
                return False
        self.PinList.append(pin(num, mode, val, desc))
        return True

    #removePin() - method to remove a pin from the internal pin list.
    def removePin(self, num):
        for x in self.PinList:
            if x.getPinNumber()==num:
                self.PinList.remove(x)
                return True
        return False

    #changePinValue - find the pin in internal list, change the stored
    #value of pin.
    def changePinValue(self, num, value):
        for x in self.PinList:
            if x.getPinNumber()==num:
                return x.setValue(value)
        return False

    def getPinValue(self, num):
        for x in self.PinList:
            if x.getPinNumber()==num:
                return x.getValue()
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
        output+="!"
        return output

    #getPinsEndOutputCmd() - 
    #Return value that tells the output to stop sending cmd.
    def getPinsEndOutputCmd(self):
        return "2:0.0!"

    #getPinsInitializeCmd() - 
    #Return the pins initialize cmd.
    def getPinsInitializeCmd(self):
        output = "1:"
        for x in self.PinList:
            if x.getPinNumber()<10:
                output+="0"
                output+="0"
                output+=f"{x.getPinNumber()}"
            elif x.getPinNumber()>79:
                if x.getPinNumber()<100:
                    output+="0"
                output+="A"
                output+=f"{x.getPinNumber()%10}"
            else:
                output+="0"
                output+=f"{x.getPinNumber()}"
            output+="."
            output+=x.getMode()
            output+=";"
        output+="!"
        return output
        
    def getPinsResetCmd(self):
        return "0"
    #changePinOutputVal() - 
    #Change the output value of an input pin.

    def changePinOutputVal(self):
        output="3:"
        for x in self.PinList:
            if x.getMode()=="O":
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
        output+="!"
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
                        self.changePinValue(int(z[0]), float(z[1]))
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