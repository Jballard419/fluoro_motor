
Filter_changer: main.o  filter.o
	 g++ -Wall  -g main.o  filter.o    -o Filter_changer  -lstepper_bee_interface
test_program:
	g++ -Wall -o test_program test_program.c -L/lib -lstepper_bee_interface

libstepper_bee_interface.so:
	g++ -c -Wall -Werror -fpic stepper_bee_interface.c
	g++ -shared -o libstepper_bee_interface.so stepper_bee_interface.o -lusb-1.0
	sudo cp libstepper_bee_interface.so usr/lib
	sudo /sbin/ldconfig -v

main.o: main.cpp
	g++ -Wall -c main.cpp

filter.o: filter.cpp filter.h
	g++ -Wall -std=c++0x  -c filter.cpp -lstepper_bee_interface
clean:
	rm *.o *~ Filter_changer test_program
