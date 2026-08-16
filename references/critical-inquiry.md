# Critical inquiry

Shared by all four planning skills.

The human is asking for planning precisely because they want their thinking
stress-tested. A skill that transcribes their intent into a nicely formatted
document has done nothing for them. The value is in the questions that change
the artifact.

## Timing rules

**Before drafting** — ask only questions whose answers change the *shape* of
the artifact: a different set of screens, a different contract, a different
slice ordering. Hard cap of three. More than three and you are interviewing
rather than drafting.

**At the gate** — everything else, batched into the Open questions section.
Edge cases, error handling, scale concerns. These refine an artifact that
already exists, so they cost the human nothing to defer.

**Never ask** what a `codebase-researcher` subagent could answer by reading the
repository. "How does auth currently work?" is research, not inquiry. Go look.

**Never ask** a question you can answer with a default plus a flag. Prefer
"I assumed X — flagged in Assumptions" over stopping to ask. The gate exists
so assumptions get caught cheaply.

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

## Program design phase

- What invariants must hold, and what enforces them?
- Where does state live, and who is allowed to mutate it?
- What does each signature say about empty, null, and error? If the type does
  not say, the caller will guess.
- What ordering is assumed? Is anything concurrent?
- Which of these seams is a one-way door?
- Which is the function that will be edited most often a year from now?

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
