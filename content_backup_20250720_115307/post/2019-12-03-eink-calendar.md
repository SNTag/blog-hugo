---
categories:
- project
- hobby
- eink
- python
- org-mode
date: "2019-12-03T00:00:00Z"
author: "Shayonendra N. Tagore"
date-string: NOVEMBER 12, 2019
title: 'eink calendar: Part 1'
---

**UPDATE 2020, Oct 16** I stopped trying to modify my kobo ereader a long while back. When I started the project, I was enjoy a ready access to nearby libraries and the joys of physical books. I've come to find that there is room for the Kobo in my library, especially for the heavier books like _Les Miserable_ and _The Count of Monte Cristo_ that are just too big to carry around. I imagine I'll return to this project one-day when I get a new ereader, but that probably won't be for a long, long time. I'm more likely to substitute the ereader for a dedicated eink display.

When I first started using org-mode on Emacs, the agenda option seemed like too much hassle.  There was too much programming involved, too many shortcuts to remember (like anything Emacs), and it just wasn't pretty.  But mid-2019, most other methods to become organized just didn't click, and org-agenda seemed ever-more appealing.  With a little bit of effort (or in my case, copy-paste) in the configuration, I've managed to get something that works.  What I need now is someway to get a device to give me daily notifications when something is coming up.  That's when I realized that my eink Kobo reader could be it!

I love my Kobo e-reader, but its not as useful as the newer versions with a direct link to the library.  I've gone back to regular old paper and pen.  Besides, my need to get organized takes priority.

Here's the rough plan: with a bit of effort, the Kobo can be reprogrammed to display my org-agenda, along with little snippets of extra information (weather for instance) using Python.  My Emacs will generate an iCal file.  This file will be uploaded to my Kobo reader through the internet for the Python program to process and generate an eink display of my calendar.

![My Kobo e-reader](/images/posts/kobo-eink-display-1.jpg)

However, here's the main challenge to getting this project working; I can't seem to hack into the Kobo e-reader.  I've come across resources, and can detect my Kobo on Linux.  But something is preventing that final step...Once I hack into the reader, it's another thing to understand the operating system to get a python script working.  I suspect I'll have to get a raspberry pi involved at some step, or drop the Kobo for a dedicated eink display hooked directly to my raspberry pi.

The iCal files can be read using python package [iCalendar](https://pypi.org/project/icalendar/).  The details can then be easily extracted, requiring only formatting to get working.  Setting up the python program to generate a display should not be difficult.  There is still a good deal of information to read to ensure I understand what is necessary to influence the display of an eink display, and what is possible.

To get my Emacs to generate a new iCal file whenever modifications are made, I'm referring to this [site](https://orgmode.org/worg/org-tutorials/org-google-sync.html).  I'm hesitant to post details on my current approach just yet as I suspect it will change.  Using a file sharing service (ssh, sync-thing, etc.), the iCal file will be shared to the Kobo.  However, if the Kobo OS is too foreign, the Raspberry Pi will be used to process the iCal file, and dictate to the Kobo how to display the calendar.  The best case scenario is that the Kobo is able to run python and have access to a file sharing service.
