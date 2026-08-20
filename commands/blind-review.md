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
fix now, follow-up (re-enters at `plan-product`), or accepted with reason. Run
that triage as elicitation — one question per finding, batched up to four in a
call, those three dispositions as the options, with your recommendation first.
A prose list of ten findings gets a reply about two of them.

Fold accepted-with-reason findings into `03-program-design.md` § Decisions so
the next review does not re-litigate them, then delete `05-review.md`.

Once the triage leaves nothing outstanding — no fix-now work still to commit —
the feature is done and its plan has stopped being true. Say so and offer
`/jig:retire`, which carries the accepted findings and any other live follow-up
out of the directory before deleting it. Do not run it unprompted.
