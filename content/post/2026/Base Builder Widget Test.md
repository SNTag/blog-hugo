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

## Built-in default base

Empty body ⇒ the widget's built-in default base (name / tag / path / sort):

{{< base-builder >}}{{< /base-builder >}}

## A custom pasted base

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
