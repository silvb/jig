# The Hunk loop

Hunk is the review surface for the whole loop — plan diffs and slice diffs
alike. It is where the human exercises control, so the annotations put into it
are the main channel by which agents tell them what to look at.

## Setup

The human keeps a Hunk window open in a second terminal:

```bash
hunk diff --watch
```

Load Hunk's own review skill rather than reimplementing its session API:

```bash
hunk skill path
```

Read the file it returns. The commands below are the subset this loop uses; the
skill is authoritative if they diverge.

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

## After approval

```bash
hunk session comment clear --repo . --all --yes
hunk session reload --repo . -- diff
```

`--all` clears the human's own notes too, so only run it once the human has
approved and the commit is made.

## Fallback without a live session

If no session is reachable, write the annotations to a sidecar file and tell
the human to open it alongside the diff:

```bash
hunk diff --agent-context /tmp/slice-notes.json
```

The loop still works; only the live steering is lost.
