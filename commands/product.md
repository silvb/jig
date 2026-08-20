---
description: Phase 1 — triage the work and draft the product design
argument-hint: [feature description or docs/plans/<slug>]
---

Use the `plan-product` skill.

Input: $ARGUMENTS

Triage the depth first (oneshot / medium / full) and stop for confirmation
before drafting — put the three depths up as an elicitation with yours
recommended, rather than asking in prose. If the work spans several user-visible
capabilities, write an epic breakdown instead and stop.

Then draw before you write. The workflow JSON, the wireframes, and the
acceptance criteria are each settled in the conversation first — drawn in full,
one elicitation each, stop — and only then assembled into `01-product.md`. A
finished document is the wrong place for the human to first meet the shape.

Draw the delta. This document introduces what the user will be able to do that
they cannot do today; it does not retell the product they already have. A
component the project already ships is one labelled box with a citation, and an
unchanged state is a line in the legend — `artifact-conventions.md` § The delta,
not the system.

Stop at the gate, and elicit whatever the checkpoints left open. On approval set
`status: approved`, then commit and push — `plan(<feature-slug>): product`. The
commit closes this gate; it does not open the next one. Do not continue to
architecture.
