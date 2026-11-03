---
title: CLAUDE
added date: 2026-09-01, 1:18:43 pm
modified date: 2026-09-01, 2:00:48 pm
---

# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What This is

A personal Hugo blog (theme: `tale-hugo`), deployed on Netlify at
https://sntag.netlify.app/. Author: Shayon Tagore.

## Authoring Workflow — Read This First

Posts are written in **Obsidian**, and this git repo is a subfolder named
`Blog/` inside a larger Obsidian vault. That has two consequences that trip
up naive edits:

1. **Obsidian writes paths relative to the vault root**, so image embeds look
   like `Blog/static/images/posts/foo.png`. Inside the repo the root *is*
   `Blog/`, so the real web path is `/images/posts/foo.png`.
2. **Posts use Obsidian wikilink image embeds:** `![[foo.png]]`. Hugo/Goldmark
   does **not** parse these — left alone they render as literal text on the
   page.

Both are handled automatically by a build-time converter (below). Keep the
wikilink syntax in source; do not "fix" `![[...]]` into Markdown by hand.

## The Wikilink Converter

`scripts/obsidian_to_hugo.py` rewrites Obsidian syntax at build time only
(source keeps the wikilink syntax). It skips front matter, fenced code blocks
and inline `code`.

**Image embeds** — `![[path]]` → `![](/web/path)`:

- Strips the `Blog/` vault prefix; maps `static/` and `content/` to the site root.
- Bare filenames (`![[foo.png]]`) are assumed to live under `/images/posts/`.
- `![[foo.png|A caption]]` → caption becomes alt text; size hints like
  `|300` are dropped. Spaces are URL-encoded.

**Note links** — `[[target#Heading|Alias]]`:

- Obsidian writes vault-absolute paths, e.g.
  `[[Blog/content/post/2026/Auto-Script Runner|Auto-Script Runner]]`. The
  converter strips `Blog/content/`, checks the page exists under `content/`,
  and emits `[Alias]({{< relref "post/2026/Auto-Script Runner.md" >}})` —
  Hugo then computes the real URL. Bare names (`[[Auto-Script Runner]]`)
  resolve by filename when unique.
- `#Heading` → GitHub-style anchor (`#events--recruiting-tracker`), matching
  Hugo's heading IDs. `[[#Heading]]` links within the page. `#^block` refs
  are dropped.
- `[[Blog/static/…]]` (e.g. a PDF) → a plain link to that file.
- Anything else — paths outside `Blog/` (`Calendar/`, `Efforts/`, `Atlas/`),
  `.base` files, drafts, missing pages — renders as just the alias text and
  is listed in the build log as `not on site, rendered as text`.
- Handles Obsidian's table-escaped pipe `\|`.
- Idempotent; only touches `content/*.md`.

Wired into the build in two places:
- **`netlify.toml`** runs it before `hugo` (ephemeral checkout — safe).
- **`deploy.sh`** (legacy local build) backs up `content/`, runs the converter,
  builds, then restores `content/` so the working tree — including unpushed
  drafts — is left untouched.

If `![[...]]` ever shows up as literal text on the live site, the converter
didn't run (e.g. `python3` missing from the build image) — check that first.

## Callouts

Obsidian callouts (`> [!note] Title`, `> [!tip]-` folded, `> [!tip]+` open)
are rendered by Hugo's blockquote render hook,
`layouts/_default/_markup/render-blockquote.html`, styled by
`assets/css/callouts.css`. Obsidian's aliases (caution, error, faq, …) map to
the base types. `> [!quote] Author` keeps the normal centered quote style and
shows the title as the attribution. Plain `>` blockquotes are unchanged.

## Images

| Purpose | Store in | Referenced as |
|---|---|---|
| Post images | `static/images/posts/` | `/images/posts/…` |
| Header art | `static/images/header/` | `/images/header/…` |
| Profile | `static/images/profile/` | `/images/profile/…` |
| Photo galleries | `static/photos/…` | `/photos/…` |

`static/` is copied verbatim to the site root. `assets/` is the Hugo Pipes
pipeline (SCSS/JS) — **not** for content images. Prefer hyphenated filenames
without spaces (`stern-announcement.png`), matching existing files.

Standalone images are styled by `layouts/_default/_markup/render-image.html`
(a lightbox figure via glightbox). It also normalizes leading slashes and
`content/` prefixes.

## Structure

- `content/` — sections: `post/`, `books/`, `about/`, `TagOS/`, and
  `mba-recruiting/`. All blog
  posts (including tech/TagOS ones) live under `content/post/YYYY/` — do not
  create a separate top-level section directory for them.
- **The `TagOS` "section" is virtual.** `content/TagOS/` holds only an
  `_index.md`; it has no posts of its own. A post appears under `/TagOS/` when
  its frontmatter carries `Obs Category: TagOS` (set in Obsidian). The listing
  is built by `layouts/TagOS/list.html`, which scans all posts for that key.
  Note Hugo lowercases frontmatter keys, so it's read as `index .Params
  "obs category"` (with a space), not `.Params.obs_category`.
- **`mba-recruiting` is virtual the same way:** `content/mba-recruiting/` holds
  only an `_index.md`; posts with `Obs Category: MBA Recruiting` are listed by
  `layouts/mba-recruiting/list.html`.
- **Header nav dropdowns:** a `[[menu.main]]` entry with `parent = "<id>"` in
  `config.toml` shows in that parent's dropdown (`layouts/partials/header-menu.html`,
  styles in `layouts/partials/head.html`). A parent with no `url` is a plain
  label that only opens the menu.
- `layouts/` — project overrides on top of `themes/tale-hugo/`.
- `scripts/` — `obsidian_to_hugo.py` (above); `update_books_widgets.py`
  regenerates `data/books_widgets.toml` from `content/books/*.md`.
- `config.toml` — Hugo config. Taxonomy is `tags` (not categories). Netlify
  pins `HUGO_VERSION = 0.152.1`.

## Build & Deploy

- **Primary:** push to `master` → Netlify builds
  (`python3 scripts/obsidian_to_hugo.py && hugo --gc --minify`).
- **Local preview:** `hugo server`.
- **Claude Code on the web:** a `SessionStart` hook
  (`.claude/hooks/session-start.sh`, wired via `.claude/settings.json`)
  installs Hugo extended v0.152.1 — the same version Netlify pins — into
  `~/.hugo` and puts it on `PATH`, so `hugo` / `hugo server` and a full
  `hugo --gc --minify` build are available to verify changes. The hook is
  remote-only (gated on `$CLAUDE_CODE_REMOTE`) and idempotent; bump its
  `HUGO_VERSION` in lockstep with `netlify.toml` if the pin changes. Note the
  theme lives in a git submodule, so a full build needs
  `git submodule update --init --recursive themes/tale-hugo` first.
- There is no automated test suite or linter; the wikilink converter is
  covered informally by its own cases.

## Conventions

- Work on a feature branch; open a PR into `master` (don't push straight to it).
- Taxonomy is `tags`; there are no `categories`.

## Future Directions (not started)

Ideas discussed but deliberately deferred. Pick up when working on the MBA
Recruiting pages.

- **Publishing link targets.** Note links now work (see the converter), but
  most links in `content/post/2026/How I Setup an MBA Tracker in Obsidian.md`
  point outside `Blog/` (`Calendar/`, `Efforts/`, `Atlas/`) or at `.base`
  files (Obsidian Bases — no web equivalent), so they render as text. Making
  them live means publishing those notes under `content/`, or a table
  snapshot of each Base, case by case; some are private (CRM, contacts).
- **Obsidian-style link graph on the MBA Recruiting page.** Have the
  converter also emit page→page link data (e.g. a JSON file),
  then draw it with a force-graph JS library (d3 / force-graph) on
  `layouts/mba-recruiting/list.html`, following light/dark mode. Open
  questions: show unpublished targets as grey nodes or hide them; scope to MBA
  posts only or include linked posts from other sections.
