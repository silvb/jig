---
description: Phase 2 — design the seams, contract, and data model
argument-hint: [docs/plans/<slug>]
---

Use the `plan-architecture` skill.

Feature directory: $ARGUMENTS

Verify `01-product.md` is `status: approved` before starting. Dispatch
`codebase-researcher` subagents in parallel to ground the design; every claim
about existing code carries a file:line citation.

Research grounds your thinking, it does not become a section. Current state is
ten lines at most — no transcribed code, no walking a file through in prose, no
restating the problem or the acceptance criteria that `01-product.md` already
holds. Cite files and upstream artifacts by path and let the reader open them.

Record outcomes, not the investigation that produced them, and rejected
alternatives in one line rather than an argument. Drop template sections this
feature does not have — no database means no Data model and no migration, not a
heading over "N/A".

Draw before you write. The flow diagram, the contract, the data model, and the
failure-modes table are each settled in the conversation first — drawn in full,
one elicitation each, stop — and only then assembled into `02-architecture.md`.

Where the seams show a product decision is unbuildable or far more expensive
than it looked, surface it and amend `01-product.md` rather than designing
around it — `artifact-conventions.md` § Amending an upstream artifact. Approved
upstream means settled, not frozen.

Stop at the gate, and ask whatever the checkpoints left open as elicited options
with their consequences named. Do not continue to program design.
