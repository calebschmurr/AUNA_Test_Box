//Pin List file

//Define output and input mode variables for system
#define OUTPUT 0
#define INPUT 1


struct pin{
	int pin_number;
	char mode; //smallest data type is char.
	//struct pin *next;
}

struct pin *head = NULL;//Make head the top of the list and end of the list.
struct pin *current = NULL;
/*
int add_pin(int new_pin_number, char new_mode){
	struct pin *link = (struct node*) malloc(sizeof(struct node));
	link->pin_number = new_pin_number;
	link->mode = new_mode;
	link->next = NULL;
	if(head==NULL){
		head=link;
		head->next = link;
		return 0;
	}
	current = head;
	while(current->next != head){
		current = current->next;
	}
	current->next = link;
	link->next = head;

	return 0;
}
*/

int add_pin(int activePinsListSize, struct pin* pinsList, int new_pin_number, char new_mode){
	activePinsListSize++;
	
	pinsList[activePinsListSize] = {new_pin_number,new_mode};
	
	
}
int clear_pins(){
	//Clear the pins list.
	//Traverse list, free pins.
	struct pin *delptr = NULL;
	current = head;
	while(current->next != head){
		delptr = current;
		current = current->next;
		free(delptr->pin_number);
		free(delptr->mode);
		free(delptr);
	}
	free(head->pin_number);
	free(head->mode);
	free(head);
}



