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

## Gates

Every phase ends with a hard stop. The stop is the entire point of the phase —
a phase that flows straight into the next one has bought nothing.

At the gate, present in chat (not the full document — the human reads that in
their diff viewer):

1. **Contestable decisions** — 3 to 6 bullets, each in the form "chose X over
   Y because Z". A decision with no plausible alternative is not contestable
   and does not belong here.
2. **Assumptions and inventions** — everything filled in without being told.
   This is where wrong plans get caught.
3. **Open questions** — batched from critical inquiry, and asked through
   interactive elicitation rather than as prose, so the human answers by
   choosing rather than by composing (see `critical-inquiry.md` § How to ask).
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
file.

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
