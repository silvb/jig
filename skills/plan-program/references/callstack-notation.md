# Call-stack and file-tree notation

Light pseudocode visualisations, not diagrams. Diagram tooling looks more
rigorous and communicates less: a sequence diagram can be entirely correct
while hiding the fact that the third call is inside a loop.

## Call-stack trees

Indentation is the stack. Diff markers show what changes.

```
 publishDraft (route handler)
   requireSession
+  DraftService.publish(id, actor)
+    assertCanPublish(draft, actor)          -> throws Forbidden
+    Store.tx
+      Store.updateStatus(id, 'published')
+      Store.insertRevision(id, body)
+    emit('draft.published', { id })
-  legacyPublish
     renderResult
```

Markers: `+` added, `-` removed, `~` changed behaviour but same call, unmarked
lines are existing context. Unmarked context is what makes the diff readable —
a tree of only `+` lines tells the reviewer nothing about where the new code
attaches.

Annotate what a reader cannot infer:

```
+  processBatch(items)
+    for each item:                          -- sequential; order matters
+      transform(item)                       -> Result<Item, Error>
+    collectErrors                           -- partial success is allowed
```

Show loops, concurrency, and error exits. These are exactly the things that get
implemented wrong and reviewed too late.

One tree per entry point that changes. Do not merge unrelated flows.

## File-tree diffs

Keeps the human in touch with where things live, which is where most
maintainability decay starts.

```
 src
 ├── draft
+│   ├── draft-service.ts        # NEW — publish/unpublish, permission checks
+│   ├── draft-service.test.ts   # NEW — publish paths incl. conflict
~│   ├── draft-store.ts          # MODIFIED — add updateStatus, insertRevision
 │   └── draft-types.ts
 └── routes
~    └── drafts.ts               # MODIFIED — wire publish endpoint
```

Every new file gets a one-line purpose. If the purpose needs a comma-spliced
list of responsibilities, the file is doing too much — that is the signal this
notation exists to produce.

Every modified file names what changes, not just that it changes.

## Signatures

Declarations only. Bodies are implementation and belong to the slice.

```ts
type PublishError =
  | { kind: 'forbidden' }
  | { kind: 'conflict'; publishedAt: string }

interface PublishResult {
  draft: Draft
  revisionId: string
}

declare function publish(
  id: DraftId,
  actor: ActorId,
): Promise<Result<PublishResult, PublishError>>

declare function assertCanPublish(draft: Draft, actor: ActorId): void
```

What to include: anything a caller must understand, anything crossing a module
boundary, and anything where the error shape is a design decision. What to
leave out: private helpers, obvious getters, anything the implementer will
choose freely without consequence.

The value is in the types, not the names. A signature that returns
`Promise<any>` has recorded no decision at all.

## Test plan

Names only:

```
draft-service.test.ts
  publishes a draft and records a revision
  rejects publish when actor lacks permission
  returns conflict when already published
  leaves status unchanged when revision insert fails
```

Naming the tests before writing them settles what "done" means, and it makes
the one that is missing conspicuous. The fourth test above is the kind that
gets skipped and is the reason the failure-modes table exists.
