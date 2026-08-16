---
name: plan-program
description: Phase 3 of the planning loop — go one level below architecture into the shape of the code: call-stack trees, file-tree diffs, and type and function signatures, before any implementation is written. Use this after plan-architecture is approved, and whenever the user wants to decide how code should be structured, what functions should exist, where files should live, or what the call flow looks like. Produces a committed 03-program-design.md and typechecks its own signature stubs.
---

# Program design

Phase 3 of 4. Produces `03-program-design.md`.

Read `${CLAUDE_PLUGIN_ROOT}/references/artifact-conventions.md` and
`${CLAUDE_PLUGIN_ROOT}/references/critical-inquiry.md` before drafting.

Requires an approved `02-architecture.md`. Skipped entirely for
`depth: medium`.

This is the phase most people skip, on the assumption that once the
architecture is right the model can just cook. Every decision recorded here is
one that would otherwise be made implicitly during code review — at the most
expensive possible moment to change your mind.

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

## Step 2: Draft `03-program-design.md`

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

## Step 3: Notation

Read `references/callstack-notation.md` for the call-stack and file-tree
formats. Both use diff syntax, because what is changing is the interesting part
and a full tree buries it.

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

For untyped or dynamically typed stacks, skip this step and say so at the gate,
so the human knows the design carries less assurance than usual.

## Step 5: Gate

Stop. Present contestable decisions, assumptions, open questions, the
typecheck result, and the file path.

After approval, the next step is `plan-slices`. Do not run it unprompted.
