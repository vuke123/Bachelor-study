#!/bin/bash

grep -i -e banana -e jabuka -e jagoda -e dinja -e lubenica namirnice.txt

grep -vi -e b   anana -e jabuka -e jagoda -e dinja -e lubenica namirnice.txt

grep -r -e '\b[A-Z]{3} [0-9]{6}\b' ~/projekti/

find . -type f -mtime +7 -mtime -14 -ls

for i in {1..15}; do echo $i; done

kraj=15

for i in {1..$kraj}; do echo $i; done #Rezultat -> {1..15}

for i in $(seq 1 $kraj); do echo $i; done

