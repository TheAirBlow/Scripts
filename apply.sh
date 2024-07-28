#!/bin/bash
IFS=$'\n'
dir=$(realpath -e -- $(dirname -- "$0"))

git pull
for file in $(find $HOME/.local/bin -type l); do
  target=$(readlink "$file")
  if [[ "$target" == $dir/* ]]; then
    echo "[-] $(basename $target)"
    rm $file
  fi
done

for file in $(find "$dir" -type f -name '*.sh' -or -name '*.py'); do
  if [[ "$file" == "$dir/apply.sh" ]]; then
    continue
  fi
  name=$(basename "$file")
  echo "[+] $name"
  ln -fs "$file" "$HOME/.local/bin/${name%.*}"
  chmod +x "$file"
done
