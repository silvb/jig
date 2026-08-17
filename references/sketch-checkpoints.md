# Sketch checkpoints

Shared by all four planning skills. Read alongside `artifact-conventions.md`
and `critical-inquiry.md`.

## Why

Every phase has a notation that carries its thinking — a workflow JSON, an
ASCII wireframe, a sequence diagram, a call-stack tree, a slice table. Drafted
the obvious way, that notation appears for the first time inside a finished
document, at the gate. By then the shape has already settled: the wireframe
implies the steps, the steps imply the acceptance criteria, and a human who
wanted a different second screen is now asking for a rewrite rather than a
change.

A gate can only accept or reject. It is the wrong instrument for steering, and
handing a human that instrument produces the two failure modes you actually
see — plans rubber-stamped because contesting them is expensive, and plans
rejected wholesale after twenty minutes of reading.

So the notation moves into the conversation. Draw each section where the human
can react to it, settle it, then draw the next. The document gets written last,
from pieces that are already agreed. That makes the gate a confirmation rather
than a reveal, which is the intent and not a loss.

## The checkpoint

One section, three parts:

1. **The material, drawn in full, in chat.** The real notation at its real
   fidelity — the actual box-drawing wireframe, the actual JSON, the actual
   signature. Not a description of what you are about to draw, and not a
   placeholder you intend to fill in later. A human cannot react to a promise.
2. **One elicitation**, on whatever is most likely wrong about what you just
   drew. Options carrying consequences, your reading first, per
   `critical-inquiry.md` § How to ask.
3. **Stop.**

Then take the answer, redraw only what it changed, and move to the next
section.

## Which sections earn one

A section earns a checkpoint if it has a shape the human could reasonably want
different.

Two kinds do not. Sections that transcribe what the human already told you —
the problem, who it is for — have nothing to contest, and showing them back is
theatre. Sections that fall out of decisions already settled — out of scope,
deferred notes, the current-state summary — are consequences, not choices. Both
go into the draft and are presented at the gate as usual. Checkpointing one of
them is padding, and padding is how this practice earns the reputation the cap
in `critical-inquiry.md` exists to prevent.

## Per phase

| Phase | Checkpoints, in order |
|---|---|
| 1 Product | workflow JSON · wireframes · acceptance criteria |
| 2 Architecture | flow diagram · contract · data model · failure modes |
| 3 Program design | call stacks · file tree · signatures · test plan |
| 4 Slices | the slice table and its ordering · the Verify blocks |

This is a default ordering, not a quota. A phase whose material is genuinely
settled in one drawing gets one checkpoint.

## One checkpoint per section, not per instance

A section with several instances — five wireframe states, three call stacks, a
table of failure modes — is drawn in a single checkpoint, all instances
together. States are read against each other; the empty state is only wrong
relative to the loaded one. Drip-feeding them one per turn is how this
degenerates into an interview, which is the failure this practice is otherwise
a way around.

## Draw variants when the fork is real

Where you genuinely have no recommendation — two layouts, two contract shapes,
two orderings — draw it both ways and make the drawings themselves the options,
in the elicitation's per-option preview. A human picks between two wireframes
in a keystroke. Critiquing one into becoming the other costs them a paragraph,
and usually does not happen; they take the one on screen.

This is for real forks. Manufacturing a variant you do not believe in, so as to
look even-handed, spends the same attention as an unnecessary question.

## Collapsing it

If the human says to just draft the thing, draft it. Collapse to one checkpoint
carrying the whole skeleton, take the reaction, and go to the gate. This exists
to keep them in the loop; a human asking to be let out of it is the loop
working, not a rule to argue with.

## What the artifact still records

The document remains the loop's state — see `artifact-conventions.md`
§ Resumability test. Material settled at a checkpoint was settled in chat, which
means it is lost unless it lands in the file. Write the agreed drawing into the
artifact as drawn, and where a checkpoint turned on a real fork, record the
rejected alternative in one line — "chose X over Y because Z", per
`artifact-conventions.md` § Record decisions, not the work. One line is what
stops the next cold agent re-proposing it; re-running the argument on the page
is recording the checkpoint rather than its outcome.

A cold agent reading the finished artifact should not be able to tell which
sections were checkpointed and which were not.
