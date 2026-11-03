---
title: How I Setup an MBA Tracker in Obsidian
author: SNTagore
tags:
  - tech
  - obsidian
  - mba
added date: 2026-08-25, 5:53:50 pm
modified date: 2026-11-02, 7:34:01 pm
date: 2026-11-02T19:34:00
layout: post
summary:
Obs Category: MBA Recruiting
---

> [!note] This page will be the master page to my MBA Recruiting using Obsidian! I'm planning to pin this to the top of the MBA recruiting page as this section grows.

> [!danger] Many of the links in this page will EVENTUALLY function, providing tools, outlines and resources to best use this approach! They do not function yet! TBA

One of the challenges I've been wondering about is how to use Obsidian for MBA Tracking. I already use it so heavily for task tracking, CRM management, and collecting articles of note. I worry that I have been stretching what Obsidian should be, but an MBA tracker was missing from my Obsidian toolkit.

To give context, as I begin submitting applications, I need to have a method to track **application status**, **companies of interest**, **events of interest**, and the **people I meet**. Getting these features into Obsidian can be a bit tough, but I've found a system. The only issue I have with my method is that it does add some distinct yaml headers that serve no other purpose than as part of this particular tracker. As someone who has been trying his hardest to reduce clutter in the background settings, it didn't sit too well, but it does answer what I need right now.

# Prior Setup

Parts of this setup were installed and setup for my use previously. Specifically:

1. **TaskNotes Calendar**
2. **Templater**
3. **QuickAdd**

I'll outline the tracker I setup in the next section.

## 1. TaskNotes Calendar

This is what makes this setup possible. I have multiple calendars, and I've set them up to sync with TaskNotes Integrations. I've also setup a simple ICS calendar template that allows me to get this working. Because of this, I can create notes quickly and easily based on events I've blocked time for. To add on to this information, I use Templater to add extra yaml data.

## 2. Templater

While very much overkill for what I'm using it for, it tendency to combine pre-existing yaml data with the selected templater note is invaluable for this. Once I create a note in obsidian using TaskNotes Calendar, I use templater to add extra details if it is an interview or a recruiting event. To identify coffee chats in the tracker I'll describe, I simply add the tag 'coffee-chat' and 'consulting'.

## 3. QuickAdd

The only purpose for QuickAdd is to rapidly create application based notes, since it can quickly generate and populate notes from pre-specificed templates. It CANNOT replace templater as I can't seem to make it handle the yaml header combination trick in the same way!

# The Obsidian Tracker

As a quick Outline of what I created:

> [!danger] Many of these links do not function yet! TBA

|                                                                                                                                                 | Tracking Method                                                                                                                                                                                   | How To                                                                                                                                                                                     |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **[[Calendar/TaskNotes/Tasks/Stern Consultant Recruiting Tracker 2026 to 2028.base#Events & Recruiting Tracker\|Events & Recruiting Tracker]]** | Tracked using<br>#recruiting  AND Yaml > Obs type ICS <br>AND Yaml > Related > [[Calendar/TaskNotes/Tasks/Becoming a Consultant - Stern\|Becoming a Consultant - Stern]]<br>                      | 1. Create ICS using tasknotes calendar with template.<br>2. Run Templater > [[Efforts/TagOS/Templater/Stern Recruiting Events\|Stern Recruiting Events]]. Will merge yaml with prior note. |
| **[[Calendar/TaskNotes/Tasks/Stern Consultant Recruiting Tracker 2026 to 2028.base#Applications\|Applications]]**                               | In each Companies CRM, have:<br>Yaml > Related > [[Stern Consultant Applications 2028]]                                                                                                           | Run Quick Add > [[Efforts/TagOS/Quick Add Templates/Stern Consultant Application\|Stern Consultant Application]]                                                                           |
| **[[Calendar/TaskNotes/Tasks/Stern Consultant Recruiting Tracker 2026 to 2028.base#Interviews\|Interviews]]**                                   | Tracked using<br>#interview  AND AND Yaml > Obs type ICS AND Yaml > Related > [[Calendar/TaskNotes/Tasks/Becoming a Consultant - Stern\|Becoming a Consultant - Stern]]                           | 1. Create ICS using tasknotes calendar with template.<br>2. Rune Templater > [[Stern Interview Log]]. Will merge yaml with prior note.                                                     |
| **[[Calendar/TaskNotes/Tasks/Stern Consultant Recruiting Tracker 2026 to 2028.base#Case Tracker\|Case Tracker]]**                               | Needs:<br>- Rating - difficulty<br>- projects (becoming a consultant - stern)<br>- related (for identifying where my notes are)<br>- completed date<br>- tags: case-study                         | Run Quick Add > [[Efforts/TagOS/Quick Add Templates/Consultant Case Tracker\|Consultant Case Tracker]]                                                                                     |
| **Resources**<br>Tasks, #coffee-chat . & other resources                                                                                        | See [[Calendar/TaskNotes/Tasks/Becoming a Consultant - Stern#Tasks Dashboard\|Tasks Dashboard]] OR [[Calendar/TaskNotes/Tasks/Becoming a Consultant - Stern#Obs Dashboard\|Obs Dashboard]] below. |                                                                                                                                                                                            |
| **[[Atlas/CRM/Comp/2026 Consulting Company Map.base\|2026 Consulting Company Map]]**                                                            |                                                                                                                                                                                                   |                                                                                                                                                                                            |
