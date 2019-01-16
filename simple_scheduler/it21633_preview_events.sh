# Lists the records sorted by current date
for i in $(wc -l "./events.csv" | cut -d" " -f1);
do
	cat "events.csv" | sort -nt"-" -k3 -k2 -k1
done
