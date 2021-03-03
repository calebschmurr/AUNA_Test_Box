#class TestSequence - class to hold all information for a testing sequence for the AUNA box.
import PinList
import json

import logging

#Below - enable logging.
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#Below - get rid of all log messages.
#logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

class testPin:
    pin = 0
    check_code = 0
    value = 0
    RealPinsList = None

    EqualValueVariant = 100

    def __init__(self, pin, check_code, value, RealPinsList):
        print("on init testPin number: {}".format(pin))
        self.pin = pin
        self.check_code = check_code
        self.value = value
        self.RealPinsList = RealPinsList

    
    def __getitem__(self, val):
        return getattr(self,val)


    #create method to perform check
    #Pin Check Codes:
    # -1 - invalid/not to do.
    # 0 - less than
    # 1 - greater than
    # 2 - equal to

    def checkPin(self):
        if self.check_code==0:
            return self.RealPinsList.getPinValue(self.pin) < self.value
        elif self.check_code==1:
            return self.RealPinsList.getPinValue(self.pin) > self.value
        elif self.check_code==2:
            return (self.RealPinsList.getPinValue(self.pin) > (self.value - self.EqualValueVariant)) and (self.RealPinsList.getPinValue(self.number) < (self.value + self.EqualValueVariant))

    #create methods to change all values as well.
    def getDict(self):
        #print("testPin getDict number: {}".format(self.pin))
        return {'pin': self.pin, 'check_code': self.check_code,
        'value': self.value, 'RealPinsList': self.RealPinsList}

class testStage:
    number = 0
    description = ""
    image = ""
    error = ""
    testPins = []
    FolderPath = None

    def __init__(self, number, description, image, pin_checks, error, RealPinsList):
        #self.testPins.clear()
        self.testPins=[]
        self.number = number
        self.description = description
        self.image = image
        self.error = error
        self.parsePinChecks(pin_checks, RealPinsList)

    def parsePinChecks(self, pin_checks, RealPinsList):
        for x in pin_checks:
            self.testPins.append(testPin(x['pin'], x['check_code'], x['value'], RealPinsList))
            print("Pin {} saved w/ value {} and code {}".format(x['pin'], x['value'], x['check_code']))

    def getDict(self):
        x = {'number': self.number, 'description': self.description,
        'image': self.image, 'error': self.error}
        x['pin_check'] = []
        for z in self.testPins:
            x['pin_check'].append(z.getDict())
            logging.debug("adding to pin_check:")
            logging.debug(z.getDict())

        logging.debug("Full dictionary:")
        logging.debug(x)
        return x

    #Check each pin to make sure it is passing the required check for stage.
    def passPinCheck(self):

        return True


class TestSequence:
    name = ""
    description = ""
    TestPinsList = PinList.PinsList() #This is the list of pins used in the test.
    testStages = []
    RealPinsList = None #To be defined on init.
    current_test = -1

    def initialLoadIn(self, ActualPinsList, FilePath):
        self.RealPinsList = ActualPinsList
        self.LoadInTests(FilePath)
        logging.info('Initializing pins list.')


    def LoadInTests(self, FilePath):
        with open(FilePath) as f:
            testData = json.load(f)
            logging.debug(testData)
            logging.debug(testData['name'])
        try:
            self.name = testData['name']
            self.description = testData['description']
        except:
            print("Error parsing in name or description.")
        
        #Mode pin setting:  0 = input, 1=output.
        for x in testData['pins']:
            self.TestPinsList.addPin(x['pin'], x['mode'], 0, x['description'])
            #logging.debug("Adding pin")
            #logging.debug(x['pin'])
        for z in testData['tests']:
            self.testStages.append(testStage(z['number'], z['description'], z['image'], z['pin_check'], z['error'], self.RealPinsList))
        
    def getNextTest(self):
        if (self.current_test+1)<len(self.testStages):
            self.current_test +=1
            return self.testStages[self.current_test]
        else:
            return False

    def getCurrentTest(self):
        return self.testStages[self.current_test]

    def isNextTest(self):
        return (self.current_test+1)<len(self.testStages)

    def getNumStages(self):
        return len(self.testStages)-1

    #This is facts baby.
    def exportJsonFile(self):
        output={}
        output['name'] = self.name
        output['description'] = self.description
        output['pins'] = []
        output['tests'] = []
        logging.debug("Here")
        for x in self.TestPinsList.PinList:
            output['pins'].append(x.getDict())
        
        logging.debug("testPinsList Dict:  ")
        for x in self.TestPinsList.PinList:
            #logging.debug(x.getDict())
            pass
        logging.debug("done.")
        
        for x in self.testStages:
            output['tests'].append(x.getDict())

        return json.dumps(output)