---
name: plan-slices
description: Phase 4 of the planning loop, and the implementation loop itself — cut approved plans into vertical slices that each produce something the human can touch, then implement exactly one slice per turn with self-checks, self-annotation in Hunk, an independent gap-hunting review, human approval, and one commit per slice. Use this after the planning phases are approved, whenever the user asks to break work into slices or tracer bullets, and whenever they want to start, continue, or resume implementing a planned feature.
---

# Vertical slices

Phase 4 of 4, plus the implementation loop. Produces `04-slices.md` and
`slices/NN-<slug>.md`.

Read `${CLAUDE_PLUGIN_ROOT}/references/artifact-conventions.md`,
`${CLAUDE_PLUGIN_ROOT}/references/critical-inquiry.md`,
`${CLAUDE_PLUGIN_ROOT}/references/sketch-checkpoints.md`, and
`references/hunk-loop.md`.

Models default to horizontal plans — migrations, then services, then API, then
frontend — because that is how the stack is drawn. It is a bad way to build,
because nothing is touchable until the end, and by then there are two thousand
lines and no idea which of them is wrong.

## Part A — Cutting the slices

### Middle-out ordering

Start where the contract meets the consumer and work outwards:

1. Contract with mock data, verifiable by curl or in the browser
2. Frontend consuming the mock, iterated visually
3. Service layer wired in, still returning fixed behaviour
4. Persistence and migrations
5. Business logic
6. Error handling and edge cases

This is a default, not a template. The right first slice is the one that
retires the most risk while still being touchable.

### Every slice must be touchable

Each slice carries a Verify block containing a real human interaction — a URL,
a curl command, a CLI invocation, a visible state change. If you cannot write
one, the slice is cut wrong. Re-cut it. Do not fall back to "run the tests":
a slice whose only proof is a green test is a horizontal slice in disguise,
which is the exact failure this phase exists to prevent.

The touchable thing may be temporary and is often supposed to be — a real
endpoint returning mock data, a route that only renders, a seam wired to a
stub. That is the middle-out ordering working as intended.

Slices should land in roughly 100–200 lines. Beyond that, resteering gets
expensive, which is the whole reason for slicing.

### Sketch the cut in the conversation

Two checkpoints before the file exists, per
`${CLAUDE_PLUGIN_ROOT}/references/sketch-checkpoints.md`.

**1. The slice table and its ordering.** Draw the table below in chat, rows and
all. Ordering is the whole argument of this phase, so where you weighed a
different cut, draw that table too and put the two up side by side — the human
knows which risks bit them before, and reads two orderings faster than they read
your reasoning about one.

**2. The Verify blocks.** All of them together, in one checkpoint, because what
matters is whether the sequence of them walks the feature into existence step by
step. Ask whether each is something they would actually run. A Verify block the
human would not bother executing is a slice that will be approved unexercised,
which is the same failure as a green test standing in for a proof.

The per-slice Scope and Out of scope sections are read off the settled table and
`03-program-design.md` § File tree; they go straight into the files.

Cutting is the last cheap chance to notice that phase 3 is wrong — an ordering
that cannot be built without a seam the design puts three slices later is a
program-design problem wearing a slicing problem's clothes. Raise it at the
table checkpoint and follow
`${CLAUDE_PLUGIN_ROOT}/references/artifact-conventions.md` § Amending an
upstream artifact, rather than bending the cut around it.

### `04-slices.md`

```markdown
---
feature: <slug>
phase: slices
status: draft
depth: full
updated: YYYY-MM-DD
---

# <Feature name> — slices

| # | Slice | Touchable proof | Status |
|---|-------|-----------------|--------|
| 1 | Publish endpoint w/ mock | curl returns published draft | pending |
| 2 | Publish button + states | click in browser, states render | pending |
| 3 | Service layer wired | real permission errors visible | pending |
| 4 | Persistence + migration | publish survives reload | pending |

Status is `pending`, `in-review`, or `committed` — no SHA. A commit's ID is a
hash of its own contents, and this file is one of them, so a row naming the
commit it ships in can never be right. `git log` maps slices to commits already:
the message is `feat(<feature-slug>): slice N — <name>`.
```

Each slice also gets `slices/NN-<slug>.md`:

```markdown
# Slice N: <name>

## Goal
One sentence. What is true after this slice that was not before.

## Scope
Files touched, referencing 03-program-design.md § File tree.

## Out of scope
What is deliberately left stubbed or fake, and which slice picks it up.

## Verify
Written for the human, not a test runner:
1. `pnpm dev`
2. Open http://localhost:3000/drafts
3. Click Publish on the first row
4. Expect: badge changes to Published, timestamp appears
5. Try: click Publish again — expect a "already published" message, not an error page

## Deterministic checks
The exact commands the implementer runs before handing over.
```

Then stop. Gate as usual, and elicit whatever the two checkpoints left open.
Ordering is the contestable thing in this phase, so if it is still unsettled at
the gate, offer the alternative cut as a drawn option rather than describing it
in a paragraph.

### Commit the plan

On approval, set `status: approved`, then commit and push `04-slices.md` and the
per-slice files together, before any implementation:

```
plan(<feature-slug>): slices
```

The earlier phases committed their own artifacts at their own gates, so by now
the whole plan is in the history as four reviewable changesets rather than one —
see `artifact-conventions.md` § What gets committed. If an artifact from an
earlier phase is still uncommitted, that gate did not close; find out why before
cutting anything.

### Check the review surface

Before the first slice, probe for Hunk (`command -v hunk`). If it is missing,
offer the install once, here, where there is still time to set it up before
there is a diff to read:

```bash
npm i -g hunkdiff
```

The loop runs without it — see the file mode in `references/hunk-loop.md` — but
noticeably worse, because implementer and reviewer notes stop landing inline on
the lines they are about. Make the offer as an elicitation — install now, or run
in file mode — so declining is as cheap as accepting. Take the answer and move
on. Do not re-offer at every slice.

## Part B — The slice loop

**Implement exactly one slice per turn.** Then stop and wait. An agent that
implements three slices because they were small has handed back an unreviewable
changeset and defeated the point.

### 0. Pick the annotation mode

Probe before implementing, so steps 3 through 6 know where notes go:

```bash
command -v hunk >/dev/null 2>&1 && hunk session list
```

Live session, sidecar, or file — `references/hunk-loop.md` § Modes defines all
three and how to write into each. **Always use the highest available mode**, and
re-probe every slice rather than reusing last slice's answer; the human may have
installed Hunk in between. If Hunk is present, load its own review skill now
(`hunk skill path`) — it is authoritative over the command subset in the
reference.

### 1. Implement

Follow `03-program-design.md`. Where reality contradicts the design, follow
reality and flag it — do not silently conform the code to a plan that turned
out wrong, and do not silently abandon the plan either.

Two different things hide under "the plan was wrong", and they are handled
differently. A local departure — this signature needed one more parameter, this
error maps somewhere else — is an `IMPL/deviation:` note, resolved into
`03-program-design.md` § Decisions on approval. A decision that is wrong at its
own altitude, where the code just made that visible, is an upstream amendment:
stop, put it to the human with the branches named, and follow
`${CLAUDE_PLUGIN_ROOT}/references/artifact-conventions.md` § Amending an
upstream artifact. Here that section's downstream rule has teeth — an amendment
to `02-architecture.md` mid-loop reaches `03-program-design.md`, `04-slices.md`,
and the pending slice files, and all of it lands in this slice's commit.

### 2. Self-check

Run the slice's deterministic checks: typecheck, lint, tests, build.

Fix what fails, up to three attempts per failing check. Then stop and report
what is still red and what was tried. Endless self-repair loops burn the
human's time and budget for nothing.

Two things are never done to make a check pass:

- Disabling, skipping, weakening, or deleting a test.
- Loosening types — `any`, non-null assertions, casts, `@ts-ignore`.

If the honest fix requires departing from the plan, that is a `DEVIATION:`
note, not a quiet edit.

### 3. Self-annotate

Batch annotations into whichever channel step 0 selected — the live session, the
sidecar file, or `slices/NN-<slug>.notes.md`. See `references/hunk-loop.md` for
the commands and the notes-file format. Three permitted kinds:

- `IMPL/choice:` — a real alternative existed and you picked one.
- `IMPL/assumed:` — the plan was silent or wrong and you filled the gap.
- `IMPL/deviation:` — you departed from `03-program-design.md`.

Cap around five, in every mode — the cap is on the human's attention, not on the
channel. Forbidden: notes describing what the code does. The human can read the
code; what they cannot read is what you were unsure about.

### 4. Independent review

Dispatch the `slice-reviewer` subagent, telling it the active mode and, in file
mode, the notes file path. It hunts for gaps you did not notice — it reads the
plans, the diff, and your annotations, and takes a position on each rather than
duplicating it. Wait for it to finish before presenting.

In file mode it returns its full findings rather than a one-line verdict; pass
those through to the human intact rather than summarising them away.

### 5. Hand to the human

Tell them where the slice is — Hunk, the sidecar file, or the notes file, named
explicitly — and give them:

- The one-line goal
- Deterministic check results
- The Verify block, so they can exercise it locally
- A one-line note on what the reviewer flagged

Where the reviewer raised something blocking, elicit the disposition of each
finding — fix in this slice, carry to a later one, or accept with a reason —
one question per finding, batched, up to four in a call. Always include the
option that means "hold, I want to read the diff first": the human's real answer
often only exists after they have looked, and an option set that assumes
otherwise pushes them into deciding blind.

Then stop.

### 6. On approval

1. Resolve the annotations into `03-program-design.md` § Decisions — the
   settled decision and its reasoning, compressed. A decision recorded without
   its reasoning gets re-argued by the next cold agent, which is worse than not
   recording it.
2. Update the slice's row in `04-slices.md` to `committed`.
3. In sidecar or file mode, delete the annotation file now — **before** the
   commit. It lives in the feature directory, so committing first is how a file
   the loop calls ephemeral ends up in the history permanently.
4. Commit code and plan edits together — including any upstream amendment this
   slice forced, which belongs here and not in a commit of its own:
   `feat(<feature-slug>): slice N — <name>`. Then push, as at every planning
   gate.
5. In live mode only, clear the session comments and reload Hunk for a clean
   next slice. There is nothing to clear in the other two modes — step 3 was
   the equivalent.
6. Stop. Wait to be asked for the next slice.

### After the last slice

Tell the human the feature is complete and offer the blind review
(`blind-reviewer`). Do not run it unprompted — it is a deliberate step, not a
formality.

## Resuming cold

Given only a feature directory path: read `04-slices.md` for the status column,
cross-check against `git log`, read `01`–`03` and the next slice file, and
continue. Ask nothing that the directory already answers.
