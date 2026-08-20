# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`jig` is a Claude Code **plugin** — almost entirely prose. There is no build, no
test suite, no dependencies. Nearly every file is Markdown instructions or a JSON
manifest, and the "program" is the behaviour those instructions produce in an
agent. Changes are reviewed by reading them, not by running them.

Consequence: correctness here means *internal consistency across files*. The same
rule is usually stated in three or four places on purpose (skill, command, agent,
reference), so a change is not done until every copy agrees.

The one exception is `hooks/`, which is executable and therefore is reviewed by
running it. Code earns a place here only where a rule has to hold *every* time
and a model can simply forget — `unwrap-artifacts.py` is the whole of it. Prefer
prose, and reach for a hook only after prose has been tried against a real
feature and lost.

## Commands

```bash
claude plugin validate .          # manifest check (marketplace + plugin.json)
claude plugin details jig         # component inventory + projected token cost
claude plugin tag .               # cut a {name}--v{version} release tag
./hooks/test-unwrap.sh            # the only executable file, the only real test
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
hooks/            the one deterministic rule, auto-loaded with the plugin
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
| (end) Retire | — | the whole directory is deleted; live follow-ups move into the repo |

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

**When the two purposes conflict, the human wins.** An artifact is both a
reviewable document and the state a cold agent resumes from, and those pull
apart often enough that `artifact-conventions.md` § Why these conventions exist
ranks them. Reach for it whenever a rule would make a document more complete for
the next agent at the cost of the human's ability to hold it in their head — the
human is the one who re-steers the next phase, so their comprehension is what
recovers from everything else going wrong.

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
  install offer and the slice hand-off in `plan-slices`, the finding triage in
  `commands/blind-review.md`, and the retirement offer with its
  where-does-the-note-go question in `commands/retire.md`. The mirror rule is in the three agent files —
  subagents have no channel to the human, so they name both branches and return
  the question upward rather than asking or guessing. A new question added to
  any file in prose form, or a subagent told to ask, is a regression.
- Scope of an artifact is owned by `artifact-conventions.md` § The delta, not
  the system — the third sibling of the two brevity sections below, and the one
  that governs *what surface* is covered rather than what goes in or how much.
  It is restated in `commands/product.md`, `commands/architecture.md`, and
  `commands/program.md`, in the draft step of all three planning skills, at the
  screens checkpoint of `plan-product`, at the flow checkpoint of
  `plan-architecture`, and in `ascii-wireframes.md` § Existing components, which
  owns the concrete form (an existing component is one labelled box with a
  citation). It exists because the brevity rules do not reach the drawings —
  drawings are explicitly outside the two-screen budget, so over-architecting
  migrates into them: wireframes of components the project already ships,
  sequence diagrams of the system rather than the seam. Its argument has two
  halves and both are load-bearing: a description of existing code goes stale
  invisibly and is trusted anyway, and the next agent does not need it because
  it reads the repo itself. The second half is what keeps the rule from being
  softened into "summarise the codebase briefly" — an agent that cannot orient
  itself in a repo is a gap in *that repo's* `CLAUDE.md`, which jig does not
  fix.
- Artifact brevity is two sibling sections of `artifact-conventions.md`.
  § Record decisions, not the work governs *what* goes in — outcomes rather than
  the investigation, one line per rejected alternative, and omit template
  sections that do not apply. § Length and duplication governs *how much* — the
  three bloat habits, the two-screen budget, the ten-line cap on Current state.
  Both are restated where each is actually lost: the research and draft steps of
  `plan-architecture` and `plan-program`, the draft step of `plan-product`,
  `commands/architecture.md` and `commands/program.md`, and
  `agents/codebase-researcher.md` § Return findings, not tours.
  Three carve-outs keep omission from deleting signal: Out of scope and Failure
  modes get a sentence rather than a deletion when empty, because their
  emptiness is a finding, and each is stated with its section (`plan-product`,
  `plan-architecture`); and a section another artifact cites by name
  (`§ Contract`, `§ Decisions`) goes only when the thing itself does not exist,
  which is restated for Decisions in `plan-program` and nowhere for Contract,
  because phase 2 without a contract is not a case worth defending against.
  The rule that makes the whole thing safe is that the *feature directory* is
  the unit that stands alone, not the file — so anything loosening
  cross-references by path brings the duplication back.
  The templates in the four skills are menus, not forms; an edit that reads
  as "always render every section" is a regression.
- The commit strategy is owned by `artifact-conventions.md` § What gets
  committed and restated at the tail of all four skills' gate steps and all four
  phase commands. One commit per phase, at that phase's gate, carrying
  `status: approved`; one commit per slice, code and plan edits together. Both
  are pushed — approval means commit and push everywhere in the loop, and
  nothing else. The part that is easy to lose in an edit is that the commit
  *closes* a gate and does not open the next one — a skill that reads
  "approve, commit, continue" has removed the gate while appearing to strengthen
  it, which is the failure the § Gates rule exists to prevent. The other part is
  that an upstream amendment rides in the commit of whatever motivated it,
  stated here, in § Amending an upstream artifact, in `plan-architecture` and
  `plan-program`'s gate steps, and in `plan-slices` § 6 step 4.
- Retirement is owned by `artifact-conventions.md` § Retiring the plan and
  driven by `commands/retire.md`, with the hand-offs in `commands/blind-review.md`
  (offer it once the triage leaves nothing outstanding) and `plan-slices`
  § After the last slice and § Resuming cold. The end state of the loop is that
  the feature directory does not exist. Three parts travel together and each
  fails differently if dropped: the deletion is safe only because every phase
  committed at its gate, so `git log -- <path>` still holds the plan — an edit
  that weakens the commit rule makes this destructive; what is still live
  (unmeasured outcome signal, deferral, accepted finding, named v2) is carried
  into wherever the repo already keeps future work, found by looking and asked
  for when nothing is found, never invented as a new directory; and the note is
  compact, or absent when nothing survives, because a manufactured follow-up
  note restarts the staleness it was meant to end. Note the interaction with
  § What gets committed: accepted-with-reason findings live in
  `03-program-design.md` § Decisions until retirement and have to leave the
  directory with it, or they die with the file that held them.
- Artifact line wrapping is stated in `artifact-conventions.md` § No hard
  wrapping and enforced by `hooks/unwrap-artifacts.py`, auto-loaded from
  `hooks/hooks.json` with no user settings involved. Two things in that script
  are load-bearing beyond their size. Its scope guard — path contains
  `docs/plans/` and ends `.md` — is all that keeps a plugin-shipped hook from
  reformatting files in repos that never asked for jig's conventions; widening
  it is a regression. And the `additionalContext` it prints on a rewrite is what
  stops the model's next `Edit` being written against line breaks the hook just
  removed, so a "quieter" version that drops the notice trades a cosmetic win
  for failed edits. It fails open by design: every error path exits 0. Run
  `./hooks/test-unwrap.sh` after touching it — this is the one file here that
  reading does not verify.
- Upstream amendment is owned by `artifact-conventions.md` § Amending an
  upstream artifact, and restated wherever a phase meets a document it did not
  write: the intro of `plan-architecture` and `plan-program`, Part A's cut and
  Part B step 1 of `plan-slices`, all four of those commands, and
  `agents/slice-reviewer.md` § What you are looking for. The three parts that
  travel together are that the conflict is *surfaced* rather than routed around
  (silent amendment and silent contradiction are the two failures, and both need
  naming), that the amendment reaches every downstream artifact or says which it
  did not, and that it rides in the commit of the work that motivated it. The
  question that surfaces it is in `critical-inquiry.md` under phases 2 and 3. An
  edit that turns this into "later phases may not change earlier artifacts"
  breaks the loop's only path out of a wrong plan; one that lets a phase amend
  without asking breaks the gate.
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
