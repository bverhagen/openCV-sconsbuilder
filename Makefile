get3rdparty:
	./getOpenCv.sh

example: get3rdparty
	scons -C example --jobs 8 example

example-linux: get3rdparty
	scons -C example --jobs 8 target=linux example

example-linux-single-threaded: get3rdparty
	scons -C example --jobs 1 target=linux example

example-mac: get3rdparty
	scons -C example --jobs 8 target=macosx example

buildAllLibsWithExample: get3rdparty
	scons -C example --jobs 8 buildAllLibsWithExample

buildAllLibsWithExample-linux: get3rdparty
	scons -C example --jobs 8 target=linux buildAllLibsWithExample

buildAllLibsWithExample-linux-single-threaded: get3rdparty
	scons -C example --jobs 1 target=linux buildAllLibsWithExample

buildAllLibsWithExample-macosx: get3rdparty
	scons -C example --jobs 8 target=macosx buildAllLibsWithExample

buildAllLibs: get3rdparty
	scons -C example --jobs 8 buildAllLibs

buildAllLibs-linux: get3rdparty
	scons -C example --jobs 8 target=linux buildAllLibs

buildAllLibs-macosx: get3rdparty
	scons -C example --jobs 8 target=macosx buildAllLibs

