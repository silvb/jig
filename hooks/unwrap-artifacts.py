#!/usr/bin/env python3
"""Unwrap hard-wrapped prose in jig planning artifacts.

The artifacts are read in an editor, a pager, or a diff viewer, and every one of
those wraps text on its own. A hard wrap on top of that buys nothing and costs
the thing the artifacts exist for: a one-word change re-flows the paragraph, so
the diff shows five changed lines instead of one, and a human reviewing a plan
revision by reading the diff is the whole design.

So paragraphs and list items collapse to one line each. Everything that carries
meaning in its line breaks — fenced blocks, tables, headings, frontmatter — is
copied through untouched, because the drawings are the dense part of these
documents and re-flowing a sequence diagram would destroy it.

Runs as a PostToolUse hook on Write and Edit, scoped to docs/plans/. It fails
open: any error at all, exit quietly and leave the file alone. A formatter that
can break the session is worse than a hard wrap.
"""

import json
import re
import sys

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
LIST = re.compile(r"^ {0,3}(?:[-*+]|\d{1,9}[.)])(?:\s|$)")

# Lines that are their own block: joining one into a paragraph changes what it
# means, or joining a paragraph into one silently deletes a heading.
ATOMIC = re.compile(
    r"""
      ^\ {0,3}\#                        # ATX heading
    | ^\ {0,3}>                         # blockquote
    | ^\ {0,3}\|                        # table row
    | ^\ {0,3}(?:-{2,}|={1,}|\*{3,}|_{3,})\s*$   # setext underline, thematic break
    | ^\ {0,3}<                         # raw HTML
    | ^\ {0,3}\[[^\]]+\]:               # link reference definition
    | ^(?:\ {4,}|\t)                    # indented code, or a continuation deep
                                        # enough that we would rather not guess
    """,
    re.VERBOSE,
)


def is_hard_break(line: str) -> bool:
    """Two trailing spaces or a trailing backslash are a deliberate break."""
    stripped = line.rstrip("\n")
    return stripped.endswith("  ") or stripped.endswith("\\")


def unwrap(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    run: list[str] = []

    def flush() -> None:
        if not run:
            return
        joined = run[0].rstrip()
        for cont in run[1:]:
            joined += " " + cont.strip()
        # Trailing whitespace is noise everywhere except here, where two spaces
        # are the break the author asked for; stripping it would delete the
        # break while leaving the newline, which renders differently.
        if run[-1].rstrip("\n").endswith("  "):
            joined += "  "
        out.append(joined)
        run.clear()

    start = 0
    # Frontmatter is a fence of its own and every line in it is significant.
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() in ("---", "..."):
                out.extend(lines[: i + 1])
                start = i + 1
                break

    fence_char = ""
    fence_len = 0
    for line in lines[start:]:
        if fence_char:
            out.append(line)
            m = FENCE.match(line)
            if m and m.group(1)[0] == fence_char and len(m.group(1)) >= fence_len:
                if not m.group(2).strip():
                    fence_char = ""
            continue

        m = FENCE.match(line)
        if m:
            flush()
            fence_char = m.group(1)[0]
            fence_len = len(m.group(1))
            out.append(line)
            continue

        if not line.strip():
            flush()
            out.append(line)
            continue

        if ATOMIC.match(line):
            flush()
            out.append(line)
            continue

        if LIST.match(line):
            flush()
            run.append(line)
        elif run:
            run.append(line)
        else:
            run.append(line)

        if is_hard_break(line):
            flush()

    flush()
    return "\n".join(out)


def main() -> int:
    payload = json.load(sys.stdin)
    path = (payload.get("tool_input") or {}).get("file_path") or ""

    # Narrow on purpose. This hook ships with the plugin, so it is loaded in
    # every session jig is installed in, and it has no business reformatting
    # anything but the artifacts the loop itself writes.
    if not path.endswith(".md") or "/docs/plans/" not in path.replace("\\", "/"):
        return 0

    with open(path, encoding="utf-8") as f:
        original = f.read()

    unwrapped = unwrap(original)
    if unwrapped == original:
        return 0

    with open(path, "w", encoding="utf-8") as f:
        f.write(unwrapped)

    # Say so, or the next Edit is written against line breaks that no longer
    # exist and fails on a stale old_string.
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": (
                        f"jig unwrapped hard line breaks in {path}: paragraphs and "
                        "list items are now one line each, drawings untouched. Line "
                        "numbers and line breaks have changed — re-read the file "
                        "before your next edit to it, and write prose unwrapped."
                    ),
                }
            }
        )
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
