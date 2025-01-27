#!/bin/bash
IFS=$'\n'

term() {
  echo "Exiting..."
  exit -1
}

trap term INT

echo "This will recursively clear ALL files that weren't commited or were .gitignored!"
read -p "Do you want to continue? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Cancelled by user"
  exit -1
fi

for dir in $(find -type d -name ".git" -prune 2>/dev/null)
do
  git -C "$dir/../" clean -Xdf
done
