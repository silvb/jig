---
description: End-of-feature second opinion from an agent that never saw the plans
argument-hint: [docs/plans/<slug>]
---

Run once, after the final slice is committed.

Dispatch the `blind-reviewer` subagent against: $ARGUMENTS

It may read `01-product.md` and the finished code only. Do not pass it the
architecture, program design, slice files, commit messages, or any review
annotations — being anchored to our reasoning is precisely what it exists to
avoid.

When it returns, present the findings and help the human triage each one into:
fix now, follow-up (re-enters at `plan-product`), or accepted with reason.

Fold accepted-with-reason findings into `03-program-design.md` § Decisions so
the next review does not re-litigate them, then delete `05-review.md`.
