#class TestSequence - class to hold all information for a testing sequence for the AUNA box.
import PinList
import json

from pathlib import Path


import logging

#Below - enable logging.
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#Below - get rid of all log messages.
#logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')


class testStage:
    number = 0
    description = ""
    image = ""
    error = ""
    testPins = []
    FolderPath = None

    def __init__(self, number, description, image, pin_checks, error):
        #self.testPins.clear()
        self.testPins = pin_checks
        self.number = number
        self.description = description
        self.image = image
        self.error = error


    def getPinExpectedValue(self, number):
        for x in self.testPins:
            if x.pin == number:
                return x.expected_value

    def getDict(self):
        x = {'number': self.number, 'description': self.description,
        'image': self.image, 'error': self.error}
        x['pin_check'] = self.testPins
 
        logging.debug("Full dictionary:")
        logging.debug(x)
        return x

    #Check each pin to make sure it is passing the required check for stage.
    def passPinCheck(self):
        for z in self.testPins:
            if not z.checkPin():
                print("Error: Pin {} did not pass check.  Code: {}, Value: {}".format(z.pin, z.check_code, z.value))
                return False
        return True


class TestSequence:


    def __init__(self, name = "", description = ""):
        self.name = name
        self.description = description
        self.testStages = []
        self.RealPinsList = None
        self.current_test = 0
        self.folderPath = Path('.')
        self.folderPath = self.folderPath / "Tests" / self.name

    def initialLoadIn(self, FilePath, MasterPinList):
        if not self.LoadInTests(FilePath, MasterPinList):
            return False
        logging.info('Initializing pins list.')
        
        return True


    def LoadInTests(self, FilePath, MasterPinList):
        with open(FilePath) as f:
            testData = json.load(f)
            logging.debug(testData)
            logging.debug(testData['name'])
        try:
            self.name = testData['name']
            self.description = testData['description']
        except:
            print("Error parsing in name or description.")
            return False
        
        #Reset TestPinsList, and testStages
        self.testStages.clear()
        MasterPinList.clearList()
        
        #Mode pin setting:  0 = do nothing, 1 = input, 2 = output.
     #   try:
        for x in testData['pins']:
            logging.debug("Found testData['pins']")
            #If the pin is between 54 and 65, add as an input.
            #Otherwise, add as an output.
            if (int(x['pin']) > 53) and (int(x['pin']) < 66):
                MasterPinList.addPin(int(x['pin']), 1, 0, x['description'])
            else:
                MasterPinList.addPin(int(x['pin']), 2, 0, x['description'])
            
        for z in testData['tests']:
            logging.debug("Found testData['tests']")  #todo:  Fix the pin_check parsing, change to load in the individual pins as pin
            self.testStages.append(testStage(int(z['number']), z['description'], z['image'], PinList.getPinsFromDict(z['pin_check']), z['error']))
#    except:
 #           print("Error parsing in test pins and adding to test stages.")
 #           return False    
        return True
        
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

    def exportJsonFile(self, pinDict):
        output={}
        output['name'] = self.name
        output['description'] = self.description
        output['pins'] = []
        output['tests'] = []
        logging.debug("Here")
        output['pins'] = pinDict
        
        
        for x in self.testStages:
            output['tests'].append(x.getDict())
            print(x.getDict())
        print("Done - testStages Append")

        return json.dumps(output)