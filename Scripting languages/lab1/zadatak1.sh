#!/bin/bash

proba="Ovo je proba"
echo $proba

lista_datoteka=*

echo $lista_datoteka

proba="Ovo je proba"
proba3="$proba. $proba. $proba."
echo $proba3

a=4
b=3
c=7

d=$(( (a + 4) * b % c ))

echo "Vrijednost varijable a je: $a"
echo "Vrijednost varijable b je: $b"
echo "Vrijednost varijable c je: $c"
echo "Vrijednost varijable d je: $d"

broj_rijeci=$(cat *.txt | wc -w)

echo "Ukupan broj riječi u .txt datotekama: $broj_rijeci"

ls ~/
