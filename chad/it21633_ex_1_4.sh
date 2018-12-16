# Checks the num of presences or absences on a particular course

presence=0
absence=0
usrnm="it21701"
dir="labs_2018-19"
cd $dir

read -p "Type your Team: " team
read -p "Type your UserName: " usr

files=$(ls | grep -e "$team$")

for i in $files; 
do
	if [[ -z $(cat $i | grep "$usr") ]];
	then
		((absence++))
		echo "$i"": 1"
	else
		((presence++))
		echo "$i"": 0"
	fi
done

echo "$usr: Presence: $presence Absence: $absence"
