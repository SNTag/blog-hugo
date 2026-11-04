+++
title = "Base Builder Widget Test"
date = 2026-11-03
draft = true
tags = ["obsidian", "test"]
+++

A scratch page for testing the `base-builder` shortcode. It is marked
`draft = true`, so it never ships to the live site — preview it locally with
`hugo server -D`.

<!--more-->

## Default example

{{< base-builder >}}

## With custom defaults

Same example notes, a different starting filter (tag `strategy`):

{{< base-builder name="Strategy Shops" path="Atlas/CRM/Comp/" tag="strategy" notes="crm-sample" >}}
