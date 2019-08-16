#include <stdio.h>
#include <ctime>
#include <iostream>
#include <string>
#include <iostream>     // std::cout
#include <sstream>      // std::ostringstream
#include <signal.h>
#include <stdlib.h>
#include <thread>
#include <iostream>
#include <fstream>
#include <chrono>
#include "SRanipal.h"
#include "SRanipal_Eye.h"
#include "SRanipal_Enums.h"

#pragma comment (lib, "SRanipal.lib")
using namespace ViveSR;

std::thread *t = nullptr;
bool EnableEye = false;
bool looping = false;
void streaming() {
	ViveSR::anipal::Eye::EyeData eye_data;
	int result = ViveSR::Error::WORK;
	std::ofstream myfile;
	myfile.open("eye_gaze_data.txt");
	unsigned long int gaze_time = 0;
	unsigned int frame_seq = 0;
	unsigned __int64 now = 0;

	while (looping) {
		if (EnableEye) {
			int result = ViveSR::anipal::Eye::GetEyeData(&eye_data);
			if (result == ViveSR::Error::WORK) {
				float *gaze = eye_data.verbose_data.left.gaze_direction_normalized.elem_;
				gaze_time = eye_data.timestamp;
				frame_seq = eye_data.frame_sequence;
				//printf("[Eye] Gaze: %.2f %.2f %.2f\n", gaze[0], gaze[1], gaze[2]);
				now = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
				std::ostringstream eye_sample;
				
				eye_sample << "eye_gaze,"
					<< now
					<< ","
					<< frame_seq
					<< ","
					<< gaze_time
					<< ","
					<< gaze[0]
					<< ","
					<< gaze[1]
					<< ","
					<< gaze[2]
					<< "\n";

				std::string str = eye_sample.str();
				std::cout << str;
				myfile << str;


			}
		}
	}
	myfile.close();
}

int main() {
	printf("SRanipal Sample\n\nPlease refer the below hotkey list to try apis.\n");
	printf("[`] Exit this program.\n");
	printf("[0] Release all anipal engines.\n");
	printf("[1] Initial Eye engine\n");
	printf("[3] Launch a thread to query data.\n");
	printf("[4] Stop the thread.\n");
	
	if(!ViveSR::anipal::Eye::IsViveProEye()){
		printf("\n\nthis device does not have eye-tracker, please change your HMD\n");
		return 0;
	}
	char str = 0;
	int error, handle = NULL;
	while (true) {
		if (str != '\n' && str != EOF) { printf("\nwait for key event :"); }
		str = getchar();
		if (str == '`') break;
		else if (str == '0') {
			error = ViveSR::anipal::Release(ViveSR::anipal::Eye::ANIPAL_TYPE_EYE);
			printf("Successfully release all anipal engines.\n");
			EnableEye = false;
		}
		else if (str == '1') {
			error = ViveSR::anipal::Initial(ViveSR::anipal::Eye::ANIPAL_TYPE_EYE, NULL);
			if (error == ViveSR::Error::WORK) { EnableEye = true; printf("Successfully initialize Eye engine.\n"); }
			else if (error == ViveSR::Error::RUNTIME_NOT_FOUND) printf("please follows SRanipal SDK guide to install SR_Runtime first\n");
			else printf("Fail to initialize Eye engine. please refer the code %d of ViveSR::Error.\n", error);
		}
		else if (str == '3') {
			int i = 0;
			printf("start C:\\ffmpeg\\bin\\ffplay C:\\ffmpeg\\bin\\snl.avi -fs");
			i = system("start C:\\ffmpeg\\bin\\ffplay C:\\ffmpeg\\bin\\snl.avi -fs");
			looping = true;
			t = new std::thread(streaming);
		}
		else if (str == '4') {
			if (t == nullptr) continue;
			looping = false;
			t->join();
			delete t;
			t = nullptr;
		}
	}
	ViveSR::anipal::Release(ViveSR::anipal::Eye::ANIPAL_TYPE_EYE);
}