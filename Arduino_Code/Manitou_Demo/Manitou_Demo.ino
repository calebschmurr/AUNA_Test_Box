
#include "PinsList.h"
#include <VariableTimedAction.h>
#include <math.h>

//Declare input array of size 200;
char inputArrayVal[200];
char * inputArray = inputArrayVal;
char swCase;
char cin;
int availableBytes;

int i = 0;

int Debug = 1;
unsigned loc;
int output_mode;
int outputTime;


//1:23.I;24.I;25.I;26.I;27.I;28.O;!
PinsList pin_list;


/*
 * PinValSender - this is what is used to send back
 * a signal that contains the registered pins info.
 * 
 */
class PinValSender : public VariableTimedAction {

  private:

  /*
   * Format for sending back data:
   * #1;01:2.2;02:3.2;05:1.2;07:1.8;
   * 
   * Format:
   * [#1];[pin_number]:[value];[pin_number]:[value];[pin_number]:[value];
   * Initialize command with #1
   * pin_number - the pin_number to return.
   * value - the value of the pin to return.
   * 
   */
  
  unsigned long run(){
    //Run the code in here:

    //TODO: Translate the Analog Input pins to use 8 instead of A as variable name
    //for passing back and forth.

    //Also TODO: For parsing input values of pins, change the size of the input to be 3 chars.
    //Initialize the send-back code:
    Serial.print("#1;");
    for(i = 0; i<pin_list.getNumberActivePins(); i++){
      //Check to see what type of pin it is: output or input.
      if(pin_list.getIfInputPin(i)){
        //If pin is input, then print the value to Serial.
       if(pin_list.getPinNumber(i)<10){
          Serial.print("0");
          Serial.print(pin_list.getPinNumber(i));
        }else{
          Serial.print(pin_list.getPinNumber(i));
        }
        Serial.print(":");
        if(pin_list.getPinMode(i)==PinAnalogInput){
          Serial.print(analogRead(pin_list.getPinNumber(i)));
          Serial.print(",");
        }else if (pin_list.getPinMode(i)==PinDigitalInput){
          Serial.print(digitalRead(pin_list.getPinNumber(i)));
          Serial.print(",");
        }
      }
    }
    Serial.print("!\n");
    return 0;
  }
public:
  
  
};

PinValSender PinValueSender;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(500);
  Serial.println("Open.\n");
  while(!Serial){
    
  }
  Serial.println("Open2.\n");
}


void loop() {
  // put your main code here, to run repeatedly:
  i = 0;
  while(Serial.available()>0){
    if(Serial.peek() != 10){

      inputArray[i] = Serial.read();
      inputArray[i+1] = '\0';
      i++;
    }else{
       Serial.read();
     }
     delay(10);
  }
    configureSetup();
    VariableTimedAction::updateActions();
    delay(10);
}


/*
 * sendPinItems()
 * Method to return the values found in pinlist: 
 */

/*
 * configureSetup() method
 * Used to receive inputs from Serial communication
 * 
 */
int configureSetup(){
      if(inputArray[0]){
        Serial.print("input var:");
        Serial.println(inputArray);

   if(inputArray[0]=='0'){
      //Reset - clear active pins, clear pin list, etc.
       if(Debug){
          Serial.println("Reset called.");
         }
      
    pin_list.clear_pin_list();
      delay(10);
      
    } else if(inputArray[0]=='1'){
      if(Debug){
        Serial.println("Setup Pins command called.");
        Serial.println(inputArray);
      }
      //parse the input until reached end of command.
      loc = 2; //declare location
      char pin_num[4]; //holder for pin value
      char pin_type[3]; //holder for the pin type.
      unsigned pinTypeLen = 0;
      unsigned u_pin_num = 0;
      pin_num[3] = '\0';
      i = 0;
      
      //While the input is not terminating parse input:
      while(inputArray[loc]!='!'){
        //Start off getting the pin number:
        pin_num[0] = inputArray[loc];
        pin_num[1] = inputArray[loc+1];
        pin_num[2] = inputArray[loc+2];  
        loc+=4;
        u_pin_num = atoi(pin_num);
        
        if(Debug){
          Serial.print("Pin_num: ");
          Serial.println(pin_num);
        }
        //Get the length of the pin type parameters
        pinTypeLen = 0;
        while(inputArray[loc]!=';'){
          loc++;
          pinTypeLen++;
        }
        if(Debug){
          Serial.print("PinTypeLen: ");
          Serial.println(pinTypeLen);
        }
        
        //Store the pin type.
        for(i = 1; i<pinTypeLen+1; i++){
          pin_type[pinTypeLen-i] = inputArray[loc-i];
        }
        if(Debug){
          Serial.print("Pin_Type: ");
          Serial.println(pin_type);
        }
        //PinMode assignment based on pin_type
        if(pin_type[0]=='I'){
            //Check to see if digital or analog:

          if(u_pin_num>=54 && u_pin_num<=69){
            pinMode(u_pin_num,INPUT_PULLUP);
            pin_list.add_pin(u_pin_num,PinAnalogInput);
            if(Debug){
              Serial.print("Pin ");
              Serial.print(u_pin_num);
              Serial.print(" is set to Analog Input.\n");
            }
          }else{
            pinMode(u_pin_num,INPUT_PULLUP);
            pin_list.add_pin(u_pin_num,PinDigitalInput);
            if(Debug){
              Serial.print("Pin ");
              Serial.print(u_pin_num);
              Serial.print(" is set to Digital Input.\n");
            }
          }

        }else if (pin_type[0] == 'O'){
              pinMode(u_pin_num,OUTPUT);
             // add_pin(&activePinsListSize, activePinsList, atoi(pin_num),0);
              pin_list.add_pin(u_pin_num,PinOutput);
            if(Debug){
              Serial.print("Pin ");
              Serial.print(u_pin_num);
              Serial.print(" is set to Output.\n");
              }
        }else {
          //ERROR CASE
          Serial.println("Error - improper values given.");
          break;
        }
        //Reset information:
        memset(pin_num, 0, sizeof pin_num);
        memset(pin_type, 0, sizeof pin_type);
       loc++;
      }

    /*
     * List pins
     * 
     * 
     */

  Serial.print("Listing Pins:\n");
  for (int i = 0; i<pin_list.active_pin_list_size; i++){
    Serial.print("Pin ");
    Serial.print(pin_list.getPinNumber(i));
    Serial.print(" is status ");
    Serial.println(pin_list.getPinMode(i));
  }
  Serial.println("Pins Listed.");
  

//Finish listing pins.
      
  }else if(inputArray[0]=='2'){
   //Setup output Command:
    //2:1.4500!
    if(Debug){
        Serial.println("Setup Output Called");
        Serial.println(inputArray);
    }
    loc=2;
    unsigned sizeofTime = 0;
    char inputChar[1];

    //Need output mode, time for output.
    inputChar[0] = inputArray[loc];
    delay(1);
    //Serial.println(inputChar);
    //Serial.println(atoi(inputChar));
     output_mode = atoi(inputChar);
     delay(5);
     loc=4; //loc=4
     while(inputArray[loc]!='!'){
          loc++;
          sizeofTime++;
          if(loc>1200){
            Serial.println("Error - command too long.");
            break;
          }
     }
     for(i = 1; i<sizeofTime+1; i++){
      if(Debug){
        Serial.println(inputArray[loc-i]);
      }
        inputChar[0] = inputArray[loc-i];
        delay(2);
        outputTime += (atoi(inputChar) * pow(10,i-1))+1; //For some reason, have to include +1 on the operation, otherwise time var does not update properly.
        delay(1);
        if(Debug){
          Serial.print("pow: ");
          Serial.println(pow(10,i-1));
          Serial.println(outputTime);
          Serial.println("restart_loop");
        }
     }
     if(output_mode){
      PinValueSender.start(outputTime);
     }else{
      PinValueSender.stop();
     }
     
     if(1){
        Serial.print("Output Mode: ");
        Serial.print(output_mode);
        Serial.print(", and output time: ");
        Serial.println(outputTime);
     }

    //COMMAND 3 //Configure the output of pins////////////////////////////////////
    //3:02.0,13.4!
    //Send command as follows:
/* [3]:[00].[001],[00],[255]!
 * [3]:[pin].[value from 0-255],[pin].[value from 0-255]!
 * When configuring the output, choose a value from 0-255 for PWM,
 * or 0 or 255 for digital output pins.
 * 
 */

   } else if(inputArray[0]=='3'){
      //Control output variables - determine which ones should be output.
      Serial.println("Case 3");
      Serial.println("Configure output value of a pin.");

      loc = 2; //declare location
      unsigned pinTypeLen = 0;
      char pin_num[3] = {'0', '0', '\0'}; //holder for pin value
      char pin_value[4] = {'0', '0', '0', '\0'}; //holder for the pin type.
      int new_pin_num = 0;
      int new_pin_val = 0;
      i = 0;
      
      //While the input is not terminating parse input:
      while(inputArray[loc]!='!'){
        //Start off getting the pin number:
        pin_num[0] = inputArray[loc];
        pin_num[1] = inputArray[loc+1];  
        pin_value[0] = inputArray[loc+3];
        pin_value[1] = inputArray[loc+4];
        pin_value[2] = inputArray[loc+5];
        loc+=7;
        new_pin_num = atoi(pin_num);
        new_pin_val = atoi(pin_value);
        //Determine if the pin selected is a valid output pin.
        
        //cycle through active pins.           
          if(pin_list.getPinIndex(new_pin_num)!=-1){
             //Pin is a valid output pin.
             if(new_pin_num>1&&new_pin_num<14){
               //New pin is PWM
               analogWrite(new_pin_num, new_pin_val);
               
             } else if (new_pin_num>21&&new_pin_num<70){
              //New pin is standard GPIO
              Serial.println(new_pin_val);
                if(new_pin_val>0){
                  digitalWrite(new_pin_num, HIGH);
                  Serial.println("Pin ");
                  Serial.println(new_pin_num);
                  Serial.println("Set to HIGH");
                }else{
                  digitalWrite(new_pin_num, LOW);
                  Serial.println("Pin ");
                  Serial.println(new_pin_num);
                  Serial.println("Set to LOW");
                }
                
             } else {
              Serial.print("Pin ");
              Serial.print(new_pin_num);
              Serial.println(" is not a valid GPIO/PWM pin.");
             }
          }else{
            Serial.print("Pin ");
            Serial.print(new_pin_num);
            Serial.println(" is not an initiated output pin.");
          }
        }
    } else {
    Serial.println("Command not recognized.");
  }
 }
    //Clear the values of input.
  memset(inputArray, 0, sizeof inputArray);
  delay(10); //add in update delay.
}
