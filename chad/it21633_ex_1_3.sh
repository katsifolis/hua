#!/usr/bin/bash

quota=5000
size=$(du -s /home/helios/hua/ 2>/dev/null | cut -f1)
size1=2700

res=$(bc -l <<< "$size / $quota")
echo $res
