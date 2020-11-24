---
title: "Digitizing collections"
author: "Shayonendra N. Tagore"
date: "2020-10-09 15:37:17"
layout: post
categories:
  - digitizing
  - diy
  - raspberry pi
  - server
---

I've begun creating a media server lately. Something that I never thought I would attempt. With the
number of relatively comprehensive streaming services, a media server did not make much sense. Not
to mention my ptsd thinking back to my teenage years of terrible data-handling. I would create
inumerable backups with minute differences, making it impossible to realize which one was the proper
backup when needed. I'm still surprised today by some backup hidden deep in my file systems. I
imagine I've learnt something from my last few years with linux, where I've learned rules to file
managment.


The appeal of a media server has been the BYOM (Bring Your Own Media) approach. I have a number of
CDs and movies in the house which are not easy to find online (think Criterion collection DVDs, the tv
show Eureka, or the number of classical music around the house). Plus, I did spend a decent bit of
cash in the past on digital media, and I did not want it to have been for naught!


I'm going to write here a general guide to how I got my system running, because many of the details
are ridiculously simple, and it should have been easier. I'll start by introducing my media server,
how I handle CDs, and how I've been ripping DVDs. I will state here that everything I've been
ripping are from a collection I own.


# The media server

I'm surprised how powerful the server I made is. I started it as a 'what-if' project, that has
become an important in-house source of entertainment. I was going to spend a max of 100$ above what
I have in the house to put the server together, because I figured it would overheat, be
underpowered, or just burn out. Most NAS systems described online cost a minimum of 400$. I used a
35$ raspberry pi. Turns out, a raspberry pi is more than enough (total cost is less than ~150$
SGD). My system needed just:

- 3A power supply at 5V
- Raspberry pi 3b+ or better
- MyTraveller WD external HDD

Of course, this is the bare minimum. The raspberry pi can be replaced with a proper computer or NAS
system. The raspberry pi is looked down upon in forums for the more advanced media servers, but I
don't feel as if i'm missing anything. It performs wonderfully for just media and one attached HDD
without overclocking, becoming undervoltage, or overheating. Adding more than one HDD does stand the
chance of undervoltage, which can be solved through powered USB hubs. I recommend doing your own
research there. I saw some hubs can shorten HDD lifespans due to improper power supply, or that was
just poor luck on part of the user. Over heating is a risk with multiple users. Think three or more
users. At two users, I got temps in the 70Cs, and I'm in Singapore with an ambient temp of ~30C.


**update**: For large movie files, using chromecast ontop of the raspberry pi can sometimes have
long loading times. I'm not sure if I'm doing something wrong, or the raspberry pi is having issues
converting files to the appropiate format.


There are some concerns about power supply. An HDD needs 5V at minimum 0.5A (rest) or ~0.7A
(spinning) for external portable hdd. That is already easily provided by the USB hubs, assuming the
power supply is at least 2.5A or greater. Internal HDDs or running multiple HDDs have a higher power
requirement and absolutely should get power from other than the raspberry pi. Do note that I have
ensured that only a maximum voltage goes through the USB. I added a few lines to /boot/config.txt on
the raspberry pi as such:

```
# power managment for usb
max_usb_current=1

```


I had concerns at first about HDD lifespans, as a media server would be on 24/7. I imagined I would
implement a complicated system where the HDD would be spun down when not in use, and there are
guides for how to do that online. Do keep in mind that not all HDDs have that ability, like the WD
MyPassport external portable drives (like the one I am using). This does not have to be a concern:
shortly after setting it up, a redditor posted details about his build which is similar to
mine. Even has the same HDD, except its been running for 3 years for 24/7. It is better to just have an
extra HDD on the side for proper backup.


For the actual server, I make use of Plex. An audiophile with a massive music-only collection and a
large monthly budget would be more interested in Roon (I do not describe how to use Roon on the
raspberry pi). Roon is software similar to Plex but highly lauded. Unlike Plex, Roon will stream
lossless media, while Plex converts lossless to MP3 at max 360Kbps. This is not a big loss for me
given an important feature in Plex missing in Roon: the option to listen to your collection outside
of the home.

Plex has three options depending on your budget:

- **Free** :

You can stream to your PCs free of charge! portable devices (tablets, phones) require an app that costs ~7$. However, once you bought it on a system (android, iOS), you can install it as many times as you want on any devices. You are also limited to one user, meaning only one user profile allowed. The last troublesome detail is that you cannot download music for offline usage on the apps.

- **monthly** :

Free access to ALL apps (including one called plex-amp), multiple user profiles, offline download
for the apps, and access to a list of special discounts and apps. Roughly 7$ per month.

- **lifetime subscription** :

one time charge, and all the benefits of monthly forever.


I went with the free option, and its suiting me just fine.


I do recommend having more than one hdd to store all your media. Its just proper habit. I have
another HDD stored separately to which I backup the server to every two weeks.


# The music ripping process

I have two pieces of invaluable software for the ripping; abcde and MusicBrainz.


## abcde

abcde is a minimal, terminal based ripping software. The output can be customized with a config file
in '/etc/abcde.conf'. I have a relatively simple config file that can be seen in my
[dotfiles](https://github.com/SNTag/.dotfiles/blob/master/abcde.conf). Ultimately I use abcde to get
the CDs in my system with minimal metadata. I process the data further using MusicBrainz. While
abcde has in-built functions to communicate with MusicBrainz, it sometimes cannot identify the CD
for one reason or the other. These are usually minor issues that the full MusicBrainz software has
options for but the terminal has limited options. To be honest, I probably don't have the right bit
of code; I have to manually modify the conf file to ignore the MusicBrainz database when the
roadblocks appear. Ultimately, I use abcde to get the CDs in with or without basic metadata.

I recommend these sites for further information:
- [abcde man page](https://linux.die.net/man/1/abcde)
- [rip cd with abcde](https://www.maketecheasier.com/rip-cd-with-abcde/)
- [reddit: What’s the current best CDDB/musicbrains config for abcde?](https://www.reddit.com/r/DataHoarder/comments/hcvy12/whats_the_current_best_cddbmusicbrains_config_for/)


## MusicBrainz

While abcde can pull information from MusicBrainz, I have not bothered to configure abcde to work
perfectly with the software. I'm working with a lot of classical music CDs, some of which are not
properly in the MusicBrainz catalogue (which is pretty damn comprehensive, abcde just can't find the
proper CD ID in the catalogue from the terminal). MusicBrainz is an amazing piece of software, and
open to user contributions like wikipedia. Any gaps can be filled in by the user. Plus, it can grab
cover art!

There are a number of configurations that I encourage people to look into, such as renaming files by
metadata, and automatic sorting into a file-hirearchy. A number of problems can be encountered, but
all of them are simple, and honestly easily solved by searching online.

For more information on setting up MusicBrainz, I recommend these guides:
- [how to master your music metadata](https://www.techhive.com/article/3192777/how-to-master-your-music-metadata-part-1.html)
- [Music Organizing with MusicBrainz Picard](https://forums.plex.tv/t/howto-music-organizing-with-musicbrainz-picard/218734)


# The DVD ripping process

My software of choice here is HandBrake. I've been ripping a series of Bergmans, Kurosawa, and
Satyajit Rays into my server using HandBrake for a few days, and have settled on a process. As I
understand it, HandBrake has presets for configuring the system (cropping of black bars, level of
quality, etc). The correct preset just has to be selected and start it. If the DVD has multiple
files (trailers, commentaries, etc), make sure to select each one in the drop-down menu, decide what
you want to name the file, add to queue, and repeat until everything is in the queue before
starting. Further customization may be wanted, I often have to modify the audio to add an extra
commentary option, or add subtitles for foriegn films, nothing too strenuos to do.

No real pre-customization is needed to use the software.


# In the future

I have a couple of ideas for how I would improve this media server in the future. For one, this
system limits audio output to mp3 360kbps. The HDD has flac, and I want to hear that through a
couple of good speakers that I have. To do that, I need to hook the raspberry pi directly to the
speakers, and have the music play *from* the raspberry pi.

Another improvement I need to make is a proper backup system. Both topics will be potentially
problematic, and I'll be sure to post my approach if I ever get to it.
