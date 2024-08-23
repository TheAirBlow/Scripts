#!/bin/bash
term() {
  echo "Exiting..."
  exit -1
}

trap term INT

echo "otval daemon (real)"
state="normal"
while true; do
    fping -c1 -t5000 1.1.1.1 &> /dev/null
    if [ $? -eq 0 ]; then
        if [ "$state" == "otval" ]; then
            notify-send -i critical -i notification-network-wireless-connected -a otval-daemon "Интернет ожил!"
            echo "we're back online"
        fi
        state="normal"
    else
        if [ "$state" == "normal" ]; then
            notify-send -i critical -i notification-network-wireless-disconnected -a otval-daemon "Произошёл отвал!!"
            echo "detected otval"
        fi
        state="otval"
    fi
    sleep 1s
done
