---
title: Base Builder Widget Test
added date: 2026-11-04, 9:04:18 am
modified date: 2026-11-06, 11:23:43 am
---

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

## Built-in Default Base

Empty body ⇒ the widget's built-in default base (name / tag / path / sort):

{{< base-builder >}}{{< /base-builder >}}

## A Custom Pasted Base

A different base pasted straight into the post — an `or` filter, custom
columns, and several tokens (note how each token's `help=` becomes the `?`
tooltip):

{{< base-builder notes="crm-sample" >}}
views:
  - type: table
    name: ${name | label=View name | help=Shown as the tab in Obsidian | default=Strategy shops}
    filters:
      or:
        - file.tags.contains("${tag1 | label=Tag A | help=First tag to include; no leading # | default=strategy}")
        - file.tags.contains("${tag2 | label=Tag B | help=Second tag to include; no leading # | default=boutique}")
    order:
      - file.name
      - tags
      - summary
      - source
    sort:
      - property: file.name
        direction: ${dir | label=Sort direction | help=ASC or DESC | options=ASC,DESC | default=ASC}
{{< /base-builder >}}

## A Custom Pasted Base 2

A different base pasted straight into the post — an `or` filter, custom
columns, and several tokens (note how each token's `help=` becomes the `?`
tooltip):

{{< base-builder notes="crm-sample" >}}
views:
  - type: table
    name: ${name | label=View name | help=Shown as the tab in Obsidian | default=Events & Recruiting Tracker}
    filters:
      and:
        - file.path.startsWith("${path | label=Folder path prefix | help=Only notes under this folder; end with a slash | default=Calendar/}")
        - or:
            - file.tags.contains("${tag1 | label=tag 1 | help=First tag to include; no leading # | default=recruiting}")
            - file.tags.contains("${tag2 | label=tag 2 | help=Second tag to include; no leading # | default=coffee-chat}")
            - file.tags.contains("${tag3 | label=tag 3 | help=Third tag to include; no leading # | default=corporate-presentation}")
            - file.tags.contains("${tag4 | label=tag 4 | help=Fourth tag to include; no leading # | default=event}")
        - and:
            - note["ics event start"] > "${after | label=Events after | help=Earliest event start, YYYY-MM-DD | default=2026-06-01}"
            - note["ics event start"] < "${before | label=Events before | help=Latest event start, YYYY-MM-DD | default=2028-06-01}"
            - note["Obs type"] == "${type | label=Obs type | help=Only notes whose Obs type is this | default=ICS}"
    order:
      - file.name
      - projects
      - ics event start
      - summary
      - to do
      - completed
      - tags
    sort:
      - property: ics event start
        direction: ${dir | label=Sort direction | help=ASC or DESC | options=ASC,DESC | default=ASC}
{{< /base-builder >}}
