#!/bin/bash

cmd="maim -u -l -b 4 -c 0.259,0.761,0.961,0.4"
end="| xclip -selection clipboard -t image/png"

if [ "$1" = "none" ]; then
  eval "$cmd $end"
elif [ "$1" = "ctrl" ]; then
  eval "$cmd -s -n 2 $end"
elif [ "$1" = "shift" ]; then
  echo "currently unused"
  exit -1
else
  echo "prtscr none - no modifier key pressed"
  echo "prtscr ctrl - any ctrl key pressed"
  echo "prtscr shift - any shift key pressed"
fi
