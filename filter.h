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



    bool Move_to(int next_node); //TODO: add speed option
    int distance_to[6][6];

    void set_node();
    int get_node();


private:
  int current_node; 



};
#endif


