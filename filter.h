/*
* Name=Jamey Ballard
* file filter.h
* header to the filter class
*/

#ifndef FILTER_NODE_H
#define FILTER_NODE_H

class filter_node

{
public:
    //In:
    //Out: a filter object starting at the desired node
    // Called: when starting the program
    filter_node(int start_node);



    bool Move_to(int next_node); //TODO: add speed option
    int[][] distance_to;

    void set_node();
    int get_node();


private:
  int current_node; 



}

#endif
