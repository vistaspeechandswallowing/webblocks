#!/usr/bin/env python3
"""Print a file the way it should be PASTED into Squarespace: no repo comments.

    python3 tools/paste.py pages/contact.html            # to the terminal
    python3 tools/paste.py pages/contact.html | pbcopy   # straight to clipboard

Why: the comments in these files are written for whoever edits them next — why a
band is last, which string must not change, what breaks if it moves. That is
worth keeping in the repo and worth nothing to a visitor, who downloads every
byte of it on every page view. Pasting the raw file shipped several KB of notes
(including internal file paths) into the live page.

So: keep writing comments freely in the source files, and paste THIS output
instead. One short marker line survives, naming the file and the commit it came
from, so it's possible to tell what's actually deployed:

    <!-- vss: pages/contact.html @ a1b2c3d -->

Comments inside <script> and <style> are left alone — only HTML comments in the
markup are removed. Nothing else is touched: no minifying, no reformatting, no
clever whitespace collapsing. The output is the same HTML with the notes gone.
"""
import os
import re
import subprocess
import sys

# <script>…</script> and <style>…</style> are copied through untouched.
#
# These are scanned STRICTLY LEFT TO RIGHT, taking whichever of the two starts
# first, because either can be mentioned inside the other. The comment headers
# in these files talk ABOUT script tags ("paste the <script> tag below"), and
# matching script regions first would treat that prose as the start of a real
# script and protect everything up to the next </script> — which is exactly the
# comment we came to remove. First match wins is the only reading that works.
NEXT = re.compile(r"<!--|<(?P<tag>script|style)\b[^>]*>", re.I)
COMMENT_END = re.compile(r"-->")


def revision():
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True,
            cwd=os.path.dirname(os.path.abspath(__file__)))
        revision = out.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"
    dirty = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))).stdout.strip()
    return revision + ("-modified" if dirty else "")


def strip_comments(source):
    """Remove HTML comments, leaving <script> and <style> contents alone."""
    out, i = [], 0
    while i < len(source):
        match = NEXT.search(source, i)
        if not match:
            out.append(source[i:])
            break
        out.append(source[i:match.start()])

        if match.group(0).startswith("<!--"):
            end = COMMENT_END.search(source, match.end())
            # An unterminated comment would otherwise swallow the rest of the
            # file silently. Keep it and let the author see it.
            if not end:
                out.append(source[match.start():])
                break
            i = end.end()                       # drop the comment entirely
        else:
            close = re.compile(r"</%s\s*>" % match.group("tag"), re.I)
            end = close.search(source, match.end())
            stop = end.end() if end else len(source)
            out.append(source[match.start():stop])   # keep it verbatim
            i = stop
    return "".join(out)


def tidy(text):
    """Close up the holes the comments left behind."""
    text = "\n".join(line.rstrip() for line in text.splitlines())
    text = re.sub(r"\n{3,}", "\n\n", text)     # no run of blank lines
    return text.strip("\n")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__.strip().splitlines()[0] + "\n\nusage: "
                 "python3 tools/paste.py <file>")
    path = sys.argv[1]
    source = open(path).read()
    output = tidy(strip_comments(source))

    root = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True,
                          cwd=os.path.dirname(os.path.abspath(path)) or ".")
    name = os.path.relpath(os.path.abspath(path), root.stdout.strip()) \
        if root.returncode == 0 else os.path.basename(path)

    print(f"<!-- vss: {name} @ {revision()} -->")
    print(output)

    saved = len(source) - len(output)
    sys.stderr.write(
        f"{name}: {len(source):,} → {len(output):,} bytes "
        f"({saved:,} of comments removed)\n")


if __name__ == "__main__":
    main()
