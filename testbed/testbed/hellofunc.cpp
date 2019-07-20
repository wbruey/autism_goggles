#include <stdio.h>
#include <iostream>
#include "hellohead.h"
#include <string>
#include <iostream>     // std::cout
#include <sstream>      // std::ostringstream

void myPrintHelloWorld(void) {

	printf("Hello bruester!\n");
	std::cout << "Hello, World!\n";


	std::ostringstream eye_sample;
	float x = 3.123;
	float y = 1.234;
	float z = 2.131;
	eye_sample << "eye_gaze,"
		<< x
		<< ","
		<< y
		<< ","
		<< z
		<< "\n";


	std::string str = eye_sample.str();
	std::cout << str;
	
	return;
}