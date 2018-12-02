# Lists files within a dir with zero file size and their empty subdirs

if [ -z $1 ];
then
	echo No file provided
	exit
fi

dir=$1

if [ -d "$dir" ]; then
	flnms=`ls "$dir"` # all names into a list 		
	cd $dir
	echo "-- Empty Files --"

	# Separating the regular files from directories
	for i in $flnms; 
	do
		if [ -f "$i" ]; 
		then 
			flnm=`cat "$i"`
			if [ "$flnm" == "" ];
			then
				echo "$i"
			fi
		fi
	done
	echo -e "\n-- Empty Directories --"

	# Printing the empty folders
	find -type d -empty | sed 's/regexp/\n/g'
else
	echo Given file is not a directory!
	exit
fi
