# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:4587-4592` records the Chinese title `海涅-博雷尔定理`,
attribution Eduard Heine/Emile Borel, year 1895, gloss `R^n中有界闭集等价于紧集`, high
importance, and status `已验证`. Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record supplies no bibliography, formula,
dimension convention, definitions, theorem/page, proof passage, translation, errata record,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:16909-16934` repeats the gloss while explicitly leaving exact definitions
and premises, proof route, dependencies, alternate forms, axioms, machine status, and artifact
links open. The rev-5.6 manifest retains `已验证` only as untrusted metadata and resets this target
to `L0 / rework_required`.

No immutable primary or authoritative edition, pinpoint proposition, complete premise and proof
crosswalk, correction audit, or independent review is available in the repository. The familiar
truth-valued family and historical attribution support provisional `H1`, not `H0`.

## Literal component crosswalk

| Catalog component | Conventional mathematical reading | Prospective Lean surface | Intake result |
|---|---|---|---|
| `R^n` | finite-dimensional real Euclidean space | `EuclideanSpace Real (Fin n)` or `Fin n -> Real` | dimension range and encoding open |
| set, implicit in "closed/bounded/compact" | an arbitrary subset of the ambient space | `s : Set (EuclideanSpace Real (Fin n))` | binder order open |
| bounded | metric boundedness, equivalent in finite dimension to coordinatewise boundedness | `Bornology.IsBounded s` | source definition and alternate transports open |
| closed | closed in the Euclidean topology | `IsClosed s` | topology must be bound to the selected carrier |
| compact | every open cover has a finite subcover, represented by topological compactness | `IsCompact s` | source definition and foundation boundary open |
| equivalent | both compact-to-closed-bounded and closed-bounded-to-compact directions | `IsCompact s <-> IsClosed s and Bornology.IsBounded s` | conventional candidate only |
| `已验证` | untrusted inventory label | accepted source and kernel receipts | no credit |

A conventional candidate root is therefore:

```text
for every natural n and every subset s of Euclidean real n-space,
s is compact if and only if s is closed and bounded.
```

This prose is a resolution target, not an admitted quotation or frozen canonical statement.

## Pinned Lean candidate crosswalk

Pinned mathlib module `Mathlib.Topology.MetricSpace.Bounded` describes
`Metric.isCompact_iff_isClosed_bounded` as the Heine-Borel theorem. Its type is universe-polymorphic
over a proper Hausdorff pseudometric space and an arbitrary subset. The two directions use
`IsCompact.isClosed`, `IsCompact.isBounded`, and `Metric.isCompact_of_isClosed_isBounded`.

| Declaration | Exact-topic role | Identity boundary |
|---|---|---|
| `Metric.isCompact_iff_isClosed_bounded` | direct compact iff closed-and-bounded theorem | generalized proper-space root; checked `R^n` specialization not frozen |
| `Metric.isCompact_of_isClosed_isBounded` | closed and bounded implies compact | only one direction of the catalog equivalence |
| `IsCompact.isClosed` | compact implies closed in a Hausdorff space | general forward-direction ingredient |
| `IsCompact.isBounded` | compact implies bornologically bounded in the metric setting | general forward-direction ingredient |
| `FiniteDimensional.proper` | finite-dimensional spaces over locally compact normed fields are proper | supplies the key Euclidean specialization premise, not the root |
| `Bornology.IsBounded.isCompact_closure` | bounded closure is compact in a proper space | related consequence, not the equivalence root |

`IntakeProbe.lean` authenticates these declarations in the pinned environment and prints axiom
reports for the direct equivalence and finite-dimensional properness theorem. That supports API
discovery only. It does not provide a source-approved expression, checked specialization, terminal
proof-body audit, or accepted proof receipt.

## Source and statement gates

Before H0, accountable reviewers must admit and hash an exact source edition, pinpoint the theorem
and incorporated definitions, map the dimension convention, every premise, both directions, and
all boundary cases, audit attribution, translation, corrections and errata, and independently
approve fidelity to THM-M-0618. Before statement acceptance, the selected claim must be elaborated
with minimal pinned imports, serialized and fingerprinted, connected to alternate encodings and the
proper-space candidate by checked declarations, and pass removed-hypothesis, changed-domain,
binder-scope, and boundary-case mutations. Exhaustive anchor, provenance, trust, and proof-body
audits remain later work.
