//PinList c manager
#include "PinsList.h"
#include "stdio.h"
#include "string.h"

void PinsList::add_pin(int pin_number, char pin_mode){
	activePinsListValues[active_pin_list_size] = {pin_number, pin_mode};
	active_pin_list_size++;
}

void PinsList::clear_pin_list(){
	active_pin_list_size = 0;
	memset(activePinsListValues, 0, sizeof activePinsListValues);
}

int PinsList::getPinNumber(int list_location){
	return activePinsListValues[list_location].pin_number;
}

int PinsList::getPinIndex(int pin_number){
  int i = 0;
  for (i = 0; i<active_pin_list_size; i++){
    if(pin_number == getPinNumber(i)){
      return i;
    }
  }
  return -1;
}

bool PinsList::getIfOutputPinNumber(int pin_number){
	int i = 0;
	for (i = 0; i<active_pin_list_size; i++){
		if(pin_number==getPinNumber(i)){
			if(getPinMode(i)=='O'){
				return true;
			}
		}
	}
	return false;
}

char PinsList::getPinMode(int list_location){
	return activePinsListValues[list_location].mode;
}

int PinsList::getNumberActivePins(){
	return active_pin_list_size;
}

void PinsList::listPins(){

	printf("Listing Pins:\n");
	for (int i = 0; i<active_pin_list_size; i++){
		printf("Pin ");
		printf("%d ", getPinNumber(i));
		printf(" is status ");
		printf("%c \n", getPinMode(i));
	}
	printf("Pins Listed.\n");
  
}

bool PinsList::getIfInputPin(int list_location){
	if (activePinsListValues[list_location].mode==PinAnalogInput || activePinsListValues[list_location].mode==PinDigitalInput){
		return true;
	}
	return false;
}

bool PinsList::getIfOutputPin(int list_location){
	if (activePinsListValues[list_location].mode==PinOutput){
		return true;
	}
	return false;
}
