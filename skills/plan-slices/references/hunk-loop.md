# The Hunk loop

Hunk is the review surface for the whole loop — plan diffs and slice diffs
alike. It is where the human exercises control, so the annotations put into it
are the main channel by which agents tell them what to look at.

Hunk is optional but strongly preferred. The loop degrades to plainer channels
without it, and this file specifies both. Read the modes section before writing
a single annotation, because the mode decides where they go.

## Modes

Probe once, at the start of each slice. One command answers both questions —
is Hunk installed, and is a session live:

```bash
command -v hunk >/dev/null 2>&1 && hunk session list
```

| Mode | Condition | Annotations go to |
|---|---|---|
| **live** | `hunk` installed, session reachable | the session, inline on the diff |
| **sidecar** | `hunk` installed, no session reachable | an agent-context JSON file |
| **file** | `hunk` not installed | `slices/NN-<slug>.notes.md` |

**Always use the highest available mode.** A lower mode is a fallback, never a
convenience — inline annotations on the diff are the entire reason the human
can review a slice in one pass, and a notes file next to a diff is measurably
worse. Do not skip the probe and default to the file mode because it needs no
setup; that trades the human's attention for the agent's.

Re-probe at the start of every slice rather than caching the mode for the
feature. The human may install Hunk between slices, and an agent still writing
to a notes file after that has silently opted them out of what they just set
up.

State the active mode once per slice, in the handoff. A human who cannot tell
which channel was used will look in the wrong place and conclude the agents had
nothing to say.

## Offering the install

If the probe finds no `hunk`, offer it once per feature — at the phase 4 gate
if you are there, otherwise before the first slice — and never again for that
feature. Repeating it every slice is nagging, and it trains the human to skim
the handoff, which is where the findings are.

```bash
npm i -g hunkdiff
```

Say what it buys concretely: implementer and reviewer notes land inline on the
exact lines they concern, the two agents' notes interleave where they disagree,
and approval clears them in one command. Then continue in file mode regardless
of the answer. The offer is not a gate — a human who does not want another
global npm package is entitled to the loop anyway.

## Setup

The human keeps a Hunk window open in a second terminal:

```bash
hunk diff --watch
```

**Every agent that touches the session loads Hunk's own review skill first,**
rather than working from the subset below:

```bash
hunk skill path
```

Read the file it returns. The commands in this document are the subset this
loop uses, recorded so the loop is legible without Hunk installed; where the
two disagree, Hunk's skill is authoritative and this file is stale. Load it
once per agent, after the probe returns live or sidecar — there is nothing to
load in file mode.

## Reading the session

```bash
hunk session list
hunk session get --repo .
hunk session review --repo . --json
hunk session comment list --repo .
```

Use `--json` and only add `--include-patch` when the raw unified diff is
genuinely needed — the structured form is cheaper and usually sufficient.

If `hunk session list` reports nothing while Hunk is visibly running, the
sandbox may be blocking loopback. Probe the daemon directly:

```bash
curl -s -X POST http://127.0.0.1:47657/session-api \
  -H 'content-type: application/json' --data '{"action":"list"}'
```

Treat that as a live session if it answers. Dropping to sidecar mode because
loopback was blocked discards a window the human is actively looking at.

## Writing annotations

One batch per agent, via stdin:

```bash
printf '%s\n' '{"comments":[
  {"filePath":"src/draft/draft-service.ts","newLine":42,
   "summary":"IMPL/choice: returned Result rather than throwing, to match store-service.ts:88. Throwing would have been fewer lines but inconsistent with the layer."},
  {"filePath":"src/routes/drafts.ts","newLine":17,
   "summary":"IMPL/assumed: plan did not say what happens on double-publish. Returning 409 per the failure-modes table."}
]}' | hunk session comment apply --repo . --stdin
```

Each item needs `filePath`, `summary`, and exactly one target (`newLine`,
`oldLine`, `hunk`, or `hunkNumber`). Add `--focus` to jump the window to the
note.

Navigate the human to a specific place when it helps:

```bash
hunk session navigate --repo . --file src/draft/draft-service.ts --hunk 2
```

## Prefix conventions

The prefix is how the human tells the two agents apart at a glance and how the
reviewer avoids duplicating the implementer.

**Implementer** — what it knows it was unsure about:

- `IMPL/choice:` a real alternative existed
- `IMPL/assumed:` the plan was silent or wrong
- `IMPL/deviation:` departed from `03-program-design.md`
- `IMPL/fix:` changed after a failing self-check

**Reviewer** — what the implementer did not notice:

- `REVIEW/re <KIND>@<file>:<line>:` a position on an implementer note — agree,
  disagree with a reason, or escalate to the human
- `REVIEW/gap:` something unhandled that the plan implied
- `REVIEW/blind-spot:` something the implementer was confidently wrong about
- `REVIEW/plan-drift:` code contradicts the plan with no deviation flagged

The prefixes and the caps on them — around five implementer notes, at most
seven reviewer findings — are identical in all three modes. They are limits on
the human's attention, not on the medium.

## After approval

```bash
hunk session comment clear --repo . --all --yes
hunk session reload --repo . -- diff
```

`--all` clears the human's own notes too, so only run it once the human has
approved and the commit is made.

## Fallback: sidecar mode

Hunk is installed but no session is reachable. Write the same annotation batch
to a sidecar file and tell the human to open it alongside the diff:

```bash
hunk diff --agent-context /tmp/slice-notes.json
```

The file takes the same `{"comments":[…]}` shape as `comment apply`. The loop
still works; only the live steering is lost.

There is nothing to clear on approval — delete the sidecar file instead.

## Fallback: file mode

Hunk is not installed. Annotations go to
`slices/NN-<slug>.notes.md` in the feature directory, beside the slice file.

This file is temporary, exactly like `05-review.md`: it is **deleted on
approval, before the commit**, and never committed. Ordering matters — the
approval sequence commits the feature directory, so a notes file still on disk
at that point ends up in the history, which is precisely the ephemerality the
loop is designed to avoid.

Group by file, then ascending line. Put the reviewer's response to an
implementer note directly beneath it, because that adjacency is what Hunk gives
for free and it is the most valuable thing to preserve:

```markdown
# Slice 3 — service layer wired · notes

Temporary. Deleted on approval, never committed. Open beside your diff.

## src/draft/draft-service.ts

**:42** `IMPL/choice:` returned Result rather than throwing, to match
store-service.ts:88. Throwing would have been fewer lines but inconsistent
with the layer.

> **`REVIEW/re IMPL/choice:`** Disagree. Result is consistent with the store
> layer, but the route at drafts.ts:17 unwraps it with a bare throw, so the
> error typing is lost at the boundary anyway.

## src/routes/drafts.ts

**:17** `IMPL/assumed:` plan did not say what happens on double-publish.
Returning 409 per the failure-modes table.

**:31** `REVIEW/gap:` the 403 path in 02-architecture.md § Failure modes has
no branch here — a caller who lost permission mid-session gets a 500.
```

The implementer writes the file; the reviewer edits the same file rather than
starting its own, so the human has one thing to read. A reviewer that cannot
find the file writes it — the implementer had nothing to flag, which is a
legitimate outcome, not a reason to withhold the review.

In this mode the handoff carries the notes file path, and the reviewer returns
its **full findings** to the dispatching agent rather than the one-line verdict
it returns in live mode. In live mode the verdict is a pointer to notes the
human can already see; here there is no window, so a verdict alone would strand
the review.
