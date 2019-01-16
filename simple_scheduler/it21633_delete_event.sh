# Deletes a record from the db with date as identifier

IFS=$'\n'

read -p "Specify the date & time of the file you wish to delete: " val

if [[ ! -z $(cat "./events.csv" | cut -d"," -f1 | grep "^$val$") ]];
then
	sed -i /$val/d "events.csv" 2> /dev/null
	echo File deleted successfully 
else
	echo File not found
fi
