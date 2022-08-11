#!/bin/sh

#Config Keyboard
#setxkmap es &

#Config Display
xrandr --output eDP1 --primary --mode 1366x768 --pos 0x0 --rotate normal --output DP1 --off --output HDMI1 --off --output HDMI2 --off --output VIRTUAL1 --off

#Icon System
udiskie -t &

nm-applet &

volumeicon &

cbatticon -u 5 &

nitrogen --restore &