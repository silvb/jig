---
name: plan-product
description: Start the planning loop for a feature, product, or epic — triage how much planning it needs, then produce a product design artifact with the problem, the success signal, ASCII wireframes, a workflow outline, and acceptance criteria. Use this whenever the user wants to plan, spec, design, or scope a feature or product before implementation, whenever they describe something they want to build and it is more than a trivial change, and whenever they mention vertical slices, planning phases, or a product review doc. This is the entry point of the loop — reach for it before writing any implementation plan.
---

# Product design

Phase 1 of 4. Produces `01-product.md`.

Read `${CLAUDE_PLUGIN_ROOT}/references/artifact-conventions.md` and
`${CLAUDE_PLUGIN_ROOT}/references/critical-inquiry.md` before drafting.

This phase stays in the product space: what the user experiences and why. When
a technical detail surfaces — and it will — write it down in a scratch list for
phase 2 and return to the user's experience. If a technical unknown genuinely
blocks a product decision, say so and propose either committing to what you
have or doing a spike first.

## Step 1: Triage

Classify before drafting, because most work does not need four phases.

**Oneshot** — no new user-visible surface, no contract change, one layer, and
an obvious repro or an obvious correct answer. Copy tweaks, one-off scripts,
bugs with a clear cause.

**Medium** — touches at most two layers, no schema change, reversible in a
single commit. Produce a merged product-and-architecture document as
`01-product.md`, skip `plan-program`, still do `plan-slices`.

**Full** — any one of: a new user-visible surface, a new or changed contract, a
schema migration, three or more layers touched, or the human cannot name the
call stack from memory. That last test is the most reliable one and it is the
human's to answer, not yours.

Present the classification and your reasoning, and stop. Triage is a gate. If
the human says the work is bigger than you judged, they are right — they know
the codebase's history and you do not.

For oneshot, say plainly that this does not need the loop and offer to just do
it.

## Step 2: Epic mode

If the work spans several user-visible capabilities, write `00-epic.md`
instead: the problem, the outcome signal, and a **feature breakdown** — each
feature with a one-line user-visible outcome and a dependency order. No
mockups, no acceptance criteria; those belong to the features.

Then stop. Each feature runs the full loop in its own directory. Ask which
feature to start with.

## Step 3: Draft `01-product.md`

```markdown
---
feature: <slug>
phase: product
status: draft
depth: full
updated: YYYY-MM-DD
---

# <Feature name>

## Problem
The user pain, in the user's terms. What they cannot do today, or what costs
them more than it should. No solution language.

## Who this is for
Primary user, and explicitly who this is not for.

## Outcome signal
What we can read after shipping to decide this was worth building. Prefer a
user outcome ("completes X without leaving the page") over a system metric.
"Support tickets about X stop" is a legitimate signal.

## Workflow
A JSON outline of the steps and their exits — the state machine of the user's
path, including the ways out that are not success.

## Screens
ASCII wireframes, one per state. See references/ascii-wireframes.md.

## Acceptance criteria
Given / When / Then, written from the user's side. These become the Verify
blocks in phase 4, so make them observable.

## Out of scope
What we decided not to do, and why. This section prevents the most expensive
kind of rework.

## Deferred to later phases
Technical notes that surfaced here and belong in architecture or program
design.
```

### Workflow outline format

```json
{
  "workflow": "publish-draft",
  "steps": [
    { "id": "compose", "user_does": "writes content", "exits": ["save", "discard"] },
    { "id": "review",  "user_does": "checks preview",  "exits": ["publish", "back"] },
    { "id": "publish", "user_does": "confirms",        "exits": ["done", "error"] }
  ]
}
```

The exits matter more than the steps. Happy paths get designed by default;
exits are where features are actually incomplete.

## Step 4: Wireframes

ASCII is the default. Read `references/ascii-wireframes.md` for the format.

Produce HTML mockups only when the human asks. When they do, write
self-contained files into `01-product.mockups/<state>.html`, one per state,
Tailwind from CDN, no build step — and reference them from the Screens section.

## Step 5: Gate

Stop. Present contestable decisions, assumptions, open questions, and the file
path, per `artifact-conventions.md`. Do not continue to architecture.

When the human approves, set `status: approved` and tell them the next step is
`plan-architecture`. Do not run it unprompted.
