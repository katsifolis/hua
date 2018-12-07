# Deletes a record from the db with date as identifier

IFS='\n'

read -p "Specify the date & time of the file you wish to delete: " val

mapfile -t lines < "./events.csv"

for i in ${lines[@]};
do
	echo $i
	if [[ $val == $(echo $i | cut -d"," -f1) ]];
	then
		sed -i /$val/d "events.csv"
		echo Found and Deleted
	else
		echo Not Found
	fi
done
