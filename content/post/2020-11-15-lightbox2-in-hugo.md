---
title: "Lightbox2 in hugo"
author: "SNTag"
date: "2020-11-15T00:00:00Z"
layout: post
categories:
  - hugo
  - shortcodes
  - lightbox2
  - photography
---

This is a quick run-down of how I set up [lightbox2](https://lokeshdhakar.com/projects/lightbox2/) for my hugo site. To be honest, it is my personal documentation to the [shortcode written by Julian Stier in his blog-post about lightbox2](https://julianstier.com/posts/2020/03/hugo-and-lightbox/). His post helped me deal with a number of problems using lightbox2 with hugo when the [main lightbox2 tutorial had failed me](https://lokeshdhakar.com/projects/lightbox2/). This will be a post under constant development as I work out lightbox2 and to remind myself how to implement it.

# Setup

## Preparing the directories and files

The first step is to prepare the main hugo directory. If it is not there already, generate the directory `/static/css/` and `/static/js/`.

Download the latest [github release](https://github.com/lokesh/lightbox2/releases). Unzip where you want. The important detail is extracting from the lightbox2 release the file `/dist/css/lightbox.css` into `/static/css/`.

If your hugo site does not have jquery, extract from the lightbox2 release the file `dist/js/lightbox-plus-jquery.css` into `/static/js/`.

## Modifying the html

The exact details of this bit can change depending on your hugo setup. The main concept is that you have to find the files with the \<head\> \& \<body\> tags. In the head section, add `<link rel="stylesheet" href="/css/lightbox.css">`. In the body section, add `<script src="/js/lightbox-plus-jquery.js"></script>`.

## Shortcode: figure

The shortcode was taken directly from [Julian Stier's blog post on his lightbox2 implementation](https://julianstier.com/posts/2020/03/hugo-and-lightbox/). This was put under `/layouts/shortcodes/figure.html`.


# Implementation

## Single images

The shortcode written by [Julian Stier](https://julianstier.com/posts/2020/03/hugo-and-lightbox/) has the option for:

- src : Where the image is
- class : where. floating.
- caption : caption

\{\{\< figure class="floatright" src="../../photos/DSLR-timelapse/2020-10-25_16-28.png" caption="A random image from my gallery" \>\}\}

{{< figure class="floatright" src="../../photos/DSLR-timelapse/2020-10-25_16-28.png" caption="A random image from my gallery" >}}

## Gallery

Work in progress.

Followed the guide posted by [Christian Specht](https://christianspecht.de/2020/08/10/creating-an-image-gallery-with-hugo-and-lightbox2/).

My version of his can be found
[here](https://github.com/SNTag/blog-hugo/blob/master/layouts/shortcodes/gallery2.html). It will
display the first image as regular sized, and the rest in a minimized thumbnail. Depends on images being locally hosted in a repository. Anything outside using a CDN for example requires third-party intervention.

# Setting up a CDN

CDN - Content Delivery Network. An important feature to have in a large-scale gallery. This website
is currently hosted on github. [Needs an alternative](https://www.reddit.com/r/gohugo/comments/jxv2vq/making_my_own_instagram_in_hugo/) to accommodate the large number of files I expect
to display in the future.

Some options as I have seen are Netlify's LFS (not many good tutorials), cloudinary, Blackblaze B2+Cloudflare, or a personal VPS. I'm currently attempting cloudinary after having tried Netlify's LFS.

## Netlify's LFS

I will admit that it sounds great, but I have encountered a number of challenges in getting it to work. there are unfortunately limited tutorials on the topic.

## Cloudinary

[cloudinary](https://cloudinary.com/pricing) has a free tier with 25GB of storage and/or
bandwitdth. This should be enough for the time being. It has a number of useful
image-transformations which are done by modifying [the URL
itself](https://cloudinary.com/documentation/image_transformations). It has been very satisfactory
to use so far. I expect it will give me a decent bit of breathing room. Unfortunately,
the next tier up is about [100$ per year](https://cloudinary.com/pricing). It may be cheaper for some to host their site on a VPS.

# References

1. Figure shortcode and getting me to understand lightbox:

[Julian Stier: Adding lightbox to Hugo](https://julianstier.com/posts/2020/03/hugo-and-lightbox/)


2. Adding gallery option:

[Christian Specht: Creating an image gallery with Hugo and Lightbox2](https://christianspecht.de/2020/08/10/creating-an-image-gallery-with-hugo-and-lightbox2/)
