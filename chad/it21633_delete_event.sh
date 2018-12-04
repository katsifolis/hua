# Deletes a record from the db with date as identifier

read -p "Specify the date & time of the file you wish to delete: " val

if [[ $val == $(cat "./events.csv" | grep $val |  cut -d"," -f1) ]];
then
	cat "./events.csv" | grep $val | sed s//\ /g
fi

