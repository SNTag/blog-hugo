#!/bin/bash
# SessionStart hook: install the pinned Hugo (extended) so Claude Code on the
# web can run `hugo` / `hugo server` and verify builds. Netlify pins the same
# version via HUGO_VERSION in netlify.toml -- keep the two in sync.
set -euo pipefail

# Web sessions only. Locally the author already has their own Hugo/Obsidian
# toolchain, so leave that environment untouched.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

HUGO_VERSION="0.152.1"
HUGO_DIR="$HOME/.hugo"
HUGO_BIN="$HUGO_DIR/hugo"

# Map uname -> Hugo's release naming.
case "$(uname -m)" in
  x86_64|amd64) HUGO_ARCH="amd64" ;;
  aarch64|arm64) HUGO_ARCH="arm64" ;;
  *) echo "session-start: unsupported arch $(uname -m); skipping Hugo install" >&2; exit 0 ;;
esac

# Idempotent: only download if the correct version isn't already present
# (the container caches after the hook completes).
if ! "$HUGO_BIN" version 2>/dev/null | grep -q "v${HUGO_VERSION}"; then
  echo "session-start: installing Hugo extended v${HUGO_VERSION} (${HUGO_ARCH})..." >&2
  mkdir -p "$HUGO_DIR"
  url="https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-${HUGO_ARCH}.tar.gz"
  curl -fsSL "$url" | tar -xz -C "$HUGO_DIR" hugo
  echo "session-start: Hugo installed -> $HUGO_BIN" >&2
else
  echo "session-start: Hugo v${HUGO_VERSION} already present, skipping download" >&2
fi

# Persist Hugo on PATH for the rest of the session.
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export PATH=\"$HUGO_DIR:\$PATH\"" >> "$CLAUDE_ENV_FILE"
fi
