# Provides info about a directory's content

print_menu () {
	echo -ne "Name"
	echo -ne "\tType"
	echo -e "\tSize"
	for j in `seq $cols`;
	do
		echo -ne "-"
	done
}

print_info () {
		
	flnms=`ls $dir`
	cd $dir
	for i in $flnms;
	do
		echo -n -e "$i |"
		echo -e -n " $(file $i | cut -d" " -f2-) |"
		echo -e  " $(du -shc $i | tail -n 1 | cut -f1) ||"
	done
	for j in `seq $cols`;
	do
		echo -ne "="
	done
	echo -e "Total size of directory: $dir_size"
	exit
	

}

dir=$1
cols=$(stty size | cut -d" " -f2)
dir_size=$(du -shc $dir | tail -n 1 | cut -f1)



if [ ! -d "$dir" ]; then
	echo goodbye
	exit
fi

print_menu
print_info
