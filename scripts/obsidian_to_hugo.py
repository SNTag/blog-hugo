#!/usr/bin/env python3
"""
obsidian_to_hugo.py

Build-time converter for Obsidian syntax that Hugo/Goldmark doesn't understand:

1. Image embeds
       ![[path/to/image.png]]  ->  ![](/images/posts/image.png)
   so the existing layouts/_default/_markup/render-image.html hook can style them.

2. Note links (wikilinks)
       [[Blog/content/post/2026/Auto-Script Runner|Auto-Script Runner]]
       ->  [Auto-Script Runner]({{< relref "post/2026/Auto-Script Runner.md" >}})
   Hugo's relref resolves the real URL (and fails the build if it can't).
   Links that point outside the site (Calendar/, Efforts/, .base files, drafts,
   missing pages) are rendered as just their alias text -- never raw brackets.
   Links to files under Blog/static/ become plain links to that file.

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
- Idempotent: a second run finds no `[[ ]]` / `![[ ]]` and changes nothing.
- Only touches Markdown (.md) files; .html content is passed through by Hugo
  untouched anyway.
- Front matter, fenced code blocks and inline `code` are left untouched, so
  things like R's `x[[i]]` or `bookshelf: "[[2026 Books]]"` survive.
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


# --------------------------------------------------------------------------
# Note links: [[target]], [[target|alias]], [[target#Heading|alias]]
# --------------------------------------------------------------------------

# A wikilink NOT preceded by "!" (those are embeds, handled above).
WIKILINK = re.compile(r"(?<!!)\[\[([^\[\]\n]+?)\]\]")

# Split "target|alias" on the first pipe, allowing Obsidian's table-escaped "\|".
ALIAS_SPLIT = re.compile(r"\\?\|")

DRAFT_RE = re.compile(r"^draft:\s*(true|yes)\s*$", re.IGNORECASE | re.MULTILINE)


def anchorize(heading: str) -> str:
    """Mirror Hugo's default (GitHub-style) heading IDs."""
    h = heading.strip().lower()
    h = re.sub(r"[^\w\- ]", "", h)  # drop punctuation; keep letters/digits/_/-/space
    return h.replace(" ", "-")


class PageIndex:
    """Published Markdown pages under content/, keyed for link resolution."""

    def __init__(self, content: Path):
        self.by_path = {}   # "post/2026/auto-script runner" -> "post/2026/Auto-Script Runner.md"
        self.by_name = {}   # "auto-script runner" -> [rel paths]
        for md in content.rglob("*.md"):
            rel = md.relative_to(content).as_posix()
            try:
                if DRAFT_RE.search(split_front_matter(md.read_text(encoding="utf-8"))[0]):
                    continue  # drafts aren't built in production; don't link to them
            except OSError:
                continue
            stem = rel[:-3]
            keys = [stem]
            # Bundles: "about/index.md" / "TagOS/_index.md" answer to "about" / "TagOS".
            for suffix in ("/index", "/_index"):
                if stem.endswith(suffix):
                    keys.append(stem[: -len(suffix)])
            for k in keys:
                self.by_path[k.lower()] = rel
                self.by_name.setdefault(k.rsplit("/", 1)[-1].lower(), []).append(rel)

    def resolve(self, target: str):
        """Return the content-relative .md path for a link target, or None."""
        t = target.strip().replace("\\", "/")
        if t.lower().endswith(".md"):
            t = t[:-3]
        if t.startswith(VAULT_PREFIX):
            t = t[len(VAULT_PREFIX):]
            if not t.startswith("content/"):
                return None
            return self.by_path.get(t[len("content/"):].lower())
        if "/" in t:
            return None  # a vault path outside Blog/ (Calendar/, Efforts/, ...)
        matches = self.by_name.get(t.lower(), [])
        return matches[0] if len(matches) == 1 else None


def static_file_url(target: str):
    """[[Blog/static/resources/x.pdf]] -> /resources/x.pdf ; else None."""
    t = target.strip().replace("\\", "/")
    if t.startswith(VAULT_PREFIX + "static/"):
        return normalize_path(t)
    return None


def make_link_converter(index: PageIndex, unresolved: list):
    def convert_link(match: re.Match) -> str:
        inner = match.group(1)
        parts = ALIAS_SPLIT.split(inner, 1)
        target = parts[0].strip()
        alias = parts[1].strip() if len(parts) > 1 else ""

        heading = ""
        if "#" in target:
            target, heading = target.split("#", 1)
            target = target.strip()
            heading = heading.strip()
        if heading.startswith("^"):
            heading = ""  # block references have no web equivalent

        if not alias:
            name = target.rsplit("/", 1)[-1] if target else ""
            if name.lower().endswith(".md"):
                name = name[:-3]
            alias = f"{name} > {heading}" if name and heading else (name or heading)

        # Same-page heading link: [[#Heading]]
        if not target:
            return f"[{alias}](#{anchorize(heading)})" if heading else alias

        url = static_file_url(target)
        if url:
            return f"[{alias}]({url})"

        rel = index.resolve(target)
        if rel is None:
            unresolved.append(inner)
            return alias

        ref = rel + (f"#{anchorize(heading)}" if heading else "")
        return f'[{alias}]({{{{< relref "{ref}" >}}}})'

    return convert_link


# --------------------------------------------------------------------------
# Text processing that skips front matter and code
# --------------------------------------------------------------------------

FRONT_MATTER = re.compile(r"\A---[ \t]*\n.*?\n---[ \t]*(\n|\Z)", re.DOTALL)
FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,})")
INLINE_CODE = re.compile(r"(`+)(?:(?!\1)[\s\S])+?\1")


def split_front_matter(text: str):
    m = FRONT_MATTER.match(text)
    return (text[: m.end()], text[m.end():]) if m else ("", text)


def convert_prose(text: str, convert_link) -> str:
    """Convert embeds + links in a chunk of non-fenced text, skipping `code`."""
    out, pos = [], 0
    for m in INLINE_CODE.finditer(text):
        out.append(_convert_plain(text[pos:m.start()], convert_link))
        out.append(m.group(0))
        pos = m.end()
    out.append(_convert_plain(text[pos:], convert_link))
    return "".join(out)


def _convert_plain(text: str, convert_link) -> str:
    text = WIKILINK_EMBED.sub(convert_embed, text)
    if convert_link is not None:
        text = WIKILINK.sub(convert_link, text)
    return text


def convert_text(text: str, convert_link=None) -> str:
    front, body = split_front_matter(text)
    out, prose, fence = [], [], None
    for line in body.splitlines(keepends=True):
        m = FENCE.match(line)
        if fence is None:
            if m:
                out.append(convert_prose("".join(prose), convert_link))
                prose = []
                fence = m.group(1)
                out.append(line)
            else:
                prose.append(line)
        else:
            out.append(line)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) \
                    and not line.strip()[len(m.group(1)):].strip():
                fence = None
    out.append(convert_prose("".join(prose), convert_link))
    return front + "".join(out)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    content = root / CONTENT_DIR
    if not content.is_dir():
        print(f"obsidian_to_hugo: no {CONTENT_DIR}/ dir at {content}", file=sys.stderr)
        return 1

    # Build the page index BEFORE rewriting anything.
    index = PageIndex(content)

    changed = 0
    for md in content.rglob("*.md"):
        original = md.read_text(encoding="utf-8")
        unresolved = []
        converted = convert_text(original, make_link_converter(index, unresolved))
        if converted != original:
            md.write_text(converted, encoding="utf-8")
            changed += 1
            print(f"obsidian_to_hugo: rewrote {md.relative_to(root)}")
        for link in unresolved:
            print(f"obsidian_to_hugo:   not on site, rendered as text: [[{link}]]")

    print(f"obsidian_to_hugo: {changed} file(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
