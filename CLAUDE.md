# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`jig` is a Claude Code **plugin** — prose only. There is no source code, no build,
no test suite, no dependencies. Every file is Markdown instructions or a JSON
manifest, and the "program" is the behaviour those instructions produce in an
agent. Changes are reviewed by reading them, not by running them.

Consequence: correctness here means *internal consistency across files*. The same
rule is usually stated in three or four places on purpose (skill, command, agent,
reference), so a change is not done until every copy agrees.

## Commands

```bash
claude plugin validate .          # manifest check (marketplace + plugin.json)
claude plugin details jig         # component inventory + projected token cost
claude plugin tag .               # cut a {name}--v{version} release tag
```

`validate` passes clean; keep it that way — but note it checks the *manifests*
only. It does not parse skill frontmatter, so a `SKILL.md` whose YAML is broken
validates green while loading with no name and no description, which silently
removes the skill from dispatch. `tag` is the command that catches that, and it
is the last thing run before a release rather than the first, so run it early
after editing any frontmatter. The usual cause is an unquoted description
containing a colon followed by a space; quote the whole value.

`details` is the closest thing to a test: it reports what actually loads and
what it costs in context. A skill listed there with an empty description is the
same bug seen from the other side.

To exercise a change end to end, install the local checkout as a marketplace
(`/plugin marketplace add /home/silv/s/jig`) and run the loop against a scratch
repo. Bump `version` in `.claude-plugin/plugin.json` for anything user-facing.

## Architecture

A four-phase planning pipeline, then a one-slice-at-a-time implementation loop,
with a mandatory human stop ("gate") between every step.

```
commands/*.md     thin entry points — delegate to a skill, restate the invariant
   ↓              that phase most often loses, and say "stop at the gate"
skills/*/SKILL.md the phase itself; loads the three shared references, sketches
   ↓              each contestable section in chat, then drafts
references/       cross-cutting rules shared by all four skills
skills/*/refs/    notation/format detail owned by one phase
agents/           subagents dispatched by skills (research, review)
```

**Every phase draws before it writes.** Each contestable section of an artifact
is drawn in the conversation at full fidelity, gets one elicitation, and stops,
before the file is written; the gate then confirms the assembled whole rather
than revealing it. `references/sketch-checkpoints.md` owns the practice and the
per-phase checkpoint sequences. This is the rule most likely to be undone by an
edit that "simplifies" a skill back into draft-then-present.

**Phases and their artifacts** — the artifacts are the loop's only state. They
live in the *target* repo under `docs/plans/<feature-slug>/` (or
`docs/plans/<epic>/features/<feature>/`), are committed, and are reviewed as
diffs:

| Phase | Skill | Artifact |
|---|---|---|
| 1 Product | `plan-product` | `01-product.md` |
| 2 Architecture | `plan-architecture` | `02-architecture.md` |
| 3 Program design | `plan-program` | `03-program-design.md` |
| 4 Slices + impl loop | `plan-slices` | `04-slices.md`, `slices/NN-<slug>.md` |
| (end) Blind review | — | `05-review.md`, deleted after triage |

`plan-slices` is two skills in one file: **Part A** cuts the slices (phase
4), **Part B** is the per-slice implementation loop. `/jig:slices` invokes Part A
only; `/jig:slice-next` and `/jig:slice-approve` drive Part B.

**Depth triage** happens in `plan-product` step 1 and changes which phases
run: `oneshot` skips the loop entirely, `medium` merges phase 2 into
`01-product.md` and skips phase 3, `full` runs everything. Any edit to the phase
sequence has to be reflected in both `plan-product` (the triage
definitions) and `plan-architecture` (its `depth: medium` tail note).

**Agents** — `codebase-researcher` (sonnet, dispatched in parallel by phases 2
and 3, every claim cited `file:line`), `slice-reviewer` (opus, after each slice),
`blind-reviewer` (opus, once at the end, deliberately context-starved).

**Hunk** is the human's review surface, and an optional dependency.
`skills/plan-slices/references/hunk-loop.md` owns the session API subset
used here; agents that touch the session load `hunk skill path` first and treat
it as authoritative rather than reimplementing it.

**Annotation modes.** Part B probes at the start of every slice and picks the
highest available channel — `live` (session), `sidecar` (agent-context JSON), or
`file` (`slices/NN-<slug>.notes.md`). Three rules make the fallback safe, and
each is stated in more than one file: always take the highest mode, re-probe per
slice rather than caching, and in the two file-backed modes delete the
annotation file *before* the approval commit so an ephemeral file never enters
the history. The install is offered once per feature and never re-offered.

## Conventions to preserve when editing

**Reference paths.** Skills load the three shared references with
`${CLAUDE_PLUGIN_ROOT}/references/<file>.md` (absolute, plugin-relative) and
their own with a bare `references/<file>.md`. Do not mix the two forms.

**Coupled text that must be changed together:**

- Annotation prefixes (`IMPL/choice|assumed|deviation|fix`,
  `REVIEW/re|gap|blind-spot|plan-drift`) are defined in `hunk-loop.md` and
  restated in `plan-slices/SKILL.md` §3 and `agents/slice-reviewer.md`.
  They are mode-independent, as are the caps on them (~5 impl, ≤7 reviewer).
- Mode handling spans `hunk-loop.md` (§ Modes), `plan-slices/SKILL.md`
  (§0 and §6), `agents/slice-reviewer.md` (Gather, Write findings, Return),
  `commands/slice-next.md`, and `commands/slice-approve.md`. A bare `hunk …`
  command added to any of them is a regression.
- Artifact filenames `01`–`05` appear in nearly every file, including the
  blind-reviewer's must-not-read list.
- The README's "The loop" and "Layout" sections mirror `commands/` and
  `skills/`; adding a command or skill means updating both.
- Interactive elicitation (`AskUserQuestion`) is the default way every skill and
  command puts a question to the human. The rule lives in `critical-inquiry.md`
  § How to ask and is restated at each decision point: the triage in
  `plan-product`, the gate line in all four skills and their commands, the Hunk
  install offer and the slice hand-off in `plan-slices`, and the finding triage
  in `commands/blind-review.md`. The mirror rule is in the three agent files —
  subagents have no channel to the human, so they name both branches and return
  the question upward rather than asking or guessing. A new question added to
  any file in prose form, or a subagent told to ask, is a regression.
- Artifact brevity lives in `artifact-conventions.md` § Length and duplication
  (the three bloat habits, the two-screen budget, the ten-line cap on Current
  state) and is restated where each is lost: the research step and the draft
  step of `plan-architecture` and `plan-program`, their two commands, and
  `agents/codebase-researcher.md` § Return findings, not tours. The rule that
  makes it safe is that the *feature directory* is the unit that stands alone,
  not the file — so anything loosening cross-references by path will bring the
  duplication straight back.
- Sketch checkpoints span `sketch-checkpoints.md` (the practice and the
  per-phase table), a "Sketch … in the conversation" step in all four
  `SKILL.md` files, a "draw before you write" line in all four phase commands,
  the timing rules in `critical-inquiry.md`, and the gate preamble in
  `artifact-conventions.md`. The per-phase checkpoint sequences are stated
  twice on purpose — the table in `sketch-checkpoints.md` and the numbered
  list in each skill — so adding or dropping a checkpoint means editing both.
  The two caps that keep this from becoming an interview are one checkpoint per
  section rather than per instance, and no checkpoint on sections that merely
  transcribe or follow from what is already settled.

**Skill `description:` frontmatter is the dispatch mechanism** — it is what makes
the model reach for the skill unprompted. These are long and trigger-heavy by
design; do not shorten them into summaries.

**Gates are load-bearing.** Every phase ends with a hard stop, and every command
file repeats it. Do not add "then continue to X" convenience to any phase.
Likewise: one slice per turn, self-healing capped at three attempts per failing
check, never fix a check by weakening a test or loosening types.

**Blind-reviewer isolation** is enforced only by prose, in three places
(`agents/blind-reviewer.md`, `commands/blind-review.md`, README). If you touch
what it may read, touch all three.

## Voice

The existing prose argues for its rules rather than asserting them — most sections
state the rule, then the failure it prevents. Match that. It is also deliberately
plain: no bold-per-sentence, no emoji, em-dash-and-comma prose, TypeScript as the
worked example while staying stack-agnostic. New instructions that read like a
checklist will be out of place.
