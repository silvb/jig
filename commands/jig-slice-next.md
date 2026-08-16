---
description: Implement the next pending slice — one slice, then stop
argument-hint: [docs/plans/<slug>]
---

Use the `plan-slices` skill, Part B.

Feature directory: $ARGUMENTS

Resume cold: read `04-slices.md` for the status column, cross-check against
`git log`, read `01`-`03` and the next pending slice file. Ask nothing the
directory already answers.

Probe the annotation mode first (`command -v hunk`, then `hunk session list`)
and use the highest one available — see `hunk-loop.md` § Modes. Re-probe every
slice; the human may have installed Hunk since the last one.

Then, for exactly one slice: implement, run the deterministic checks and fix
what fails (three attempts maximum per check, never by weakening tests or
loosening types), self-annotate into the selected channel, dispatch
`slice-reviewer` with the active mode, and hand it to the human with the Verify
block and the path to the annotations.

Stop. Do not start the following slice.
