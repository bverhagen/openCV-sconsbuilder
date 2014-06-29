#!/bin/bash
buildshLocation=$(dirname $0)
dir=$(cd $buildshLocation;pwd)

latest_stable_commit='2d81595ed4ac44dd02779485bdd76ec15edb4ee7'
current_dir=$(pwd)

cd $dir
if [ -d $dir/opencv ]; then
	# Update repository
	cd $dir/opencv
	git pull
else
	# Download repository
	git clone https://github.com/Itseez/opencv.git
fi

cd $dir/opencv
git checkout $latest_stable_commit
cd $current_dir
