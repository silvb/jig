---
name: plan-program
description: "Phase 3 of the planning loop — go one level below architecture into the shape of the code: call-stack trees, file-tree diffs, and type and function signatures, before any implementation is written. Use this after plan-architecture is approved, and whenever the user wants to decide how code should be structured, what functions should exist, where files should live, or what the call flow looks like. Produces a committed 03-program-design.md and typechecks its own signature stubs."
---

# Program design

Phase 3 of 4. Produces `03-program-design.md`.

Read `${CLAUDE_PLUGIN_ROOT}/references/artifact-conventions.md`,
`${CLAUDE_PLUGIN_ROOT}/references/critical-inquiry.md`, and
`${CLAUDE_PLUGIN_ROOT}/references/sketch-checkpoints.md` before drafting.

Requires an approved `02-architecture.md`. Skipped entirely for
`depth: medium`.

This is the phase most people skip, on the assumption that once the
architecture is right the model can just cook. Every decision recorded here is
one that would otherwise be made implicitly during code review — at the most
expensive possible moment to change your mind.

It is also the phase most likely to find that phase 2 was wrong, and that is
half of what it is for. Architecture is decided before anyone knows what the
code looks like, so it overbuilds — a queue for one producer, a seam between two
things that turn out to be one function. Writing the signatures is what exposes
that. Approved upstream means settled, not frozen: surface the contradiction as
soon as the drawing raises it, and follow
`${CLAUDE_PLUGIN_ROOT}/references/artifact-conventions.md` § Amending an
upstream artifact. Designing around a decision you believe is wrong is the
failure here, and it is the easy thing to do, because the document above you is
marked approved.

This document is also the oracle the slice reviewer checks against later. There
is no general oracle for maintainability, but for this feature, this file is
one. Write it as something to be measured against.

## Step 1: Ground in the codebase

Dispatch `codebase-researcher` subagents for the questions phase 2 did not
already answer:

- What is the existing shape of code in this area — layering, naming, error
  handling, testing conventions?
- What utilities and types already exist that this should use?
- Where does similar logic already live, and would a reasonable person expect
  this to live beside it?

Cite `file:line`. Matching the codebase's existing patterns matters more here
than importing better ones; a locally consistent codebase beats a globally
optimal one that nobody can navigate.

As in phase 2, the research grounds your thinking and does not become a section.
A pattern you found is worth one cited line — "errors map to HTTP at the route
layer, `src/routes/drafts.ts:31`" — not a description of how that file works.

## Step 2: Sketch the code's shape in the conversation

Four checkpoints, in this order, before the file exists — each drawn in chat at
full fidelity with one elicitation on it, per
`${CLAUDE_PLUGIN_ROOT}/references/sketch-checkpoints.md`. Notation for the first
two is in `references/callstack-notation.md`; both use diff syntax, because what
is changing is the interesting part and a full tree buries it.

**1. The call stacks.** The diff-annotated trees. Ask where the new code hangs
off the existing tree, because that is the decision the tree makes visible and
prose hides.

**2. The file tree.** The layout diff with a purpose per file. The fork worth
drawing twice is "beside the code it resembles" versus "in a new module of its
own" — a placement argument settles in seconds against two trees and not at all
against a paragraph.

**3. The signatures.** Real declarations, no bodies. Ask the question the type
answers: what empty, null, and failure look like at this seam. A `Result` and a
throw are the archetypal two-drawing fork, and the human picks one on sight.

**4. The test plan.** The test names. Naming them is what settles the meaning
of done, so it is worth a stop of its own — the useful question is which
behaviour has no name in the list yet.

Invariants and Decisions do not get checkpoints. Invariants are read off the
drawings above once they are settled, and Decisions is a record that grows as
the loop runs, not a shape to choose.

## Step 3: Draft `03-program-design.md`

Write the settled drawings in, as drawn. Where a checkpoint turned on a real
fork, that fork and its loser belong in Decisions, one line each — this is the
section the slice reviewer reads later to avoid re-litigating what you already
settled, and a line does that as well as a page. Decisions is never omitted; it
grows for the rest of the loop and other files cite it by name.

This document is nearly all drawings, which is how it should be: call stacks,
a file tree, signatures, a list of test names. The prose between them is what
`artifact-conventions.md` § Length and duplication budgets to two screens. The
contract lives in `02-architecture.md` § Contract — cite it, do not copy it, or
the two will disagree by slice three and nobody will know which one is current.

```markdown
---
feature: <slug>
phase: program
status: draft
depth: full
updated: YYYY-MM-DD
---

# <Feature name> — program design

## Call stacks
Diff-annotated trees for the control flow that changes.

## File tree
The layout diff, with a one-line purpose per file.

## Signatures
Types and function signatures for the new surface. No bodies.

## Invariants
What must always be true, and what enforces it.

## Test plan
The test names — not the tests. Naming them here settles what "done" means.

## Decisions
Trade-offs settled during planning and during slice review. Each entry: the
decision, the alternative, and why. This section grows as the loop runs.
```

## Step 4: Typecheck the stubs

Write the Signatures section as real, compilable declarations — then verify it.
Extract the block to a scratch file and run the project's typechecker in
no-emit mode (`tsc --noEmit`, or the equivalent for the stack).

This is cheap and it catches a real class of problem: signatures that reference
types that do not exist, contradict the contract in `02-architecture.md`, or
cannot actually compose the way the call stack claims. A design phase usually
has no verification at all; this one gets a little.

Delete the scratch file afterwards. If the typecheck fails, fix the design
before presenting — do not present a design that does not hold together.

That rule puts this step earlier than its number suggests: run it against the
signatures before they go up as a checkpoint, not only before the gate. Asking
a human to weigh two seams that do not compile spends their attention on a
question you could have closed yourself. Report the result at the gate either
way, so it is on the record.

For untyped or dynamically typed stacks, skip this step and say so at the gate,
so the human knows the design carries less assurance than usual.

## Step 5: Gate

Stop. Present contestable decisions, assumptions, open questions, the
typecheck result, and the file path. Elicit the open questions rather than
listing them — a signature fork ("Result vs throw at this seam") is exactly the
shape that answers itself once both options are on screen with their
consequences, which is why most of them belong at the signatures checkpoint and
not here.

On approval, set `status: approved`, then commit and push —
`plan(<feature-slug>): program design`, per `artifact-conventions.md` § What
gets committed. Where this phase amended `02-architecture.md`, that edit rides
in the same commit, which is the point: the overbuilt decision and the
signatures that exposed it land in one diff.

Then the next step is `plan-slices`. Do not run it unprompted.
