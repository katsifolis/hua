# Modifies existing record of db
IFS=$'\n'

read -p "Specify the date & time of the file you wish to modify: " val

if [[ ! -z $(cat "./events.csv" | cut -d"," -f1 | grep "^$val$") ]];
then
	read -p "Please write down the modification: " input
	sed -i "/$val/ c\\$input" "events.csv"
	echo File modified successfully 
else
	echo File not found
fi
