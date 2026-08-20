# ASCII wireframes

A wireframe settles a layout argument that three paragraphs would only prolong.
It is committed and diffed like everything else, so the format is chosen for
diff stability as much as for readability.

## Rules

**72 columns, fixed.** Every wireframe in the document uses the same canvas
width. Reflowing to fit content makes every subsequent edit touch every line,
which turns a one-word change into an unreadable diff.

**Box-drawing characters:** `┌ ─ ┬ ┐ │ ├ ┼ ┤ └ ┴ ┘`. Plain ASCII (`+-|`) is
acceptable if the target environment mangles Unicode, but pick one per document
and stay with it.

**One wireframe per state.** Empty, loading, loaded, error, and any meaningful
variant get their own box. A single annotated composite hides exactly the
states that get built badly — do not produce one.

**Numbered callouts.** Mark interaction points inline as `[1]`, `[2]` and
explain them in a legend below the box. Keep the boxes visually clean; put the
behaviour in the legend where it can be edited without redrawing.

**Content is representative, not lorem.** Real-looking labels expose length
problems that placeholder text hides.

## Existing components

A wireframe settles an argument about something not yet decided. A component
the project already ships is not that, so it is drawn as a single labelled box
naming it and citing where it lives, and the fidelity goes into what is new
around it:

```
┌──────────────────────────────────────────────────────────────────────┐
│  Drafts                                          [1] + New draft     │
├──────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  <DraftTable>  src/components/draft-table.tsx:1            [2] │  │
│  └────────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Publish confirm — new                                         │  │
│  │  Publishing sends this to 1,240 subscribers.                   │  │
│  │                              [3] Cancel      [4] Publish now   │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

**Legend**

1. Unchanged.
2. Existing table, unchanged except that rows now carry a Published badge.
3. Dismisses; the draft stays a draft.
4. The new action. Disabled while the confirm is in flight.

Two things go wrong when the existing component is drawn out instead. The
picture is a snapshot of something that shipped months ago and will drift from
it silently, which is the general case in `artifact-conventions.md` § The delta,
not the system. And redrawing invites redesigning: a shipped component rendered
in a planning document reads as a proposal, and the next four turns go to a
table nobody asked to change. Where the feature genuinely does change it, that
change is the new part — draw the change, and say in the legend which component
it edits.

The same holds for a state that is already implemented. Draw the states this
feature adds or alters; an existing empty state gets a line in the legend
saying it is unchanged, not a box of its own.

## Example

### State: loaded

```
┌──────────────────────────────────────────────────────────────────────┐
│  Drafts                                          [1] + New draft     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ Migrating the widget registry            edited 2h ago     [2] │  │
│  │ Draft · 1,240 words                          [3] Publish  ···  │  │
│  └────────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ Notes on Drizzle relations               edited yesterday  [2] │  │
│  │ Draft · 310 words                            [3] Publish  ···  │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  Showing 2 of 2                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**Legend**

1. Opens the composer. Disabled while a draft is saving.
2. Row click opens the draft. Whole row is the target, not just the title.
3. Publish is inline; opens the confirm step rather than publishing directly.

### State: empty

```
┌──────────────────────────────────────────────────────────────────────┐
│  Drafts                                          [1] + New draft     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│                        Nothing here yet.                             │
│              Your first draft saves automatically.               [1] │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**Legend**

1. Same action as the header button; the empty state repeats it as the primary
   call to action.

## Editing an existing wireframe

Change the affected lines only. If a change would reflow the whole box, that is
a signal the layout changed materially — say so at the gate rather than quietly
redrawing, because the human is about to see a diff that looks like a rewrite
and should know why.

## Non-visual features

Features with no UI still need this section, but the artifact is different: for
a CLI, the exact terminal session including the output; for an API, the request
and response as the consumer will experience them. The principle holds — show
the surface the user meets, do not describe it.
