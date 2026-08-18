---
description: Phase 4 — cut the work into vertical slices, then commit them
argument-hint: [docs/plans/<slug>]
---

Use the `plan-slices` skill, Part A only.

Feature directory: $ARGUMENTS

Every slice needs a Verify block with a real human interaction. If you cannot
write one, re-cut the slice — do not fall back to "run the tests".

Draw before you write. The slice table with its ordering, and then all the
Verify blocks together, are settled in the conversation first — drawn in full,
one elicitation each, stop — and only then assembled into `04-slices.md` and the
per-slice files. Where you weighed a different ordering, put both tables up as
drawn options.

An ordering that cannot be built without a seam `03-program-design.md` puts
later is a program-design problem, not a slicing one. Raise it and amend that
file — `artifact-conventions.md` § Amending an upstream artifact — rather than
bending the cut around it.

Stop at the gate, and elicit whatever the checkpoints left open. On approval set
`status: approved`, then commit and push `04-slices.md` with the per-slice files
— `plan(<feature-slug>): slices`. The earlier phases committed their own
artifacts at their own gates; if one is still uncommitted, that gate did not
close. Then stop again. Do not implement slice 1 unprompted.
