
# Lists the contents of the home folder which are over 100M in descending order

find ~/ -maxdepth 1 -type f -size +1k -exec ls -lh {} + | sort -hr -k 5
