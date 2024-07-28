#!/bin/bash
IFS=$'\n'

term() {
  echo "Exiting..."
  exit -1
}

trap term INT

for file in $(find . -type f -name "*.png" -o -name "*.jpg" -o -name "*.jpeg"); do
  new=${file%.*}.webp
  echo Converting $file into WEBP...
  magick "$file" -quality 80 -strip -resize 1920x1080\> "$new"
  rm "$file"
done

for file in $(find . -type f -name "*.gif"); do
  new=${file%.*}.webp
  echo Converting $file into WEBP...
  gif2webp "$file" -o "$new"
  rm "$file"
done

for file in $(find . -type f -name "*.mp4" -or -name '*.mov' -or -name '*.wmv' -or -name "*.mkv"); do
  echo Compressing $file...
  ffmpeg -i "$file" -vf scale=-2:2400,scale=1080:-2 -crf 18 -c:v libx265 -an "${file}_tmp.mp4"
  rm "$file"
  mv "${file}_tmp.mp4" "${file%.*}.mp4"
done
