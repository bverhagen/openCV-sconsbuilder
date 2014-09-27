#!/bin/bash
buildshLocation=$(dirname $0)
dir=$(cd $buildshLocation;pwd)

wgetbin='wget'
unzipbin='unzip'
opencv_repo='Itseez/opencv'
#opencv_latest_stable_commit='99eed2d885a2232453e911672cbe98c5001fec6b'
opencv_latest_stable_commit='f187fd99da878e98432c421b57a948a77216c361'

function downloadFromGithub {
	$wgetbin http://github.com/$1/archive/$2.zip
}

function unzipGithub {
	$unzipbin -q $1.zip
	mv $2-$1 $2
}

function getFromGithub {
	# Check if versions correspond
	if [ -d $dir/$1 ]; then
		if [ -f $dir/$1/commit ]; then
			. $dir/$1/commit
			if [ $version != $opencv_latest_stable_commit ]; then
				rm -rf $dir/$1
			fi
		fi
	fi

	# Recheck if the folder still exists. Download and/or unpack otherwise
	if [ ! -d $dir/$1 ]; then
		if [ ! -f $dir/$3.zip ]; then
			# Download repository
			downloadFromGithub $2 $3
		fi
		# Unzip
		echo 'Unzipping...'
		unzipGithub $3 $1
		echo 'version='$3 > $1/commit

		if [ $? == 0 ]; then
			rm $3.zip
		fi
	fi
}

current_dir=$(pwd)
cd $dir

getFromGithub 'opencv' $opencv_repo $opencv_latest_stable_commit

cd $current_dir
