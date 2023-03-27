#!/bin/bash

if [ "$#" -ne 1 ]; then
echo "Navedite ime direktorija."
exit 1
fi
if [ ! -d "$1" ]; then
echo "Direktorij koji ste naveli $1 ne postoji."
exit 1
fi

images=""

for file in "$1"/*.jpg
do
name="$(basename "$file")"
gggg=${name:0:4}
mm=${name:4:2}
date="${gggg}${mm}"
dates+="$date "

map["$date"]+="$(basename "$file")?"
done

image_folders=($(echo "${dates[@]}" | sed 's/ /\n/g' | sort -u ))

for unique_date in "${image_folders[@]}" 
do 
m=${unique_date:0:4}
y=${unique_date:4:2}
echo -e "\n$m-$y :" 
echo "----------"
map_value=${map["$unique_date"]}
sorted_map_value=($(echo "$map_value" | sed 's/?/\n/g' | sort))
count=1
for image in "${sorted_map_value[@]}"
do
echo -e "\t$count. $image" 
count=$((count+1))
done
echo "--- Ukupno: $count slika -----"
done
