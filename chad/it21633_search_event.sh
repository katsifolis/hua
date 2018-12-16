# Queries the db for an event

# Deletes a record from the db with date as identifier

IFS=$'\n'

read -p "Specify the info | time of the file you wish to search: " val

cat "./events.csv" | grep -E "^$val$|$val"

