---
title: "Quick Scripts"
author: "SNTag"
date: "2024-10-23T00:00:00Z"
layout: post
summary:
    "**System Quick Scripts**: A collection of scripts I've found handy for a linux system. Includes quick-installation scripts."
categories:
  - Makers
  - md
  - pdf
  - linux
---

# Quick Install: Pop-OS
THIS IS THE SCRIPT TO QUICKLY GET BASIC SOFTWARE UP ONLY. For further config, see "System Setup" Below.
See "Current install setup" below or install.txt in Files > Documents > org-files.

Current install setup will ONLY install programs to avoid future issues with basic file redundancies.

```
        # Basics
    sudo apt install -y gnome-tweaks            # tweaks!!!
    sudo apt install -y nmap                        # networking!!!
    sudo apt install -y zsh                        # shell
    sudo apt install -y htop		# extras
    sudo apt install -y texlive
    sudo apt install -y vlc
    #sudo apt install -y tlp                   # Confirm before install using
    #sudo apt install -y tlp-rdwsudo           # what does it do?
    sudo apt install -y inotify-tools
    
    sudo add-apt-repository universe
    sudo apt update
    
    
    # Install Nerd Fonts?
    #git clone https://github.com/ryanoasis/nerd-fonts.git
    #sudo ./nerd-fonts/install.sh
    
    
    ### tweaks
    ## https://www.digitalocean.com/community/tutorials/how-to-configure-periodic-trim-for-ssd-storage-on-linux-servers
    # sudo systemctl enable fstrim.timer     # Confirm before install using sudo systemctl status fstrim.timer
    
    
    # Software
    sudo apt install -y guake                       # terminal
    sudo apt install -y grsync
    sudo apt install -y darktable rawtherapee inkscape gimp		# photography, file editing
    # sudo apt install -y gparted		# tooling # Comes preinstalled in pop OS?
    sudo apt install -y qbittorrent
    #### MISSING GNOME TWEAKS

# Update font cache
sudo fc-cache -f -v
    
    #flatpak install flathub com.spotify.Client      # See https://flathub.org/apps/com.spotify.Client
    flatpak install flathub com.zoho.Notebook        # See https://flathub.org/apps/com.zoho.Notebook
    #flatpak install flathub com.rtosta.zapzap       # See https://flathub.org/apps/com.rtosta.zapzap
    
    # Proton vpn needs intervention. Use flathub instead?                # https://protonvpn.com/support/official-ubuntu-vpn-setup/
    # webapp-manager needs intervention.                                 # https://fosspost.org/how-to-install-webapps-on-linux/
    # AppImage Pool needs invervention Pop Shop
    
    #Do I need ubuntu-restricted extras? sudo apt install -y ubuntus-restricted-extras
```
## Setting up R
```
sudo apt update
sudo apt install r-base r-base-dev
```
### For RStudio
Code does not download latest version.
```
cs ~/
wget https://download1.rstudio.org/electron/jammy/amd64/rstudio-2024.09.0-375-amd64.deb
sudo apt install ./rstudio-2024.09.0-375-amd64.deb
```
# Scripts
Quick collection of scripts that I use day-to-day, and imagine others may find useful.
## Rapid switch caps, ctrl
using Gnome Tweak Tools.

```sh
#!/bin/bash
## Comments
## Enable will make ctrl act as ctrl, and caps as caps lock.
## Disable will make ctrl act as a caps lock button, and the caps button act as a ctrl.

# Function to enable the Caps Lock and Ctrl swap
enable_swap() {
    echo "Enabling standard keyboard layout (Caps=Caps, Ctrl=Ctrl)..."
    gsettings reset org.gnome.desktop.input-sources xkb-options
    sleep 2  # Allow time for X server to apply changes
    echo "Standard layout enabled."
}

# Function to disable the Caps Lock and Ctrl swap
disable_swap() {
    echo "Disabling standard layout (Caps=Ctrl, Ctrl=Caps)..."
    gsettings set org.gnome.desktop.input-sources xkb-options "['ctrl:swapcaps']"
    sleep 2  # Allow time for X server to apply changes
    echo "Swapped layout enabled."
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

Add to ~/.local/bin/. Run `chmod +x toggle_caps_ctrl.sh` to make it executable.

Takes commands:
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
## Find the Raspberry Pi IP
Takes either no input or just 'pi'. If you input nothing, finds all IP addresses on your network. If you input 'pi', finds ip of raspberry pi. Not my script, I copied this and added some tweaks from someone else a long time ago on the internet.
```bash
function raspPiFinder {
    if [ "${1}" == "pi" ]; then
        sudo nmap -sP 192.168.1.111/24 | awk '/^Nmap/{ip=$NF}/B8:27:EB/{print ip}'

    else
        sudo nmap -sP 192.168.1.111/24

    fi
}

raspPiFinder $1
```