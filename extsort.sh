#!/bin/bash
IFS=$'\n'

term() {
  echo "Exiting..."
  exit -1
}

trap term INT

if [ "$1" != "--skip-warning" ]; then
  echo "This will recursively sort ALL files by extension."
  read -p "Do you want to continue? [y/N] " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled by user"
    exit -1
  fi
fi

for file in $(find . -type f); do
  if [ -d "$file" ]; then
    continue
  fi
  if [ ! -f "$file" ]; then
    continue
  fi
  ext=${file##*.}
  echo Moving $file into $ext/
  mkdir -p "$ext/"
  mv "$file" "$ext/"
done
