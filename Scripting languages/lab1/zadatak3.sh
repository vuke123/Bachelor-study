#!/bin/bash

if ["$#" -ne 1 ]; then
echo "Navedite ime direktorija." 
exit 1 
fi 
if [ ! -d "$1" ]; then
echo "Direktorij koji ste naveli $1 ne postoji." 
exit 1 
fi 

for file in "$1"/*-02-*
do
date=$(basename "$file" | cut -d'.' -f 1)
y=$( basename "$date" | cut -d'-' -f 3 ) 
m=$( basename "$date" | cut -d'-' -f 2 ) 
d=$( basename "$date" | cut -d'-' -f 1 ) 
echo "datum: $d-$m-$y" 
echo "---------------------------------------------------"
cut -d'"' -f 2 "$file" | sort |uniq -c | sort -r
done
