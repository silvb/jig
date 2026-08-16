---
description: Approve the slice under review — record decisions, commit, reset
argument-hint: [docs/plans/<slug>]
---

The human has approved the slice currently in review.

1. Resolve the annotations into `03-program-design.md` § Decisions — settled
   decision plus compressed reasoning, not the raw argument.
2. Update the slice's row in `04-slices.md` to `committed <sha>`.
3. If the slice ran in sidecar or file mode, delete the annotation file now,
   before the commit — otherwise an ephemeral file lands in the history.
4. Commit code and plan edits together:
   `feat(<feature-slug>): slice N — <name>`
5. If Hunk was the review surface, clear and reload it:
   `hunk session comment clear --repo . --all --yes`
   `hunk session reload --repo . -- diff`
   Skip both if `hunk` is not installed; step 3 was the equivalent.

Then stop. Report the SHA and which slice is next. Do not start it.
