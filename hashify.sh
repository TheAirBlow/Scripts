#!/bin/bash
IFS=$'\n'

term() {
  echo "Exiting..."
  exit -1
}

trap term INT

echo "This will recursively rename and move ALL files."
read -p "Do you want to continue? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Cancelled by user"
  exit -1
fi

for file in $(find . -type f); do
  hash=$(sha256sum "$file" | head -c 32)
  new="sus_$hash.${file##*.}"
  echo "$file -> $new"
  mv "$file" "$new"
done
