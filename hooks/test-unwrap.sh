#!/usr/bin/env bash
# Exercises hooks/unwrap-artifacts.py. This is the only executable file in the
# plugin, so it is also the only one that can be wrong in a way reading will not
# catch — run this after touching it.
#
#   ./hooks/test-unwrap.sh

set -uo pipefail
HOOK="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/unwrap-artifacts.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/docs/plans/f"
fail=0

run() { printf '{"tool_name":"Write","tool_input":{"file_path":"%s"}}' "$1" | python3 "$HOOK"; }
check() { # name expected actual
  if [ "$2" = "$3" ]; then echo "ok   $1"; else
    echo "FAIL $1"; echo "  expected: $2"; echo "  actual:   $3"; fail=1
  fi
}

art="$TMP/docs/plans/f/02-architecture.md"
cat > "$art" <<'EOF'
---
feature: f
updated: 2026-08-18
---

# Title

A paragraph that was
hard wrapped across
three lines.

- A bullet that was
  wrapped too.
- A second bullet.

```mermaid
sequenceDiagram
  UI->>API: POST
```

| A | B |
|---|---|
| 1 | 2 |

1. Ordered item
   continued here.
2. Second item.

break here  
after the break.

    indented code
    stays put
EOF

run "$art" > /dev/null

check "paragraph joins"    "A paragraph that was hard wrapped across three lines." "$(sed -n '8p' "$art")"
check "bullet joins"       "- A bullet that was wrapped too."                      "$(sed -n '10p' "$art")"
check "second bullet kept" "- A second bullet."                                    "$(sed -n '11p' "$art")"
check "fence untouched"    "  UI->>API: POST"                                      "$(sed -n '15p' "$art")"
check "table untouched"    "| A | B |"                                             "$(sed -n '18p' "$art")"
check "ordered joins"      "1. Ordered item continued here."                       "$(sed -n '22p' "$art")"
check "frontmatter kept"   "updated: 2026-08-18"                                   "$(sed -n '3p' "$art")"
check "hard break kept"    "break here  "                                          "$(sed -n '25p' "$art")"
check "indented code kept" "    indented code"                                     "$(sed -n '28p' "$art")"

cp "$art" "$TMP/once.md"; run "$art" > /dev/null
check "idempotent" "" "$(diff "$TMP/once.md" "$art")"

out="$TMP/src.md"; printf 'a\nb\n' > "$out"; run "$out" > /dev/null
check "out of scope untouched" "2" "$(wc -l < "$out" | tr -d ' ')"

check "garbage stdin exits 0" "0" "$(echo nope | python3 "$HOOK" >/dev/null 2>&1; echo $?)"
check "missing file exits 0"  "0" "$(run /docs/plans/nope.md >/dev/null 2>&1; echo $?)"

[ "$fail" = 0 ] && echo "all passed" || echo "FAILURES"
exit "$fail"
