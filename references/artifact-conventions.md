# Artifact conventions

Shared by all four planning skills. Read this before writing any artifact.

## Why these conventions exist

The artifacts are committed to the repository, which means they are diffable. A
human reviews a plan revision the same way they review code: by reading the
diff. Two things follow, and most of the rules below are downstream of them:

1. **Edit, never regenerate.** Rewriting a whole file to change one decision
   produces a diff nobody can read, which destroys the reviewability that
   justified committing the artifacts in the first place.
2. **The artifacts are the loop's state.** An agent with no conversational
   memory must be able to read the feature directory and resume. Anything that
   only exists in chat is lost.

When those two pull apart, the human wins. An agent that misreads a plan is
caught by the human who did not; a human who cannot hold the plan in their head
has nothing left to catch it with, and re-steering the next phase is how this
loop actually recovers.

## Directory layout

```
docs/plans/
  <epic-slug>/
    00-epic.md                       # only when the work spans several features
    features/
      <feature-slug>/
        01-product.md
        01-product.mockups/          # only when HTML mockups were requested
        02-architecture.md
        03-program-design.md
        04-slices.md
        slices/
          01-<slice-slug>.md
          02-<slice-slug>.md
```

A single feature with no epic above it still lives at
`docs/plans/<feature-slug>/` with the same file names — omit the `features/`
level rather than inventing a fake epic.

## Frontmatter

Every artifact opens with:

```yaml
---
feature: <feature-slug>
phase: product | architecture | program | slices
status: draft | approved
depth: oneshot | medium | full
updated: YYYY-MM-DD
---
```

`status` is a record of what happened, not the approval mechanism. Approval
happens in conversation. Set `status: approved` only after the human has said
so in words — never in the same turn the artifact was drafted.

## Cross-references

Reference other artifacts by **file path**, never by phrases like "as decided
above" or "per the architecture doc". A cold agent reading
`03-program-design.md` needs to know exactly which file to open:

- Good: `Contract defined in 02-architecture.md § Contract`
- Bad: `Uses the endpoint we agreed on earlier`

The same applies to claims about existing code: cite `path/to/file.ts:42`.

## Record decisions, not the work

An artifact is the record of what was settled. It is not a record of how it came
to be settled, and that difference accounts for most of the pages nobody reads.

**Outcomes, not the investigation.** What you looked at, what you ruled out on
the way, which subagent turned up what, the order in which you came to
understand the domain — none of it belongs. The reader wants the position you
arrived at, with enough citation to check it. "Status transitions go through one
function, `src/draft/draft-store.ts:140`" is the finding; the search that located
it is not part of the design.

**One line per rejected alternative.** A decision worth recording is worth
recording as "chose X over Y because Z", the same form the gate uses. The reason
to write the loser down at all is to stop the next cold agent from re-proposing
it, and one line does that — a three-paragraph rebuttal does not do it better.
Sustained argument also gives a document a defensive tone, which makes it harder
to contest later, and being contestable is the whole point of committing it.

**Omit sections that do not apply.** The template in each skill is a menu, not a
form. A feature that touches no database has no Data model section — not a Data
model section reading "N/A". An empty heading costs a line in the skim and
teaches the reader that headings are not load-bearing, which is expensive here,
because they are.

Two headings earn a sentence rather than deletion when they come up empty,
because their emptiness is itself a finding: an Out of scope with nothing in it
usually means nothing was cut, and a Failure modes with nothing in it usually
means nobody looked. Say which is true instead of dropping the heading.

A section another artifact cites by name — `02-architecture.md § Contract`,
`03-program-design.md § Decisions` — is omitted only when the thing itself does
not exist, never merely because it is short.

## Length and duplication

A planning artifact is skimmed, not studied. The human is deciding whether to
let work proceed, and a cold agent is looking for the one section it needs to
act on. Both are served by a document that fits on two screens. Neither is
served by one that restates its own inputs at length.

Three habits produce nearly all of the bloat, and they share a fix.

**Transcribing code.** A paragraph describing what `publishDraft` does is longer
than `publishDraft`, less precise than reading it, and wrong the moment the
function changes. Cite `src/draft/publish.ts:42` and move on — every reader of
these documents can open a file. What belongs in the artifact is what opening
the file will *not* tell you: an invariant that nothing enforces, a behaviour
spread across four call sites, a convention that holds in three places and
breaks in the fourth. State the finding, not the source.

**Restating an upstream artifact.** `02-architecture.md` does not re-explain the
problem, the users, or the acceptance criteria — `01-product.md` holds them and
is one directory entry away. Reference it by path and write only what this phase
decided. The unit that has to stand alone is the feature directory, not the
file; a document that stands alone on its own has usually managed it by
duplicating something that will now drift out of sync.

**Narrating the research.** The sharpest case of recording work rather than
outcomes, and common enough to name on its own: what a `codebase-researcher`
returned is input to your thinking, not a section of the artifact. Current state
carries the few facts the design actually turns on, cited, and stops. A fact
that changes no decision in this document is not current state — it is
background, and the reader already has the repository.

### The budget

Excluding its drawings — wireframes, diagrams, tables, signature blocks, which
are the dense part and the whole point — a planning artifact runs to about two
screens. Current state, specifically, is ten lines at most. An artifact well
over that is carrying something it should be citing.

The skim test: read only the headings and the drawings. If that is not enough to
know what was decided, the decisions are buried in prose, and the document needs
restructuring rather than trimming.

## Gates

Every phase ends with a hard stop. The stop is the entire point of the phase —
a phase that flows straight into the next one has bought nothing.

The gate is not the first time the human sees the material. Each contestable
section is drawn in the conversation and settled before the document is written
(`sketch-checkpoints.md`), so by the time the file exists its shape is already
agreed. That makes the gate a confirmation of the whole against its parts, which
is a different question from "is any of this right" and a much cheaper one to
answer. It stays a hard stop either way.

At the gate, present in chat (not the full document — the human reads that in
their diff viewer):

1. **Contestable decisions** — 3 to 6 bullets, each in the form "chose X over
   Y because Z". A decision with no plausible alternative is not contestable
   and does not belong here.
2. **Assumptions and inventions** — everything filled in without being told.
   This is where wrong plans get caught.
3. **Open questions** — whatever the checkpoints did not already settle, batched
   from critical inquiry, and asked through interactive elicitation rather than
   as prose, so the human answers by choosing rather than by composing (see
   `critical-inquiry.md` § How to ask).
4. **The file path**, so the human can open it in Hunk or any diff viewer.

Then stop. Do not draft the next phase. Do not start implementing. Do not set
`status: approved`. Wait for a reply. An elicitation is a gate like any other —
presenting options is not the same as being given an answer.

If the human's reply is partial approval with changes, edit the artifact,
present the diff summary, and stop again.

## Resumability test

Before finishing any phase, ask: if a fresh agent were handed only this
directory path and no conversation history, could it continue correctly?

If the answer depends on something said in chat, that something belongs in a
file. This bites hardest around checkpoints, where a shape is agreed in
conversation turns before the document exists: the drawing the human approved,
and one line naming the one they rejected, both have to end up written down.

## What gets committed

- The four planning artifacts, committed together after the `04-slices.md`
  gate, before the first slice.
- Per slice: the code plus any intentional plan edits, in one commit.

Nothing else. Review annotations live in the Hunk session and are cleared on
approval; where Hunk is unavailable they live in a temporary file that is
deleted on approval *before* the commit, so it never enters the history. The
blind review report is likewise temporary and is deleted after triage. The only
exception is a finding the human explicitly accepted with a reason — that is
folded into the Decisions section of `03-program-design.md` so the next review
does not re-litigate it.
