#Test json of 214-OS1-1501

#Test program - build up a demo using the 214-OS1-1501
#This will set the format for the JSON saving.

import json

x = {
    "name": "214-OS1-1501 Control Panel Jumper",
    "description": [{"param1": "Example Value/Parameter"}],
    #Mode pin setting:  0 = input, 1=output.
    "pins": [{"pin": 54, "mode":0, "description": "BlowerStep1"},
     {"pin": 55, "mode":0, "description": "BlowerStep2"},
     {"pin": 56, "mode":0, "description": "BlowerStep3"},
     {"pin": 57, "mode":0, "description": "AC Signal"},
     {"pin": 58, "mode":0, "description": "Air Flap Sig1"},
     {"pin": 59, "mode":0, "description": "Air Flap Sig2"},
     {"pin": 60, "mode":0, "description": "Air Flap Sig3"},
     {"pin": 61, "mode":0, "description": "WV Poti Sig"}],

    #Pin Check Codes:
    # -1 - invalid/not to do.
    # 0 - less than
    # 1 - greater than
    # 2 - equal to

    #Pin Output Setting Code:

    #Since all these pins are analog pins, the 'Off' is going to be Less than 600,
    #On will be greater than 600.

    #Also, the initial test condition, 0, will set the 'default' condition.  
    #All other changes to the pin statuses will be modifications starting from the
    #'default condition.

    "tests" : [{"number": 0, "description":"Starting", "image":"/img0.jpg",
    "pin_check": [{"pin" : 54, "check_code": 0, "value": 600},
    {"pin" : 55, "check_code": 0, "value": 600},
    {"pin" : 56, "check_code": 0, "value": 600},
    {"pin" : 57, "check_code": 0, "value": 600},
    {"pin" : 58, "check_code": 0, "value": 600},
    {"pin" : 59, "check_code": 0, "value": 600},
    {"pin" : 60, "check_code": 0, "value": 600},
    {"pin" : 61, "check_code": 0, "value": 600},
    ],
    "error": "Error at Stage 0 - Initialization.  No changes, default state."},
    
    {"number": 1, "description": "Speed1", "image":"/img1.jpg",
    "pin_check": [{"pin":54, "check_code":1, "value":600}],
    "error": "Error at Stage 1 - Blower Speed to 1."},
    
    {"number": 2, "description": "Speed2", "image":"/img2.jpg",
    "pin_check": [{"pin":54, "check_code":0, "value":600}, 
        {"pin":55,"check_code":1, "value":600}],
    "error": "Error at Stage 2 - Blower Speed to 2."},
    
    {"number": 3, "description": "Speed3", "image":"/img3.jpg",
    "pin_check": [{"pin":55, "check_code":0, "value":600}, 
        {"pin":56,"check_code":1, "value":600}],
    "error": "Error at Stage 3 - Blower Speed to 3."},
    

    #Test 4 - checking poti value for coldest poti setting.
    {"number": 4, "description": "WV_Poti", "image":"/img4.jpg",
    "pin_check": [{"pin":56, "check_code":0, "value":600}, 
        {"pin":61,"check_code":0, "value":400}],
    "error": "Error at Stage 4 - Poti to coldest."},    

    {"number": 5, "description": "WV_Poti_Hot", "image":"/img5.jpg",
    "pin_check": [ {"pin":61,"check_code":1, "value":900}],
    "error": "Error at Stage 5 - Poti to hottest."},

    {"number": 6, "description": "Louver_Head", "image":"/img6.jpg",
    "pin_check": [ {"pin":58,"check_code":1, "value":600}],
    "error": "Error at Stage 6 - Louvers to Head pos."},
    
    {"number": 7, "description": "Louver_Defrost", "image":"/img7.jpg",
    "pin_check": [{"pin":58, "check_code":0, "value":600}, 
        {"pin":59,"check_code":1, "value":600}],
    "error": "Error at Stage 7 - Louver move to Defrost position."},

    {"number": 8, "description": "Louver_Defrost_Foot", "image":"/img8.jpg",
    "pin_check": [{"pin":59, "check_code":0, "value":600}, 
        {"pin":60,"check_code":1, "value":600}],
    "error": "Error at Stage 8 - Louver move to Defrost & Foot Position position."},

    {"number": 9, "description": "AC_SW", "image":"/img9.jpg",
    "pin_check": [{"pin":60, "check_code":0, "value":600}, 
        {"pin":54,"check_code":1, "value":600},
        {"pin":57,"check_code":1, "value":600}],
    "error": "Error at Stage 8 - Louver move to Defrost position."},
    ]
}

y = json.dumps(x)
print(y)

with open('Test1.txt', 'w') as outfile:
    json.dump(x, outfile)