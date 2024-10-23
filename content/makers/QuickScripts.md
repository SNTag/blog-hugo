---
title: "Quick Scripts"
author: "SNTag"
date: "2024-10-23T00:00:00Z"
layout: post
summary:
    "**System Quick Scripts**: A collection of scripts I've found handy on a linux system."
categories:
  - Makers
  - md
  - pdf
  - linux
---

# My System setup
## Rapid switch caps, ctrl
using Gnome Tweak Tools.

```sh
#!/bin/bash

# Function to enable the Caps Lock and Ctrl swap
enable_swap() {
    echo "Enabling Caps Lock and Ctrl swap..."
    gsettings set org.gnome.desktop.input-sources xkb-options "['ctrl:nocaps']"
    echo "Swap enabled."
}

# Function to disable the Caps Lock and Ctrl swap
disable_swap() {
    echo "Disabling Caps Lock and Ctrl swap..."
    gsettings reset org.gnome.desktop.input-sources xkb-options
    echo "Swap disabled."
}

# Check if the user provided an argument
if [ "$1" == "enable" ]; then
    enable_swap
elif [ "$1" == "disable" ]; then
    disable_swap
else
    echo "Usage: $0 {enable|disable}"
    exit 1
fi

```
chmod +x toggle_caps_ctrl.sh

./toggle_caps_ctrl.sh enable
./toggle_caps_ctrl.sh disable
## Keyboard Numlock Check
Will check if numlock is on every 5 minutes, and if on, wait 2 minutes before turning it off. Generated using ChatGPT

needs following : &ldquo;sudo apt-get install xdotool x11-xserver-utils&rdquo;

```sh
#!/bin/bash
    
# Function to check and turn off Num Lock
check_and_turn_off_numlock() {
    # Use xset to check the state of Num Lock
    numlock_state=$(xset q | grep "Num Lock:" | awk '{print $8}')
    check_count=0
    
    while [ "$numlock_state" = "on" ] && [ $check_count -lt 3 ]; do
        echo "Num Lock is on. Checking again in 2 seconds..."
        sleep 2
        numlock_state=$(xset q | grep "Num Lock:" | awk '{print $8}')
        check_count=$((check_count + 1))
    done
    
    if [ "$numlock_state" = "on" ]; then
        echo "Num Lock is still on after 3 checks. Turning it off..."
        xdotool key Num_Lock
        echo "Num Lock has been turned off."
    else
        echo "Num Lock is already off or was turned off during checks."
    fi
}
    
# Main loop
while true; do
    check_and_turn_off_numlock
    echo "Waiting for 30 seconds before checking again..."
    sleep 30  # Wait for 30 seconds before checking again
done
```
