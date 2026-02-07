#!/usr/bin/env python3
"""
update_books_widgets.py

Scans Hugo content files and generates data/books_widgets.toml
with entries for the books-page widgets.

Currently Reading (left widget):
  Pulls from content/books/*.md.
  A book is "currently reading" when its `started` field has a date
  and its `completed` field is empty.

Recommendations (right widget):
  Pulls from content/books/*.md.
  Books are selected when they match at least one of the tags
  listed in RECOMMEND_TAGS below, or all books if the list is empty.

Run from the repo root:
    python3 scripts/update_books_widgets.py

The script is safe to re-run — it overwrites data/books_widgets.toml
each time.
"""

import os
import re
import sys
import textwrap
from pathlib import Path

import yaml

# ─── Configuration ──────────────────────────────────────────────
# Edit these to control which items appear in each widget.

# Currently-Reading widget:
# Set to a list of tag prefixes to additionally filter books.
# e.g. ["books/"] means only books whose tags start with "books/".
# Leave empty ([]) to skip tag filtering — only started/completed matters.
READING_TAG_PREFIXES = []

# Recommendations widget:
# Books with ANY of these tag prefixes (case-insensitive) are included.
# e.g. ["books/fic"] means only books tagged books/fic/... are recommended.
# Set to [] to include ALL books as recommendations.
RECOMMEND_TAG_PREFIXES = []

# ─── Helpers ────────────────────────────────────────────────────

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def find_repo_root():
    """Walk upward from the script location to find the Hugo repo root
    (the directory that contains config.toml)."""
    candidate = Path(__file__).resolve().parent.parent
    if (candidate / "config.toml").exists():
        return candidate
    # Fallback: current working directory
    candidate = Path.cwd()
    if (candidate / "config.toml").exists():
        return candidate
    print("Error: could not find Hugo repo root (no config.toml).", file=sys.stderr)
    sys.exit(1)


def parse_front_matter(filepath):
    """Return a dict of YAML front matter, or None on failure."""
    text = filepath.read_text(encoding="utf-8")
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None


def to_list(val):
    """Ensure a value is a list (handles single strings and None)."""
    if val is None:
        return []
    if isinstance(val, list):
        return val
    return [val]


def has_value(val):
    """Return True if the value is non-empty (not None, not blank string)."""
    if val is None:
        return False
    if isinstance(val, str) and val.strip() == "":
        return False
    return True


def slug_from_filename(filepath):
    """Derive a URL slug from a content filename, matching Hugo conventions."""
    name = filepath.stem.lower()
    # Replace ' -- ' and ' = ' separators, then clean up
    name = re.sub(r"\s*--\s*", "--", name)
    name = re.sub(r"\s*=\s*", "=", name)
    # Replace remaining spaces with hyphens
    name = name.replace(" ", "-")
    return name


def escape_toml_string(s):
    """Escape a string for use in TOML double-quoted values."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


# ─── Collectors ─────────────────────────────────────────────────


def collect_currently_reading(root):
    """Return a list of dicts for books being currently read."""
    books_dir = root / "content" / "books"
    if not books_dir.exists():
        return []

    results = []
    for md in sorted(books_dir.glob("*.md")):
        fm = parse_front_matter(md)
        if fm is None:
            continue

        started = fm.get("started")
        completed = fm.get("completed")

        # Must have started but not completed
        if not has_value(started) or has_value(completed):
            continue

        # Optional tag-prefix filter
        if READING_TAG_PREFIXES:
            tags = to_list(fm.get("tags"))
            if not any(
                t.startswith(prefix)
                for t in tags
                for prefix in READING_TAG_PREFIXES
            ):
                continue

        cover = fm.get("cover", "")
        authors = to_list(fm.get("author"))

        results.append({
            "title": fm.get("title", md.stem),
            "author": ", ".join(authors) if authors else "Unknown",
            "cover": cover,
            "format": "book",  # default; override manually for audiobooks
        })

    return results


def collect_recommendations(root):
    """Return a list of dicts for recommended books (links to book pages)."""
    books_dir = root / "content" / "books"
    if not books_dir.exists():
        return []

    results = []
    filter_prefixes = [p.lower() for p in RECOMMEND_TAG_PREFIXES]

    for md in sorted(books_dir.glob("*.md")):
        if md.name == "_index.md":
            continue

        fm = parse_front_matter(md)
        if fm is None:
            continue

        # Optional tag-prefix filter
        if filter_prefixes:
            tags = [t.lower() for t in to_list(fm.get("tags"))]
            if not any(
                t.startswith(prefix)
                for t in tags
                for prefix in filter_prefixes
            ):
                continue

        title = fm.get("title", md.stem)
        slug = slug_from_filename(md)
        url = f"/books/{slug}/"

        results.append({"title": title, "url": url})

    return results


# ─── Output ─────────────────────────────────────────────────────


def write_toml(root, reading, recommendations):
    """Write data/books_widgets.toml."""
    out = root / "data" / "books_widgets.toml"
    out.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append("# Auto-generated by scripts/update_books_widgets.py")
    lines.append("# Re-run the script to refresh. Manual edits will be overwritten.")
    lines.append("")

    # ── Currently reading ──
    lines.append("# ── Currently Reading / Listening ──")
    if not reading:
        lines.append("# (no books matched — set a 'started' date in front matter)")
    for entry in reading:
        lines.append("")
        lines.append("[[currently_reading]]")
        lines.append(f'title  = "{escape_toml_string(entry["title"])}"')
        lines.append(f'author = "{escape_toml_string(entry["author"])}"')
        lines.append(f'cover  = "{escape_toml_string(entry["cover"])}"')
        lines.append(f'format = "{entry["format"]}"')

    lines.append("")
    lines.append("# ── Recommendations ──")
    if not recommendations:
        lines.append("# (no books matched the tag filter)")
    for entry in recommendations:
        lines.append("")
        lines.append("[[recommendations]]")
        lines.append(f'title = "{escape_toml_string(entry["title"])}"')
        lines.append(f'url   = "{escape_toml_string(entry["url"])}"')

    lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


# ─── Main ───────────────────────────────────────────────────────


def main():
    root = find_repo_root()
    print(f"Repo root: {root}")

    reading = collect_currently_reading(root)
    print(f"Currently reading: {len(reading)} book(s)")
    for r in reading:
        print(f"  - {r['title']} ({r['format']})")

    recommendations = collect_recommendations(root)
    print(f"Recommendations:  {len(recommendations)} book(s)")
    for r in recommendations:
        print(f"  - {r['title']}  ->  {r['url']}")

    out_path = write_toml(root, reading, recommendations)
    print(f"\nWritten to {out_path}")

    if not reading:
        print(
            textwrap.dedent("""\

            Hint: no books are marked as "currently reading".
            To fix this, add a date to the 'started' field in a book's
            front matter (and leave 'completed' empty):

                started: 2025-01-15
                completed:
            """)
        )


if __name__ == "__main__":
    main()
