# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this is

A personal Hugo blog (theme: `tale-hugo`), deployed on Netlify at
https://sntag.netlify.app/. Author: Shayon Tagore.

## Authoring workflow — read this first

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

## The wikilink converter

`scripts/obsidian_to_hugo.py` rewrites `![[path]]` → `![](/web/path)` at build
time only (source keeps the wikilink syntax):

- Strips the `Blog/` vault prefix; maps `static/` and `content/` to the site root.
- Bare filenames (`![[foo.png]]`) are assumed to live under `/images/posts/`.
- `![[foo.png|A caption]]` → caption becomes alt text; size hints like
  `|300` are dropped. Spaces are URL-encoded.
- Idempotent; only touches `content/*.md`.

Wired into the build in two places:
- **`netlify.toml`** runs it before `hugo` (ephemeral checkout — safe).
- **`deploy.sh`** (legacy local build) backs up `content/`, runs the converter,
  builds, then restores `content/` so the working tree — including unpushed
  drafts — is left untouched.

If `![[...]]` ever shows up as literal text on the live site, the converter
didn't run (e.g. `python3` missing from the build image) — check that first.

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

- `content/` — sections: `post/`, `books/`, `tech/`, `about/`. Post filenames
  are dated, e.g. `2020-11-15 -- title.md`.
- `layouts/` — project overrides on top of `themes/tale-hugo/`.
- `scripts/` — `obsidian_to_hugo.py` (above); `update_books_widgets.py`
  regenerates `data/books_widgets.toml` from `content/books/*.md`.
- `config.toml` — Hugo config. Taxonomy is `tags` (not categories). Netlify
  pins `HUGO_VERSION = 0.152.1`.

## Build & deploy

- **Primary:** push to `master` → Netlify builds
  (`python3 scripts/obsidian_to_hugo.py && hugo --gc --minify`).
- **Local preview:** `hugo server`. Hugo may not be installed everywhere;
  don't assume a full build can be run to verify — the converter is unit-tested
  via its cases.

## Conventions

- Work on a feature branch; open a PR into `master` (don't push straight to it).
- Taxonomy is `tags`; there are no `categories`.
