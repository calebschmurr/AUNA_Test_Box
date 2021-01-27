#class TestSequence - class to hold all information for a testing sequence for the AUNA box.
import PinList
import json

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class testPin:
    number = 0
    check_code = 0
    value = 0
    RealPinsList = None

    EqualValueVariant = 100

    def __init__(self, pin, check_code, value, RealPinsList):
        self.number = pin
        self.check_code = check_code
        self.value = value
        self.RealPinsList = RealPinsList

    #create method to perform check
    #Pin Check Codes:
    # -1 - invalid/not to do.
    # 0 - less than
    # 1 - greater than
    # 2 - equal to

    def checkPin(self):
        if self.check_code==0:
            return self.RealPinsList.getPinValue(self.number) < self.value
        elif self.check_code==1:
            return self.RealPinsList.getPinValue(self.number) > self.value
        elif self.check_code==2:
            return (self.RealPinsList.getPinValue(self.number) > (self.value - self.EqualValueVariant)) and (self.RealPinsList.getPinValue(self.number) < (self.value + self.EqualValueVariant))
    #create methods to get all values - not needed

    #create methods to change all values as well.

class testStage:
    number = 0
    description = ""
    imgpath = ""
    error = ""
    testPins = []


    def __init__(self, number, description, imgpath, pin_checks, RealPinsList):
        self.number = number
        self.description = description
        self.imgpath = imgpath
        self.parsePinChecks(pin_checks, RealPinsList)

    def parsePinChecks(self, pin_checks, RealPinsList):
        for x in pin_checks:
            self.testPins.append(testPin(x["pin"], x["check_code"], x["value"], RealPinsList))



class TestSequence:
    name = ""
    description = ""
    TestPinsList = PinList.PinsList()
    testStages = []
    RealPinsList = None #To be defined on init.
    current_test = -1

    def __init__(self, ActualPinsList, FilePath):
        #On init, parse through pins needed, store in the PinsList.
        #Parse through each stage, save as a testStage class in testStage list.
        self.RealPinsList = ActualPinsList
        self.LoadInTests(FilePath)
        logging.info('Initializing pins list.')

    def LoadInTests(self, FilePath):
        with open(FilePath) as f:
            testData = json.load(f)
            logging.debug(testData)
            logging.debug(testData["name"])
        try:
            self.name = testData["name"]
            
            self.description = testData["description"]
        except:
            print("Error parsing in name or description.")
        
        #Mode pin setting:  0 = input, 1=output.

        for x in testData["pins"]:
            self.TestPinsList.addPin(x["pin"], x["mode"], 0, x["description"])
            logging.debug("Adding pin")
            logging.debug(x["pin"])
        for z in testData["tests"]:
            self.testStages.append(testStage(z["number"], z["description"], z["image"], z["pin_check"], self.RealPinsList))
        
    def getNextTest(self):
        if (self.current_test+1)<len(self.testStages):
            self.current_test +=1
            return self.testStages[self.current_test]
        else:
            return False

    def isNextTest(self):
        return (self.current_test+1)<len(self.testStages)

    #This is facts baby.
    def exportJsonFile(self):
        logging.debug("testPinsList Dict:  ")
        for x in self.TestPinsList.__dict__:
            logging.debug(x)
        logging.debug("done.")
        

        jsonTestStages = []
        for x in self.testStages:
            jsonTestStages.append(x.__dict__)
            
        return json.dumps({'name': self.name, 'description': self.description,
        'pins': self.TestPinsList.__dict__, 'tests': jsonTestStages})
