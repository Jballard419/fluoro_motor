#include "stepper_bee_interface.h"
#include "filter.h"
#include <iostream>
#include <stdlib.h>
#include <chrono>





filter::filter(int start_node){


  current_node=start_node; //sets the node that is the starting postion

  distance_to ={ //this array is the measurement between the different nodes that I measured
    {0,     99, 198,298,-201, -100 },
    {-99,   0, 99,199,300, -199},
    {-198,-99 , 0,100,201,302},
    {-298,-199, -100, 0, 101, 202},
    {201,-300, -201, -101,0,101},
    {100,199, -302,-202, -101, 0},
   };
	//int reply;
	//reply = init_controller();
// for(int i=0; i<6; i++){
// 	for(int j=0; j<6; j++){
// 		std::cout<<distance_to[i][j]<< " ";
// 	}
// 	std::cout<<" \n";
//
// }


}

bool filter::Move_to(int next_node){

	int motor_one_status, motor_two_status, motor_one_steps, motor_two_steps;
	int dir = 1;

	int steps_to=distance_to[current_node][next_node]; //

	if(steps_to <=0) // checks the direction
	{
		 dir = 0;
		 steps_to= -1*steps_to;
	}

	std::cout<<steps_to<<" " << distance_to[current_node][next_node]<< std::endl;
	int time_interval=10; // time interval between ticks  the motor 10 ms


	int reply; //used to call  methods from stepper_bee_interface

	reply = init_controller(); // turns the board
	reply = set_modes(1,1,1,1); // allows the board to report back to use

	reply = move_motor(1, dir, steps_to, time_interval, 0, 0, 0); // moves motor stepper_bee_interface just change the first int from a  1 to a 0


	int wait=0; //built in for the delay that will occur on the usb

	do{

		reply = get_motor_status(&motor_one_status, &motor_two_status, &motor_one_steps, &motor_two_steps) ;
		std::cout<<"MOTOR - steps left = "<< motor_two_steps<< " \n"; //CTM: change to motor_one_steps if using other motor
		j++;
	}while(motor_one_status == 1 || motor_two_status == 1|| wait<5); //this how we wait for the motor
	std::cout<<"DONE !! \n";
	current_node=next_node; // so the class knows where it is at 
	reply=close_controller();  //prevent bad signals being sent to the motor



	return true;


}
