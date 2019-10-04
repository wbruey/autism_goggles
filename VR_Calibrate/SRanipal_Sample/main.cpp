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
#include "SRanipal_Lip.h"
#include "SRanipal_Enums.h"
#include <Windows.h>

#pragma comment (lib, "SRanipal.lib")
using namespace ViveSR;

std::thread *t = nullptr;
bool EnableEye = false;
bool EnableLip = false;
bool looping = false;
bool test_running = true;
unsigned long int trash = 0;
void streaming() {
	ViveSR::anipal::Eye::EyeData eye_data;
	ViveSR::anipal::Lip::LipData lip_data;
    char lip_image[800 * 400];
	lip_data.image = lip_image;

	int result = ViveSR::Error::WORK;
	std::ofstream myfile;
	myfile.open("C:\\Users\\willb\\git_repos\\autism_goggles\\eye_gaze_data_cal.csv");
	unsigned long int gaze_time = 0;
	unsigned int frame_seq = 0;
	unsigned __int64 now = 0;
	unsigned __int64 movie_duration = 23000;  //dot static
	unsigned __int64 start_time = 0;
	start_time = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
	unsigned __int64 time_so_far = 0;
	while (looping) {
		now = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
		time_so_far = now - start_time;

		if (time_so_far > movie_duration) {
			looping = false;
			test_running = false;
			printf("The Eye Tracking Monitoring is Complete");
			//give some time to write to and close file.
			Sleep(2000);
			ViveSR::anipal::Release(ViveSR::anipal::Eye::ANIPAL_TYPE_EYE);
			myfile.close();
			exit(0);
		}

		while (time_so_far > 0 && time_so_far < 500) {
			now = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
			time_so_far = now - start_time;
			printf("time: %d\n", time_so_far);
			
		}

		if (EnableEye) {
			int result = ViveSR::anipal::Eye::GetEyeData(&eye_data);
			if (result == ViveSR::Error::WORK) {
				float* left_gaze = eye_data.verbose_data.left.gaze_direction_normalized.elem_;
				float* right_gaze = eye_data.verbose_data.right.gaze_direction_normalized.elem_;
				float* combined_gaze = eye_data.verbose_data.combined.eye_data.gaze_direction_normalized.elem_;
				float *gaze = eye_data.verbose_data.left.gaze_direction_normalized.elem_;
				frame_seq = eye_data.frame_sequence;
				//printf("[Eye] Gaze: %.2f %.2f %.2f\n", gaze[0], gaze[1], gaze[2]);
				std::ostringstream eye_sample;
				eye_sample << "eye_gaze,"
					<< now
					<< ","
					<< frame_seq
					<< ","
					<< gaze_time
					<< ","
					<< left_gaze[0]
					<< ","
					<< left_gaze[1]
					<< ","
					<< left_gaze[2]
					<< ","
					<< right_gaze[0]
					<< ","
					<< right_gaze[1]
					<< ","
					<< right_gaze[2]
					<< ","
					<< combined_gaze[0]
					<< ","
					<< combined_gaze[1]
					<< ","
					<< combined_gaze[2]
					<< ","
					<< time_so_far
					<< "\n";

				std::string str = eye_sample.str();
				std::cout << str;
				myfile << str;
			}
		}
        if (EnableLip) {
			result = ViveSR::anipal::Lip::GetLipData(&lip_data);
			if (result == ViveSR::Error::WORK) {
				float *weightings = lip_data.prediction_data.blend_shape_weight;
				printf("[Lip] frame: %d, time: %d, weightings %.2f\n", lip_data.frame_sequence, lip_data.timestamp, weightings[0]);
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
    printf("[2] Initial Lip engine\n");
	printf("[3] Launch a thread to query data.\n");
	printf("[4] Stop the thread.\n");
	
	if(!ViveSR::anipal::Eye::IsViveProEye()){
		printf("\n\nthis device does not have eye-tracker, please change your HMD\n");
		return 0;
	}
	char str = 0;
	int error, handle = NULL;
	while (test_running) {
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
        else if (str == '2') {
			error = ViveSR::anipal::Initial(ViveSR::anipal::Lip::ANIPAL_TYPE_LIP, NULL);
			if (error == ViveSR::Error::WORK) { EnableLip = true; printf("Successfully initialize Lip engine.\n"); }
			else if (error == ViveSR::Error::RUNTIME_NOT_FOUND) printf("please follows SRanipal SDK guide to install SR_Runtime first\n");
			else printf("Fail to initialize Lip engine. please refer the code %d of ViveSR::Error.\n", error);
		}
        else if (str == '3') {
			int i = 0;
            if (t == nullptr) {
				i = system("start C:\\ffmpeg\\bin\\ffplay C:\\Users\\willb\\git_repos\\autism_goggles\\dotstaticsmall.mp4 -fs -autoexit");
				printf("start C:\\ffmpeg\\bin\\ffplay C:\\Users\\willb\\git_repos\\autism_goggles\\dotstaticsmall.mp4 -fs -autoexit");
				t = new std::thread(streaming);
                if (t)   looping = true;
            }
        }
        else if (str == '4') {
            looping = false;
            if (t == nullptr) continue;
            t->join();
            delete t;
            t = nullptr;
        }
	}
	ViveSR::anipal::Release(ViveSR::anipal::Eye::ANIPAL_TYPE_EYE);
    ViveSR::anipal::Release(ViveSR::anipal::Lip::ANIPAL_TYPE_LIP);
}