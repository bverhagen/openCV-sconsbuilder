/*
 * =====================================================================================
 *
 *       Filename:  example.cpp
 *
 *    Description:  Example file for building openCV using the scons builder
 *
 *        Version:  1.0
 *        Created:  06/28/2014 09:13:48 PM
 *
 *         Author:  Bart Verhagen (bv), barrie.verhagen@gmail.com
 *
 * =====================================================================================
 */
#include <string>
#include <iostream>
#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"

int main(int argc, char** argv) {
	std::string filename = "duomo.jpg";
	cv::Mat imFrame = cv::imread(filename, cv::IMREAD_GRAYSCALE);

	if(imFrame.rows == 0 || imFrame.cols == 0) {
		std::cerr << "Could not load image '" << filename << "'. Exiting now." << std::endl;
		return EXIT_FAILURE;
	}

	std::cout << "[" << imFrame.cols << " ," << imFrame.rows << "]" << std::endl;

	cv::imwrite("testImage.jpg", imFrame);
	cv::imshow("You need vision", imFrame);
	cv::waitKey(1000);

/*   	const unsigned int videoId = 0U;
	cv::VideoCapture videoCapture;
	videoCapture.open(videoId);
	if(! videoCapture.isOpened()) {
		return EXIT_FAILURE;
	}
	const uint NB_OF_FRAMES_TO_CAPTURE = 90;
	for(uint i = 0; i < NB_OF_FRAMES_TO_CAPTURE; ++i) {
		cv::Mat frame;
		videoCapture.read(frame);
		cv::imshow("Camera input", frame);
		cv::waitKey(30);
	}*/
	return EXIT_SUCCESS;
}
