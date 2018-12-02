quota=5000000
size=$(du -s ~/ 2>/dev/null | cut -f1)
size1=2700

res=$(bc -l <<< "$size / $quota")

# The first cut is to get rid of the dot
percent=$(echo $res | cut -d"." -f2 | cut -b-2)
echo "You are using $percent% of your quota"
