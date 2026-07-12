# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` attributes the item to Anand Pillay and Charles Steinhorn, dates
it to 1986, and states only "properties of o-minimal structures". Stage0 repeats that wording while
leaving definitions and assumptions open. The rev-5.6 manifest preserves `已验证` as explicitly
untrusted metadata. These records do not identify a theorem, page, proof, or formal artifact.

## Candidate primary source

Anand Pillay and Charles Steinhorn, *Definable sets in ordered structures. I*, Transactions of the
American Mathematical Society 295 (1986), 565-592, is the primary-source candidate matching the
repository's authors and year. The intake did not inspect an immutable scan, select an exact theorem
number/page, compare definitions, or audit corrections and errata. The bibliographic entry is a
discovery locator only and is not `H0` evidence.

The source audit must decide whether the intended item is the monotonicity theorem provisionally
scoped here or a different result from that paper. It must record exact wording, all assumptions,
parameter conventions, cited lemmas, and errata, followed by independent row-by-row review.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| o-minimal structure | ordered first-order structure whose definable unary sets are finite unions of points and intervals | language expansion, structure compatibility, `Set.Definable₁`, finite union/interval predicate | family identified; encoding open |
| properties | provisionally the unary definable-function monotonicity theorem | definable graph, finite partition, continuity, strict monotonicity | ambiguous; exact source theorem open |
| definable | definability with precisely the source's allowed parameters | formulas, realization, parameter encoding | pinned generic API exists; convention open |
| finite partition | points plus interval cells covering the function domain | finite set/list of cuts or finite family of pairwise-disjoint cells | representation open |
| monotone and continuous pieces | constant, strictly increasing, or strictly decreasing continuous restrictions | order topology, restriction, `StrictMonoOn`/`StrictAntiOn` or checked equivalent | conclusion API open |
| 1986 / Pillay-Steinhorn | bibliographic locator | no machine component and no proof credit | candidate paper identified only |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.ModelTheory.Definability` provides formula-based definability including
`Set.Definable₁`; `Mathlib.ModelTheory.Order` provides first-order languages and semantics for
orders; and the order library provides dense linear orders and interval sets. `IntakeProbe.lean`
checks representative names in the pinned environment.

The scoped repository and pinned-mathlib search found no named o-minimality predicate or
one-variable o-minimal monotonicity theorem. A legacy Pila-Wilkie discovery module independently
records o-minimality as an assumed predicate slot; it does not prove this target and receives no
credit. This negative local search is not a complete external anchor audit.
