---
description: Implement the next pending slice — one slice, then stop
argument-hint: [docs/plans/<slug>]
---

Use the `plan-slices` skill, Part B.

Feature directory: $ARGUMENTS

Resume cold: read `04-slices.md` for the status column, cross-check against
`git log`, read `01`-`03` and the next pending slice file. Ask nothing the
directory already answers.

Then, for exactly one slice: implement, run the deterministic checks and fix
what fails (three attempts maximum per check, never by weakening tests or
loosening types), self-annotate in Hunk, dispatch `slice-reviewer`, and hand it
to the human with the Verify block.

Stop. Do not start the following slice.
