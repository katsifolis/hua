# Inserts an event with the date as key_identifier

## I must find a correct value guard for date

pattern="[0-9]{2}"

read -p "Please provide the name of the event: " event_name
echo "The format of the date given should be DD-MM-YY HH:MM"
read -p "Please provide the date: " event_date

#if [[ $event_date =~ $pattern ]];
#then
#	echo matches
#else
#	echo doesnt match
#fi

read -p "Please provide some optional text: " event_opt

echo -en "$event_date, $event_name, $event_opt" >> events.cv
