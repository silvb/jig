# Contract design

The contract is the highest-leverage artifact in the architecture phase,
because it is the thing multiple parts of the system must agree on and the
thing that is most expensive to change after code exists on both sides.

## Format: plain types plus a route table

No schema toolchain, no code generation, no new dependency. A contract that
requires installing something will not get written for the small features, and
the small features are where this habit either sticks or dies.

### Route table

```markdown
| Method | Path                    | Auth        | Request        | Response       |
|--------|-------------------------|-------------|----------------|----------------|
| POST   | /api/drafts             | session     | CreateDraft    | Draft          |
| POST   | /api/drafts/:id/publish | session     | —              | Draft          |
| GET    | /api/drafts             | session     | ListDraftQuery | DraftSummary[] |
```

The auth column is not decoration. Making it explicit per route catches the
endpoint that quietly has none.

### Types

```ts
type DraftId = string & { readonly __brand: 'DraftId' }

type DraftStatus = 'draft' | 'published' | 'archived'

interface Draft {
  id: DraftId
  title: string
  body: string
  status: DraftStatus
  publishedAt: string | null   // ISO 8601; null unless status === 'published'
  updatedAt: string
}

interface CreateDraft {
  title: string
  body?: string                // defaults to empty
}

interface ListDraftQuery {
  status?: DraftStatus
  cursor?: string
  limit?: number               // 1-100, defaults to 20
}
```

### Errors

Error shapes are part of the contract and get left out of roughly every
contract ever written.

```ts
interface ApiError {
  code: 'not_found' | 'forbidden' | 'conflict' | 'validation'
  message: string              // safe to display
  fields?: Record<string, string>   // validation only
}
```

| Status | code       | When                                    |
|--------|------------|-----------------------------------------|
| 400    | validation | Request failed schema validation        |
| 403    | forbidden  | Actor may not act on this draft         |
| 404    | not_found  | No draft with this id visible to actor  |
| 409    | conflict   | Already published                       |

## What makes a contract reviewable

**Say what null means.** `publishedAt: string | null` is ambiguous until the
comment says when it is null. The consumer will otherwise guess, and guess
wrong at the worst moment.

**Say what is optional versus nullable.** These are different and mixing them
produces a class of bug that is tedious to find.

**Brand identifiers.** `DraftId` rather than `string` costs one line and
prevents passing a user id where a draft id belongs. Skip it if the codebase
does not already do this — matching local convention beats importing a better
one mid-feature.

**State the pagination and limit rules in the type comment**, because they are
contract, not implementation.

## Other stacks

The format is the point, not the language. The same table plus type block works
for:

- **Go / Rust / Python**: struct or dataclass definitions, same annotations.
- **GraphQL**: SDL for the new types and fields, plus which resolvers are new.
- **Events and queues**: message name, payload type, producer, consumers,
  ordering and delivery guarantees, and what a duplicate delivery does.
- **CLI**: the command signature, flags, exit codes, and stdout shape.

If the repository already has a schema source of truth — an OpenAPI file, a
protobuf definition, a Zod schema module — write the contract in that instead
and cite it. Two sources of truth for one contract is worse than an
unfashionable format.
