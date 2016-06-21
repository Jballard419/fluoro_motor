/*
* Name=Jamey Ballard
* file filter.h
* header to the filter class
*/
#ifndef FILTER_H
#define FILTER_H



class filter
{
public:
    //In:
    //Out: a filter object starting at the desired node
    // Called: when starting the program
    filter(int start_node);
    //In: the next location of
    //Out: the swivel moves
    // Called: when starting the program
    bool Move_to(int next_node); //TODO: add speed option
    int distance_to[6][6]; // the array that stores the tick differnce




private:
  int current_node; //allows use to know where swivel is at making interface smooth



};
#endif
