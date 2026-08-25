#!/usr/bin/env python3
"""
obsidian_to_hugo.py

Build-time converter: rewrites Obsidian-style embedded wikilinks
    ![[path/to/image.png]]
into standard Markdown images that Hugo/Goldmark understands
    ![](/images/posts/image.png)
so the existing layouts/_default/_markup/render-image.html hook can style them.

Why this exists
---------------
Hugo's Goldmark parser does NOT understand `![[ ... ]]` embeds, so they render
as literal text on the page. This lets you keep authoring image embeds with
Obsidian wikilink syntax while still producing a working site.

Vault vs. repo root
-------------------
The site lives inside an Obsidian vault subfolder named `Blog/`, so Obsidian
emits paths relative to the VAULT root, e.g.
    Blog/static/images/posts/Stern Announcement.png
Inside the git repo, the repo root *is* `Blog/`, and everything in `static/`
is served from the site root. So we strip the `Blog/` vault prefix and map
`static/...` -> `/...`.

Run from the repo root:
    python3 scripts/obsidian_to_hugo.py

Notes
-----
- Operates IN PLACE on files under content/. Intended to run against an
  ephemeral build checkout (Netlify). Your committed source keeps the
  wikilink syntax, so your Obsidian workflow is unchanged.
- Idempotent: a second run finds no `![[ ]]` and changes nothing.
- Only touches Markdown (.md) files; .html content is passed through by Hugo
  untouched anyway.
"""

import re
import sys
import urllib.parse
from pathlib import Path

# Directory (relative to repo root) whose Markdown files are scanned.
CONTENT_DIR = "content"

# The Obsidian vault subfolder that contains the Hugo site. Paths that Obsidian
# writes are relative to the vault root, so this leading segment is stripped.
VAULT_PREFIX = "Blog/"

# Where bare-filename embeds (e.g. ![[image.png]]) are assumed to live.
DEFAULT_IMAGE_DIR = "/images/posts/"

# Matches ![[ inner ]] . Inner is captured lazily and may contain an alias
# after a pipe:  ![[path|alt or size]]
WIKILINK_EMBED = re.compile(r"!\[\[\s*([^\]]+?)\s*\]\]")

# An alias that is purely a size hint (Obsidian: ![[img.png|300]] or |300x200)
SIZE_ALIAS = re.compile(r"^\d+(x\d+)?$")


def normalize_path(raw: str) -> str:
    """Turn a vault-relative embed target into a site-absolute web path."""
    p = raw.strip().replace("\\", "/")

    # Leave external URLs and protocol-relative URLs alone.
    if re.match(r"^(https?:)?//", p):
        return p

    # Strip the vault-root subfolder ("Blog/") if Obsidian included it.
    if p.startswith(VAULT_PREFIX):
        p = p[len(VAULT_PREFIX):]

    # static/... is served from the site root -> drop the "static" segment.
    if p.startswith("static/"):
        p = "/" + p[len("static/"):]
    # content/... resources map to the site root too (matches render-image.html).
    elif p.startswith("content/"):
        p = "/" + p[len("content/"):]
    elif p.startswith("/"):
        pass  # already absolute
    elif "/" in p:
        # Some other repo-relative path; make it absolute from the site root.
        p = "/" + p
    else:
        # Bare filename -> assume the posts image folder.
        p = DEFAULT_IMAGE_DIR + p

    # Collapse any accidental double slashes (but keep a single leading slash).
    p = re.sub(r"/{2,}", "/", p)

    # URL-encode spaces and other unsafe chars in the path portion only,
    # preserving the slashes.
    p = urllib.parse.quote(p, safe="/%")
    return p


def convert_embed(match: re.Match) -> str:
    inner = match.group(1)
    alt = ""
    target = inner
    if "|" in inner:
        target, alias = inner.split("|", 1)
        alias = alias.strip()
        # Ignore size hints like |300 ; use anything else as alt text.
        if alias and not SIZE_ALIAS.match(alias):
            alt = alias
    return f"![{alt}]({normalize_path(target)})"


def convert_text(text: str) -> str:
    return WIKILINK_EMBED.sub(convert_embed, text)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    content = root / CONTENT_DIR
    if not content.is_dir():
        print(f"obsidian_to_hugo: no {CONTENT_DIR}/ dir at {content}", file=sys.stderr)
        return 1

    changed = 0
    for md in content.rglob("*.md"):
        original = md.read_text(encoding="utf-8")
        converted = convert_text(original)
        if converted != original:
            md.write_text(converted, encoding="utf-8")
            changed += 1
            print(f"obsidian_to_hugo: rewrote {md.relative_to(root)}")

    print(f"obsidian_to_hugo: {changed} file(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
