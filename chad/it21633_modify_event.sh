# Modifies existing record of db
IFS='\n'
newinput="31, asjdfla, fjaldk"

read -p "Specify the date & time of the file you wish to modify: " val

mapfile -t lines < "./events.csv"

for i in ${lines[@]};
do
	if [[ $val == $(echo $i | cut -d"," -f1) ]];
	then
		echo Found and Deleted
		read -p "Please write down the modification: " input
		sed -i "/$val/ c\\$input" "events.csv"
		break
	else
		echo Not Found
	fi
done

