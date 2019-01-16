#!/usr/bin/env bash
# A personal scheduler

SCR="$HOME/hua/chad/"
cols=$(stty size | cut -d" " -f2)
welcome="Welcome to Your Personal Agenda"
mid=$(($cols / 2))
algn_msg=$(($mid - ${#welcome} / 2))
str=0


align () {
	for i in `seq $algn_msg`
	do
		echo -n " "
	done
}

p_menu () {
	align;echo Welcome To Your Personal Agenda!
	align;echo -e "  \t1. Insert Event"
	align;echo -e "  \t2. Delete Event"
	align;echo -e "  \t3. Modify Event"
	align;echo -e "  \t4. Search Events"
	align;echo -e "  \t5. Preview Events"
	align;echo -e "  \t6. Preview Day Events"
	align;echo -e "  \t7. Quit\n"

}

selection () {

	read -p 'Make your Selection: ' answer

	while [ $answer != 7 ];
	do	
		case $answer in
			1 | "1")
				. "$SCR""it21633_insert_event.sh";;
			2)
				. "$SCR""it21633_delete_event.sh";;
			3)
				. "$SCR""it21633_modify_event.sh";;
			4)
				. "$SCR""it21633_search_event.sh";;
			5)
				. "$SCR""it21633_preview_events.sh";;
			6)
				. "$SCR""it21633_preview_day_events.sh";;
			7)
				echo "Have a nice day";;
			*)
				echo "Make a valid selection"
				

		esac
	p_menu
	read -p 'Make your Selection: ' answer
	done
	echo -n "Have a nice day"
	sleep 0.5
	echo  "!"
	sleep 0.5

}

p_menu
selection 
