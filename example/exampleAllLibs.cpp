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
#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"

int main(int argc, char** argv) {
	const unsigned int videoId = 0U;
	cv::VideoCapture videoCapture;
	videoCapture.open(videoId);
	if(! videoCapture.isOpened()) {
		return EXIT_FAILURE;
	}
	while(true) {
		cv::Mat frame;
		videoCapture.read(frame);
		cv::imshow("Camera input", frame);
		cv::waitKey(30);
	}
	return EXIT_SUCCESS;
}
