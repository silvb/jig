# Critical inquiry

Shared by all four planning skills.

The human is asking for planning precisely because they want their thinking
stress-tested. A skill that transcribes their intent into a nicely formatted
document has done nothing for them. The value is in the questions that change
the artifact.

## Timing rules

**While drafting** — the questions that change the *shape* of the artifact
ride on the material, at checkpoints. A different set of screens, a different
contract, a different slice ordering: draw it, then ask about the drawing. See
`sketch-checkpoints.md` for the mechanics. This is the main channel and it has
no cap, because a checkpoint asks the human to react to something concrete
rather than to compose the drawing in their own head first.

**Blind, before there is anything to look at** — hard cap of three. Some
questions genuinely precede the material: you cannot sketch a workflow for a
feature whose user you have not established. Three of those, then draw
something. Past three you are interviewing, and the interview is what
checkpoints replace.

**At the gate** — everything else, batched into the Open questions section.
Edge cases, error handling, scale concerns. These refine an artifact that
already exists, so they cost the human nothing to defer. Expect this list to be
short: the shape questions were settled at the checkpoints, and a gate still
carrying six of them means the drawing came too late.

**Never ask** what a `codebase-researcher` subagent could answer by reading the
repository. "How does auth currently work?" is research, not inquiry. Go look.

**Never ask** a question you can answer with a default plus a flag. Prefer
"I assumed X — flagged in Assumptions" over stopping to ask. The gate exists
so assumptions get caught cheaply.

That last rule is about questions, not about drawings. A defaultable decision
still gets drawn — your default is what the sketch shows, and showing it is how
the human catches it in two seconds rather than at the gate. It is the *stop*
that a good default makes unnecessary, and only when nothing else in that
section is contestable either; see `sketch-checkpoints.md` § Which sections earn
one.

## How to ask

Ask through interactive elicitation — the `AskUserQuestion` tool — whenever the
question has nameable answers. A question buried in a paragraph of chat gets a
one-word reply that resolves half of it. The same question as three labelled
options gets answered exactly, in one keystroke, and the answer still reads
unambiguously to a cold agent going through the transcript later.

- **Options carry consequences, not just names.** "Medium — architecture merged
  into the product doc, program design skipped" is choosable; "Medium" is a
  quiz. If you cannot say what follows from an option, you do not understand it
  well enough to offer it.
- **Lead with your recommendation**, first in the list and marked
  `(Recommended)`. You have read the material. Withholding a view to look
  neutral hands the human work you have already done.
- **Batch.** Up to four questions go in a single call — ask them together
  rather than draining the human one round-trip at a time. Where answers are not
  exclusive, allow multiple selection.
- **Present the material first.** Elicitation replaces the question, not the
  context behind it. At a checkpoint the material is the drawing itself; at a
  gate it is the decisions, assumptions, and file path, printed in chat as usual
  with the open questions riding on top. A set of options with nothing to read
  against is unanswerable.
- **Where the fork is visual, make the options visual.** Two candidate
  wireframes or two candidate signatures belong in the per-option previews, not
  in prose above them (`sketch-checkpoints.md` § Draw variants when the fork is
  real).
- **Keep the escape open.** The human can always answer in free text, so an
  option set that misses their answer costs them nothing. Options they would
  never pick cost them attention, which is the scarce thing.

This changes how you ask, not how much. The timing rules above still hold —
three blind questions at most, shape questions on the material, everything else
batched to the gate — and so do both "never ask" rules. A cheaper interface is
not a licence to interview, and neither is a checkpoint: what makes a checkpoint
cheap is the drawing attached to it, so one with nothing to look at is just an
interview question wearing the name.

**A question is still a stop.** Offering options is not permission to act on the
one you recommended. Wait for the answer.

**Subagents cannot elicit.** `codebase-researcher`, `slice-reviewer`, and
`blind-reviewer` have no channel to the human. A question that surfaces inside
one travels back to the dispatching skill in its return value, and the skill
asks it. A subagent that answers on the human's behalf has invented a decision
and labelled it a finding.

## Product phase

- Who is explicitly *not* a user of this? What did we decide not to serve?
- What does the first-run and empty state look like? These get skipped and then
  designed badly under pressure.
- What does the user do when it fails? Not what the system does — what the
  person does next.
- What happens to users who are mid-flow when this ships?
- Which part of this could we cut and still get most of the outcome?
- How will we know it worked? If the success signal is unmeasurable, say so.

## Architecture phase

- What happens on partial failure — one write succeeds, the next does not?
- Is this operation safe to retry? If a client retries, what breaks?
- Who is allowed to do this, and where is that enforced?
- What happens when the underlying data is deleted?
- What does the migration and the rollback look like? Is the rollback real?
- What does this look like at 100× the expected volume? At zero?
- What is now coupled that was not coupled before?
- Does anything here make a decision in `01-product.md` look unbuildable, or far
  more expensive than it read?

## Program design phase

- What invariants must hold, and what enforces them?
- Where does state live, and who is allowed to mutate it?
- What does each signature say about empty, null, and error? If the type does
  not say, the caller will guess.
- What ordering is assumed? Is anything concurrent?
- Which of these seams is a one-way door?
- Which is the function that will be edited most often a year from now?
- Which decision in `02-architecture.md` do these signatures make look
  overbuilt? A seam that turns out to be one function is the usual one.

## Slices phase

- Which slice carries the real risk? Is it early enough?
- What cannot be proven until the last slice? That is the thing to pull
  forward.
- If we stopped after slice two, is the codebase in a coherent state?
- How does each slice get rolled back?
- Which slice is likely to reveal that the program design is wrong?

## Tone

Ask like a colleague who has read the plan carefully and wants it to work —
not like a checklist. One sharp question is worth six generic ones. If the plan
genuinely has no gaps at this phase, say that and move on; manufacturing
concerns to look thorough wastes the human's attention and teaches them to skim
the gate.

The same applies at a checkpoint. If the drawing has one obvious reading and no
fork worth putting up, show it, say that you see nothing contestable in it, and
go on to the next section. A checkpoint that exists only to prove you stopped is
worse than no checkpoint, because it trains the human to approve without
looking — and the whole practice runs on them looking.
