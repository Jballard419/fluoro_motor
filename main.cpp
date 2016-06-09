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
			std::cout<<i<<") go to the " << names[i] << " filter \n";		
		}else{

			std::cout<<i<<") go to the " << names[i-1] << " filter \n";
		}
	i++;
	}
	std::cout<< "6) exit \n";
	std::cin>>next_setting;
	while(std::cin.fail()) {
		std::cin.clear();
		std::cin.ignore(std::numeric_limits<int>::max(),'\n');
		std::cout << "Bad entry.  Enter a NUMBER: ";
		std::cin >>next_setting;
	}
	if(next_setting==6){
		
		return;	
	}else if(next_setting>6 || next_setting<1) {
		std::cout << "please enter  a number between 1-6";
		
		
	}else
	{
		if(next_setting <= current_location)
		{
			next_setting=next_setting-1;
		}
		current_location=next_setting;
		rotor->Move_to(current_location);
		
		
	}
	Interface(current_location, names,rotor); 




	
}

//int motor_one_status, motor_two_status, motor_one_steps, motor_two_steps;
	//int reply;
	//reply = init_controller();
	//reply = get_motor_status(&motor_one_status, &motor_two_status, &motor_one_steps, &motor_two_steps);
	//reply = move_motor(1, 0, 200, 1, 0, 0, 0);
int main(){
	
	
int current_location;
std::string names[6] = {"Cu","In","Sn","Ag","node4","node5"};
std::cout<<"select the filter currently aligned \n";
int i=1;
while(i<7){
	std::cout<<" "<<i<<") go to the " << names[i-1] << " filter \n";
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
	
	
}while(current_location<1||current_location>6);

	

filter* rotor = new filter(current_location-1);
Interface(current_location-1, names,rotor); 
delete rotor;

return 0;

}






