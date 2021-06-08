//HeaderFile - PinList manager

#define PinOutput 0
#define PinDigitalInput 1
#define PinAnalogInput 2

class PinsList {

private:


struct pin{
	int pin_number;
	char mode; //smallest data type is char.
	//struct pin *next;
};

  const static int num_of_pins = 80;

public:

	pin activePinsListValues[num_of_pins];
  int active_pin_list_size = 0;

  //Declare static vars:

	/*
	Add a pin to the list.
	
	*/
	void add_pin(int pin_number, char pin_mode);
	
	/*
	Clear all pins from pin list
	
	*/
	void clear_pin_list();
	/*
	return the pin number at this location in the pin array
	*/
	int getPinNumber(int list_location);

/*
 * Return the pin location in array of this pin number
 */

  int getPinIndex(int pin_number);
	/*
	Return the pin mode at this location in the pin array
	*/
  
	char getPinMode(int list_location);
	
	int getNumberActivePins();
	
	bool getIfInputPin(int pin_number);

	bool getIfOutputPin(int pin_number);

	bool getIfOutputPinNumber(int pin_number);

	void listPins();
};
