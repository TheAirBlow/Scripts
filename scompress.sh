#!/bin/bash
IFS=$'\n'

term() {
  echo "Exiting..."
  exit -1
}

trap term INT

echo "This will recursively compress ALL images, gifs and videos."
read -p "Do you want to continue? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Cancelled by user"
  exit -1
fi

for file in $(find . -type f -name "*.png" -o -name "*.jpg" -o -name "*.jpeg"); do
  new=${file%.*}.webp
  echo "$file -> $new"
  magick "$file" -quality 80 -strip -resize 1920x1080\> "$new"
  rm "$file"
done

for file in $(find . -type f -name "*.gif"); do
  new=${file%.*}.webp
  echo "$file -> $new"
  #gif2webp "$file" -o "$new"
  magick "$file" -resize 2400x1080\> -delay 4 "$new"
  rm "$file"
done

for file in $(find . -type f -name "*.mp4" -o -name "*.mov" -o -name "*.wmv" -o -name "*.mkv"); do
  new="${file%.*}.mp4"
  echo "$file -> $new"
  ffmpeg -i "$file" -vf scale=-2:2400,scale=1080:-2 -crf 18 -c:v libx265 -an "${file}_tmp.mp4"
  rm "$file"
  mv "${file}_tmp.mp4" "$new"
done
