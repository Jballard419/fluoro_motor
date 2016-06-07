
extern "C"{

	#include "stepper_bee_interface.h"

}





filter_node::filter_node(int start_node){
  node=start_node;
  distance_to= new int[6][6];
  current_node=start_node;
  int[6] distance_between= [99,99,100,101,101,99]
  distance_to= [
    {0,     99, 198,298,-201, -100 },
    {-99,   0, 99,199,300, -199},
    {-198,-99 , 0,100,201,302},
    {-298,-199, -100, 0, 101, 202},
    {201,-300, -201, -101,0,101},
    {100,199, -302,-202, -101, 0},
   ];





}

filter_node::Move_to(int next_node){

	int steps_to=distance_to[current_node][next_node];
	if(steps_to >=0)
	{
		int dir = 0;
	}
        else
	{
		int dir = 1;
	}
	time_interval=200; 

	int reply = move_motor(int motor_id,  dir, steps_to, time_interval, 0,0,0 );	 	



}

