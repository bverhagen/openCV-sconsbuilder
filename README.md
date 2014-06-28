openCV-sconsbuilder
===================

OpenCV builder for use in Scons build systems. Using scons integration in an existing scons build system allows for building only the required opencv libraries, without having to build the entire system. 

The scons builder does not support configuration of the necessary openCV build options, but relies on the user to set these correctly, including the paths where the required (compatible) libraries can be found. This requires much more knowledge of the user about the openCV build options, but makes cross-compilation much more easy and enables more dynamic builds of opencv for different targets.

Features
--------

Build system building openCV using its source files. For an overview of the currently supported options, you can check 'opencvBuilder/opencv\_config.py'. Feature requests can be made to the author (barrie.verhagen@gmail.com) or tis Github page.

This scons builder supports VariantDir builds, but object files of the opencv source files are at the moment nevertheless build in their own directory. All other files will be built in the variant dir. Header files and libraries will also be placed in their defined folders (see 'Configuring SConstruct and SConscript'). This should be fixed in the future.

Requirements
------------

- git for downloading compatible openCV source files
- scons
- cmake

Installation
------------

1) Clone the openCV-sconsbuilder:
	git clone git@github.com:bverhagen/openCV-sconsbuilder.git

2) Run getOpenCv.sh:
	./getOpenCv.sh

3) Make a softlink from the site\_tools/site\_tools directory of your scons build system to the opencvBuilder directory:
	ln -s <path to opencvBuilder directory> openCvBuilder

4) Configure your SConstruct and SConscript files as described in the chapter 'Configuring SConstruct and SConscript'

Configuring SConstruct and SConscript
-------------------------------------

1) Set the following environment variables:
- openCV\_DIR: absolute path to the downloaded opencv dir
- OPENCVBUILDER\_INCLUDE\_DIR: path to the folder where all opencv includes for your application should be placed.
- OPENCVBUILDER\_LIBS\_DIR: path to the folder where all opencv libraries should be placed for your application to find them.
- opencv\_config: Dictionary of openCV build options that should be set. Default all boolean options are set to False. Check example/opencv/Sconscript for an example. Check site\_scons/site\_tools/openCVBuilder/opencv\_config.py for the entire list of options.
- OPENCVBUILDER\_INCLUDE\_PATHS: list of directories that contain include files and libraries that are not within your path. Usefull for cross-compilation. If all include files and libraries are within your file, define an empty list for this variable.
- OPENCVBUILDER\_MODULE\_DIR: path to the 'modules' dir in the downloaded opencv source file directory after it has been downloaded using 'getOpenCv.sh'.
- OPENCVBUILDER\_3RDPARTY\_DIR: path to the '3rdparty' dir in the downloaded opencv source file directory after it has been downloaded using 'getOpenCv.sh'
 
2) Add 'opencvBuilder' to the environment tools
3) Call the SConscript file in the root of this repo.

Check the SConstruct and SConscript files in the examples directory for an example.

The example
-----------
In the example dir you find an example program that is build using the openCV sconsbuilder. It will capture the video from a capture device (e.g. your webcam) and shows it on the screen.

To build the example:
1) run getOpenCv.sh:
	./getOpenCv.sh
2) Go to the example dir and build the project:
	scons example target=<target>
		where <target> is (depending on your system):
			linux (default)
			macosx
3) Run the example:
	build/example

You can find an additional example in the 3rdparty directory of the EmbeddedMT project:
https://github.com/tass-belgium/EmbeddedMT
