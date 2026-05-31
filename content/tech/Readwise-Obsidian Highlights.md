---
title: Readwise to Obsidian
author: SNTag
date: 2026-05-17T00:00:00Z
layout: post
summary: Atomic notes for a designed daily template.
tags:
  - Obsidian
  - Readwise
  - CommonPlace_Book
  - Tech
---

Lately, one of my biggest complaints is that I have setup a beautiful daily periodic notes setup. As I'm using readwise more and more, I wanted to have my quotes displayed in a beautiful format! I've put together this code for putting together my images. I'll add more details sporadically to this post, how it works, and how it looks!

<p style="text-align: center;">
<b>Github Repository</b> <br>
<a href="https://github.com/SNTag/Readwise-to-Obsidian">https://github.com/SNTag/Readwise-to-Obsidian</a>
</p>

![Example of a quote in my new system](content/photos/Pasted%20image%2020260520083541.png)

The repository works in 2-steps tied together by the values in a config file.

**Script 1**
Creates a local CSV with columns taken from Readwise, and adds two: CommonPlace & Updated.

**Script 2**
Depending on the presence of Y in each row of CommonPlace & Updated, a note will either be generated in obsidian or updated. 

Using a templater template as dedicated by the config file, each note is formatted into a neat quotes callout. Unfortunately, this is a slow script, as templater does not seem to work if the script is accelerated...