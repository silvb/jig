# jig

**You set the shape. The agent makes the cuts. You check every one.**

Front-loaded planning and vertical-slice implementation for Claude Code, with a
human gate at every phase. A jig doesn't do the cutting — it constrains the
tool so every cut lands where you intended.

Based on the four phases in
[Why Software Factories Fail](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/wsff.md),
with [Hunk](https://github.com/modem-dev/hunk) as the review surface.

## The premise

Models are good at solving one-off problems and bad at maintaining codebase
quality over time, because nothing in their training penalises bad design —
tests pass or they do not, and the cost of bad architecture shows up months
later. So the human stays in the loop, and planning moves earlier, where
changing your mind is cheap.

Each phase produces a small, committed, diffable artifact. You reject wrong
decisions by reading a call-stack tree, not by reading two thousand lines of
finished code.

## Install

```bash
/plugin marketplace add silvb/jig
/plugin install jig
```

Requires `git`. Strongly recommended: [Hunk](https://github.com/modem-dev/hunk)
(`npm i -g hunkdiff`), kept open in a second terminal with `hunk diff --watch`.

Hunk is where the loop is meant to be reviewed — implementer and reviewer notes
land inline on the lines they concern, and where the two agents disagree their
notes sit next to each other. Without it the slice loop still runs: annotations
fall back to a temporary notes file beside the slice plan, deleted on approval
like every other ephemeral artifact. The planning phases need nothing but a
diff viewer. The loop offers the install once and never nags.

## The loop

```
/jig:product <description>      triage → sketch → 01-product.md        → gate → commit
/jig:architecture <dir>         research → sketch → 02-architecture.md → gate → commit
/jig:program <dir>              sketch → 03-program-design.md          → gate → commit
/jig:slices <dir>               sketch → 04-slices.md                  → gate → commit

  per slice, one per turn:
    /jig:slice-next <dir>       implement → self-check → annotate
                                → slice-reviewer → you, in Hunk
    /jig:slice-approve <dir>    → record decisions → one commit → reset

/jig:blind-review <dir>         once, after the last slice
```

`sketch` is the part you sit inside: each contestable section of the artifact
gets drawn in the conversation and settled with you before the document is
written. It is several stops, not one — see Drawings come before documents,
below.

Not everything needs this. `plan-product` triages first: oneshot work is
just done, medium work merges phases 1 and 2 and skips program design, full
depth runs everything.

## What each phase is for

| Phase | Artifact | The question you answer |
|---|---|---|
| Product | Problem, outcome signal, ASCII wireframes, workflow JSON, acceptance criteria | Is this the right thing? |
| Architecture | Sequence diagram, contract, data model diff, failure modes | Do the seams sit right? |
| Program design | Call-stack trees, file-tree diff, typechecked signatures | Is this the code I'd have written? |
| Slices | Ordered slices, each with a manual Verify block | Can I feel it working at each step? |

## Three agents

**`codebase-researcher`** grounds phases 2 and 3 in what actually exists.
Every claim carries a `file:line` citation; uncited assertions are rejected.

**`slice-reviewer`** (opus) reviews each slice before you see it. It reads the
plans, the diff, and the implementer's own annotations, and takes a position on
each rather than duplicating them. It hunts for what the implementer was
confidently wrong about — the complement of what the implementer already
flagged. It never blocks; you decide.

**`blind-reviewer`** (opus) runs once at the end and sees only `01-product.md`
and the finished code. Never the architecture, program design, slice plans, or
commit messages — being anchored to our reasoning is what it exists to avoid.
It reviews outcome fit, organization, test coverage, the
premature-optimization / extensibility trade-off, and business logic leaking
into technical abstractions.

## Design rules worth knowing

**One slice per turn.** An agent that implements three slices because they were
small has handed back an unreviewable changeset.

**Every slice must be touchable.** A slice whose only proof is a green test is
a horizontal slice in disguise. Verify blocks are written for you to run
manually — Playwright appears only in deterministic checks on already-written
tests, or when you ask for it by name.

**Self-healing has a fuse.** Three attempts per failing check, then it stops
and reports. Never by disabling tests or loosening types.

**Questions are asked, not narrated.** Every decision the loop needs from you —
the depth triage, the open questions at each gate, the disposition of a review
finding — arrives as a choice with the options and their consequences on screen,
not as a paragraph you have to reply to. Free text always still works; the
options exist so the common answer costs one keystroke.

**Drawings come before documents.** Each phase settles its material in the
conversation, one section at a time — the workflow JSON, then the wireframes,
then the acceptance criteria; the sequence diagram, then the contract, then the
schema diff — drawn at full fidelity, one question on each, then a stop. The
artifact is assembled from pieces you already agreed to, so the gate confirms
rather than reveals. Where a fork is real you get both drawings side by side and
pick one, instead of writing a paragraph about what is wrong with the one you
were shown. Say "just draft it" and the whole sequence collapses to a single
sketch.

**Approved upstream means settled, not frozen.** Phase 3 finding that the
architecture was overbuilt is phase 3 doing its job — you only see that a seam
is one function once the signatures are written. When it happens you get the
branches as a choice: amend the upstream artifact and carry on, keep the
decision and design within it, or stop and re-run that phase. The amendment is a
narrow edit to the decision itself, it drags every downstream artifact it
reaches along with it, and it rides in the same commit as the work that
motivated it — so the change of mind reads as one diff. What never happens is a
phase quietly writing a document that contradicts the one above it.

**Artifacts are not hard-wrapped.** Paragraphs and list items are one line
each, and your editor, pager, or diff viewer wraps them however you like. Hard
wrapping makes a one-word change re-flow the paragraph, so a trivial revision
lands as five changed lines and you have to find the real edit inside the noise
— which defeats reviewing plans as diffs. A hook enforces it on every write
under `docs/plans/`; fenced blocks, tables, and frontmatter are never touched,
because that is where the line breaks are the content.

**Plans record decisions, not the work of deciding.** Outcomes rather than the
investigation that produced them, one line per rejected alternative rather than
an argument, and no section for something this feature does not have — a
feature with no database gets no Data model heading, not a heading over "N/A".

**Plans are skimmable, not thorough.** Two screens outside the drawings, and
Current state capped at ten lines. The artifacts cite code rather than
transcribing it, and cite each other rather than repeating — you can open a
file, and the phase that already settled something is one directory entry away.
A plan that reads like a Sunday afternoon is a plan nobody re-reads at slice
four.

**Artifacts are the loop's state.** Hand a fresh agent nothing but a feature
directory path and `/jig:slice-next` and it resumes correctly. The unit that
stands alone is the directory, not any one file — which is what lets each
document stay short.

**Every gate ends in a commit.** Approve a phase and its artifact goes to
`status: approved`, gets committed, and gets pushed — one `plan(<feature>): …`
commit per phase, so the plan lands as four reviewable changesets rather than
one wall. Each slice goes the same way once you have tested it against its
Verify block: code and plan edits in one commit, committed and pushed. The commit is how the loop
records that a gate closed, which is why a resuming agent can read its own
position out of `git log`; it is not permission to start the next phase.

**Ephemeral by default.** Review annotations live in the Hunk session and are
cleared on approval. The blind review report is deleted after triage. What gets
committed is code and intentional plan changes — plus findings you accepted
with a reason, which fold into the Decisions section so they are not
re-litigated.

## Stack

Stack-agnostic by design; TypeScript is the worked example throughout.
Contracts are plain types plus a route table rather than a schema toolchain — a
contract format that requires an install will not get used on small features,
and small features are where the habit sticks or dies.

## Layout

```
skills/
  plan-product/        + references/ascii-wireframes.md
  plan-architecture/   + references/contract-design.md
  plan-program/        + references/callstack-notation.md
  plan-slices/         + references/hunk-loop.md
references/
  artifact-conventions.md    layout, frontmatter, gates, resumability
  critical-inquiry.md        per-phase questions, and how to put them
  sketch-checkpoints.md      drawing each section in chat before drafting
agents/
  codebase-researcher.md  slice-reviewer.md  blind-reviewer.md
commands/
  product  architecture  program  slices
  slice-next  slice-approve  blind-review
hooks/
  unwrap-artifacts.py        unwraps prose in docs/plans/ on every write
```
