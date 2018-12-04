# Modifies existing record of db

read -p "Specify the date & time of the file you wish to modify: " val
hello=0

if [[ $val == $(cat "./events.csv" | grep $val |  cut -d"," -f1) ]];
then
	cat "./events.scv" | grep $val
fi

