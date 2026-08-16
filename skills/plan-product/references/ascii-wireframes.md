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
