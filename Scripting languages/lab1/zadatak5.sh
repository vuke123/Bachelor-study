#!/bin/bash

if [ "$#" -ne 2 ]; then
echo "Navesti dva argumenta."
exit 1
fi

if [ ! -d "$1" ]; then
echo "Direktorij koji ste naveli ($1) ne postoji."
exit 1
fi

all_files=( $( find "$1" -type f -name "$2") )
count=0

for file in "${all_files[@]}"; do
    cnt_lines=$(wc -l < "$file")
    count=$((count+cnt_lines))
done
echo "Ukupan broj redaka je $count"
