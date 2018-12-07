# Lists the records sorted by current date
cur_date=$(date +%d%m%y | sed s/0/\ /)
echo $cur_date

cat "events.csv" | sort -rk $cur_date 
