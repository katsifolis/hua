# Lists the records sorted by asc/desc

read -p "Give the day you wish to see the upcoming events for" val

grep $val "events.csv"
