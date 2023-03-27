#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Navesti dva direktorija"
  exit 1
fi

if [ ! -d "$1" ]; then
  echo "Prvi direktorij ne postoji"
  exit 1
fi

if [ ! -d "$2" ]; then
  echo "Drugi direktorij ne postoji"
  exit 1
fi

for file1 in "$1"/*; do
  file2="$2/$(basename $file1)"
  if [ "$file1" -nt "$file2" ] || [ ! -e "$file2" ]; then
    echo "$file1 --> $2"
  fi
done

for file2 in "$2"/*; do
  file1="$1/$(basename $file2)"
  if [ "$file2" -nt "$file1" ] || [ ! -e "$file1" ]; then
    echo "$file2 --> $1"
  fi
done