---
title: Outline of my MBA Recruiting Bases
added date: 2026-11-03, 7:23:23 pm
modified date: 2026-11-06, 11:19:18 am
---

> [!note] Home to future widgets both describing a specific base used in my MBA recruiting, and allowing custom creation of each base.

# Events & Recruiting Tracker

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

# Applications

# Interviews

# Case Tracker

# 2026 Consulting Company Map
