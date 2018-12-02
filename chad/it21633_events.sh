# A personal scheduler

cols=$(stty size | cut -d" " -f2)
mid=$(($cols / 2))

align (str) {

	for i in `seq $mid`
	do
		echo -n " "
	done

}

p_menu () {
	align; echo Welcome To Your Personal Agenda!
	align;



}

p_menu
