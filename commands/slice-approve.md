---
description: Approve the slice under review — record decisions, commit, reset
argument-hint: [docs/plans/<slug>]
---

The human has approved the slice currently in review.

1. Resolve the Hunk annotations into `03-program-design.md` § Decisions —
   settled decision plus compressed reasoning, not the raw argument.
2. Update the slice's row in `04-slices.md` to `committed <sha>`.
3. Commit code and plan edits together:
   `feat(<feature-slug>): slice N — <name>`
4. `hunk session comment clear --repo . --all --yes`
5. `hunk session reload --repo . -- diff`

Then stop. Report the SHA and which slice is next. Do not start it.
