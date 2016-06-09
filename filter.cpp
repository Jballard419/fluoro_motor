#include "stepper_bee_interface.h"
#include "filter.h"
#include <iostream>
#include <stdlib.h>        
#include <chrono>         





filter::filter(int start_node){
 
 
  current_node=start_node;
  
  distance_to ={
    {0,     99, 198,298,-201, -100 },
    {-99,   0, 99,199,300, -199},
    {-198,-99 , 0,100,201,302},
    {-298,-199, -100, 0, 101, 202},
    {201,-300, -201, -101,0,101},
    {100,199, -302,-202, -101, 0},
   };
	//int reply;
	//reply = init_controller();
for(int i=0; i<6; i++){
	for(int j=0; j<6; j++){
		std::cout<<distance_to[i][j]<< " ";	
	}
	std::cout<<" \n";

}


}

bool filter::Move_to(int next_node){
	
	int motor_one_status, motor_two_status, motor_one_steps, motor_two_steps;
	int dir = 1;
	std::cout<<current_node<<" " << next_node<< std::endl;
	int steps_to=distance_to[current_node][next_node];
	
	if(steps_to <=0)
	{
		 dir = 0;
		 steps_to= -1*steps_to;
	}
        
	std::cout<<steps_to<<" " << distance_to[current_node][next_node]<< std::endl;
	int time_interval=10; 

		//int motor_one_status, motor_two_status, motor_one_steps, motor_two_steps;
	int reply;

	reply = init_controller();
	reply = set_modes(1,1,1,1);
	
	reply = move_motor(1, dir, steps_to, time_interval, 0, 0, 0);
	
	
	int j=0; //built in for the delay that will occur on the usb
	
	do{
		//std::cin.ignore();
		reply = get_motor_status(&motor_one_status, &motor_two_status, &motor_one_steps, &motor_two_steps) ;
		std::cout<<"MOTOR - steps left = "<< motor_two_steps<< " \n";	
		j++;
	}while(motor_one_status == 1 || motor_two_status == 1|| j<5);
	std::cout<<"DONE !! \n";	
	current_node=next_node;
	reply=close_controller();
	/*for(int i=0; i<6; i++){
	for(int j=0; j<6; j++){
		std::cout<<distance_to[i][j]<< " ";	
	}
	std::cout<<" \n";
	*/

//}
	
		
	return true;


}

