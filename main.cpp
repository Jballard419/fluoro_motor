#include <iostream>
#include <stdio.h>
#include <stdint.h>
#include <math.h>
#include <string>
#include <limits>
#include "stepper_bee_interface.h"
#include "filter.h"



void Interface(int current_location, std::string names[],filter* rotor)
{
	int next_setting;
	int i=1;
	while(i<6)
	{

		 if(i-1>=current_location) {
			std::cout<<i<<") go to the " << names[i] << " filter \n"; // used to show avaible nodes to move to
		}else{

			std::cout<<i<<") go to the " << names[i-1] << " filter \n"; // only shows options of where the node isn't

		}
	i++;
	}
	std::cout<< "6) exit \n";
	std::cin>>next_setting;
	while(std::cin.fail()) { // this code is here to protect the program from crashing if the user inputs a character by mistake
		std::cin.clear();
		std::cin.ignore(std::numeric_limits<int>::max(),'\n');
		std::cout << "Bad entry.  Enter a NUMBER: ";
		std::cin >>next_setting;
	}
	if(next_setting==6){

		return;
	}else if(next_setting>6 || next_setting<1) {
		std::cout << "please enter  a number between 1-6";
		std::cin>>next_setting;
		while(std::cin.fail()) { // this code is here to protect the program from crashing if the user inputs a character by mistake
			std::cin.clear();
			std::cin.ignore(std::numeric_limits<int>::max(),'\n');
			std::cout << "Bad entry.  Enter a NUMBER: ";
			std::cin >>next_setting;
		}

	}else
	{
		if(next_setting <= current_location)
		{
			next_setting=next_setting-1;
		}
		current_location=next_setting;
		rotor->Move_to(current_location); //swivel Activate


	}

}


int main(){


int current_location;
std::string names[6] = {"Cu","In","Sn","Ag","node4","node5"}; // if you have to change an element of an node change thiis line
std::cout<<"select the filter currently aligned \n";
int i=1;
while(i<7){
	std::cout<<" "<<i<<") go to the " << names[i-1] << " filter \n"; //print the list of numbers
	i++;
}
do{
	std::cout<<"Please be sure to enter a number between 1-6 \n";
	std::cin>>current_location;
	while(std::cin.fail()) {
			std::cin.clear();
			std::cin.ignore(std::numeric_limits<int>::max(),'\n');
			std::cout << "Bad entry.  Enter a NUMBER: ";
			std::cin >>current_location;
		}


}while(current_location<1||current_location>6); // there is probably a more clever way to do this
//make sure an int between 1 and 6 is found



filter* rotor = new filter(current_location-1);  // minus one to help user with index
Interface(current_location-1, names,rotor); // the menu
delete rotor; // prevents memory leaks

return 0;

}
