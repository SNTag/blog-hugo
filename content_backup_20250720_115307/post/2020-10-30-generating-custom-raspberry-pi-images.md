---
title: "Generating custom raspberry-pi images"
author: "SNTag"
date: "2020-10-30 14:17:40"
layout: post
categories:
- blog
- diy
- raspberry pi
---

I've been working on a number of projects involving my raspberry pi; DSLR timelapse, a pi running
dedicated stocks and notifications systems, and a media server. I have a silly approach of solving
any critical errors by flashing a new raspbian image to the SD card and continuing as if the error
was never made. The approach can be heavily criticized, but I'm not invested in immediately working
out the errors; it's usually something obscure. 90% of the time, some critical software was just
installed the wrong way. I've been looking for easy ways to set up my raspbian images from the
get-go and found what I think is the best approach: [Pi-gen](https://github.com/RPi-Distro/Pi-gen).

The easiest and most common alternative is [pi-bakery](https://www.pibakery.org/). I strongly
recommend it to those new to the raspberry pi. It modifies the official raspbian image using
'recipes' (colourful and easy-to-understand codeblocks). However, take note that it has limitations
when moving outside the standard code-blocks and it is officially unsupported (there may be a pibakery2
at some point).

[Pi-gen](https://duckduckgo.com/?t=canonical&q=pi-gen&ia=web) creates a custom-made raspbian image
from scratch. Its use assumes you have some degree of experience with bash. This post is meant to be an
update of sorts to the original article that got me onto
[pi-gen](http://kmdouglass.github.io/posts/create-a-custom-raspbian-image-with-pi-gen-part-1/). The
original article includes steps that are more easily configured as of late.


# Pi-gen

**I want to repeat that I wrote this to add onto the details in [the original
post](http://kmdouglass.github.io/posts/create-a-custom-raspbian-image-with-pi-gen-part-1/) that
introduced me to pi-gen.** The original post did not make use of some very handy options available
to set up a variety of features which inspired this post. It is even easier to make an image than
the original post makes it seem.

The pi-gen software is easy and incredibly useful. Pi-gen is the tool used to generate the official
raspbian images, so you can be confident that it works. I recommend the first-time user to jump to
'Building the image' below after installing docker and Pi-gen ('Getting the software'). It will
generate the standard desktop version of raspbian, but it will confirm that Pi-gen is working. Be
fore-warned, generating a new image can be a lengthy process (took me a little over 30 min on a
strong laptop) and consume a lot of space (several GB).

If you follow this guide step by step, I will show you how to build a custom raspbian lite
image. You can create a custom image with Desktop enabled too if you skip the section 'Stages'
below.

The raspbian image will have:
- Personalized username
- Changed password
- Timezone setup
- SSH and wifi configured
- custom packages installed (such as git)

## Getting the software

You will need 'docker' to run Pi-gen. Instructions to install it can be found
[here](https://docs.docker.com/engine/install/).

The first step is to get the software.

```{bash}
cd ~
git clone https://github.com/RPi-Distro/Pi-gen

```

## Stages

**WARNING** skip this section to create an image with Desktop enabled.

The software builds a custom raspbian image in [stages](https://github.com/RPi-Distro/Pi-gen#stage-anatomy) (see the git page for more info):
stage0 - absolute minimal filesystem
stage1 - makes it bootable
stage2 - sets up a lite system
stage3 - sets-up the desktop experience
stage4 - the normal raspbian image. installs software standard to new users.
stage5 - the normal raspbian image. installs bloatware.

I'm interested in setting up a headerless raspberry pi, so I disable stage 3, 4, 5 by making simple
files. To make a full raspbian image with desktop enabled, ignore the following.

```{bash}
touch ./stage3/SKIP ./stage4/SKIP ./stage5/SKIP
touch ./stage4/SKIP_IMAGES ./stage5/SKIP_IMAGES

```

## Adding custom details

It is very easy to configure Pi-gen. Make a config file ( /pi-gen/config ) and add the following:

```{bash}
# image name
IMG_NAME=puck

# account details
FIRST_USER_NAME="Puck"
FIRST_USER_PASS="JackShallHaveJillNoughtShallGoIll"

# timezone
LOCALE_DEFAULT="en_US.UTF-8"
TIMEZONE_DEFAULT="America/New_York"

# connectivity

ENABLE_SSH=1
WPA_ESSID="MinisTirith"
WPA_PASSWORD="Gandalf"
WPA_COUNTRY="US"

```

Pi-gen has a [series of useful comands](https://github.com/RPi-Distro/Pi-gen#config) that enable
easy-modification of a number of features. You can probably guess what each variable does, but I
will go over it in detail.

### Image name

This line decides the name of the image you are creating. for me, I called it simply
['Puck'](https://en.wikipedia.org/wiki/Puck_(A_Midsummer_Night%27s_Dream)), after the main
user-account that will be assigned to the image.

```{bash}
IMG_NAME=puck

```

### User settings

I strongly recommend changing the default username and password. You can always change this again,
but the default values in a raspbian image are too well known and far too easy a target.

The first line says what the main user-name should be. The default is `pi`, and you always want to
change that to reduce chances of a security breach. To have any mischief nought go ill, you should
change the password too by setting the variable `FIRST_USER_PASS`.

```{bash}
FIRST_USER_NAME="Puck"
FIRST_USER_PASS="JackShallHaveJillNoughtShallGoIll"

```

### Time

I want the raspberry to be on the same time as me. Both of these lines inform the timezone.

```{bash}
LOCALE_DEFAULT="en_US.UTF-8"
TIMEZONE_DEFAULT="America/New_York"

```

### Connections

And finally, whats the point of all this effort if I cannot connect to Puck? I want SSH enabled from
the get go by setting `ENABLE_SSH` to 1. The name of the wifi to connect to is given
through `WPA_ESSID` along with the password (`WPA_PASSWORD`) and the country (`WPA_COUNTRY`).

If you are going with a desktop image, I recommend disabling ssh (`ENABLE_SSH=0`) unless you know
what you are doing. It will be safer.


```{bash}
ENABLE_SSH=1
WPA_ESSID="MinisTirith"
WPA_PASSWORD="Gandalf"
WPA_COUNTRY="US"

```

### Etc

The only other value that you may have an interest in setting (and unmentioned here)
is `KEYBOARD_LAYOUT`, but as I am typing in English, I'm happy enough leaving it to the default.

## Installing specific packages

There are some packages that I want the image to come pre-built. Git, for one. This is a simple
issue of modifying the file in /Pi-gen/stage2/01-sys-tweaks/00-packages. Add each package of
interest in a new line, and it will be installed using the command `sudo apt-get install`.

## Building the image

Even if you haven't done the above steps, you can build an image. It only requires maximum of two
lines too. Go to the root directory of Pi-gen, and:

```{R}
./build-docker.sh

```

There is a decent chance for the build to get interrupted. In most cases, the following will save you:

```{R}
CONTINUE=1 ./build-docker.sh

```

The image should now be in `/Pi-gen/deploy/` with the value you passed `IMG_NAME` in the file name
as a zipped file. To get to the image, `unzip image_${DATE}_${IMG_NAME}.zip` in the directory of
your choice.

## Flashing the image

**WARNING** Be sure of paths in this step! You can easily overwrite/delete/crash you system and your
data if done improperly! If you want to play it safe, there are software to handle image flashing such as [balenaEtcher](https://www.balena.io/etcher/). I have not used such programs, I cannot tell you how good it is.

At this point, insert your SD card into your system. MAKE SURE YOU KNOW WHERE YOUR SD-CARD IS. A
simple approach is to open a program like GParted, and see where it is. ex., for me, it
is `/dev/mmcblk0`. Otherwise you can use the terminal command `df`. Simply observe changes in the
list without the SD card inserted and with it in. Navigate to the directory where you have unzipped
your image and give the path to the SD card to the variable `of=`, as I have below.

```{bash}
sudo dd if=2020-10-27-puck-lite.img of=/dev/mmcblk0 bs=4096; sync

```

After this, all that's left is plugging your SD card into the pi and letting it install.

# Tips for those seeking advanced manipulation

**WARNING: The following are ruminations I had on how to go about doing something. I cannot promise it would work.**

There are some other features people may be interested in, but I have not tried them out. Features
such as installing a program using git or modifying the rc.local.

## Install programs to the image using git

To have the image install a git program, you can try making a /Pi-gen/stage2/03-git/ folder as [this
fellow mentioned](https://github.com/RPi-Distro/pi-gen/issues/210). Looking at
/Pi-gen/stage2/01-sys-tweaks/ as an example, the majority of the commands are decided in
01-run.sh. Such a file under /Pi-gen/stage2/03-git/01-run.sh may be made to install programs. I have
not attempted this, but I do plan to try this at some point to get my dotfiles and other programs on
there faster.

## modifying rc.local

https://github.com/RPi-Distro/pi-gen/issues/246

It seems to be an easy task. I have not attempted it myself, so I won't go into the details here. Just know it is possible.

# References

[learnthinksolve](https://learnthinksolvecreate.wordpress.com/category/raspberry-pi/pi-gen/)

[kmdouglass](http://kmdouglass.github.io/posts/create-a-custom-raspbian-image-with-pi-gen-part-1/)

[Pi-gen](https://github.com/RPi-Distro/Pi-gen)
