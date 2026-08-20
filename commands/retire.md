---
description: Retire a finished feature — carry forward what is still live, delete the plan
argument-hint: [docs/plans/<slug>]
---

Run once, after the blind review has been triaged and any fix-now findings are
committed.

Feature directory: $ARGUMENTS

Read the directory and separate what the code now records from what is still
live: an outcome signal nobody has measured, an Out of scope entry that was a
deferral rather than a decision, a blind-review finding accepted with a reason,
a v2 or an adjacent feature named while building this one. Only the live things
leave the directory — see `artifact-conventions.md` § Retiring the plan.

Then look for where this repository already keeps future work — `docs/notes/`,
a roadmap or backlog file, an ADR directory, a `TODO.md`. Do not invent a
location. Propose what you found; where there is nothing, ask.

Put the retirement and the destination in one elicitation: what will be
deleted, what will be carried, and to which file. Then stop and wait — the
human may know about work in flight that the directory does not show.

On approval, write the carried-forward lines, compact and in the repository's
existing style, or none if nothing is still live. Then delete the feature
directory and commit the note and the deletion together —
`plan(<feature-slug>): retire` — and push.

Nothing is lost: every phase committed its artifact at its gate, so
`git log -- docs/plans/<feature-slug>` still has the whole plan at every version
it had. What the deletion removes is its claim to be current.
