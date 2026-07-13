# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:6749-6754` supplies exactly the title `贝尔数`, attribution Eric
Bell, year 1934, gloss `集合划分的计数`, importance `高`, and status `已验证`. Git history attributes
all six uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains
no formula, bibliography, definition, ordered binders, assumptions, conclusion, proof locator,
correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:25174-25199` repeats the gloss while explicitly leaving the formal system,
logical foundation, exact definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links unresolved. The rev-5.6 manifest records rank 1465,
baseline `L0 / rework_required`, no legacy slot, `lifecycle_mode: planned`, and
`theorem_complete: false`. Its `已验证` field is explicitly untrusted.

## Literal crosswalk

| Repository component | Mathematical information fixed | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `贝尔数` | the conventional Bell-number subject | `Nat.bell` or a future cardinality-defined sequence | recognizable object family, not a proposition |
| `集合` | a finite labeled carrier is conventionally intended | `Fin n`, `Fintype`, or a finite set | carrier and equivalence transport absent |
| `划分` | decomposition into unordered nonempty blocks covering the carrier | setoids, equivalence relations, or `Finpartition` | representation and equality absent |
| `计数` | a natural-number cardinality or identity is intended | `Fintype.card` or an equivalent finite enumeration | exact equality and sequence definition absent |
| Eric Bell / 1934 | historical attribution metadata | provenance only | likely bibliography found, but no cited passage or proof mapping |
| `已验证` | untrusted inventory value | accepted source and kernel receipts would be required | no H or M completion credit |

## Modern mathematical scope reference

NIST Digital Library of Mathematical Functions, version 1.2.7 (release 2026-06-15), Chapter 26,
Section 26.7(i), *Set Partitions: Bell Numbers*, was inspected on 2026-07-13. It says `B(n)` is the
number of partitions of `{1,2,...,n}` and gives `B(0) = 1`. The same section gives
`B(n) = sum S(n,k)` and a Dobinski-type formula; later subsections give the exponential generating
function and the recurrence

```text
B(n+1) = sum_{k=0}^n choose(n,k) B(k).
```

DLMF notes Comtet (1974), pages 210-211, for the definition section and records a historical erratum
for equation 26.7.6: the summand originally used `B(n)` where the corrected recurrence uses `B(k)`.
This is a strong modern definition and statement-family reference, but not `H0`: no complete proof
and incorporated-definition map was admitted, the cited book pages were not inspected, the
catalog-to-formula choice is still absent, and no independent source review exists.

## Historical bibliographic lead

Crossref metadata identifies E. T. Bell, "Exponential Numbers," *The American Mathematical
Monthly* 41(7) (August 1934), pages 411-419, DOI
`10.1080/00029890.1934.11987615`. The author, year, and subject title make it a plausible lead for
the catalog attribution. Publisher and JSTOR PDF requests were blocked, so the article's statement,
definitions, proof, pages, corrections, and relationship to the modern set-partition convention
were not inspected. The citation is discovery metadata only, not primary proof evidence or H0.

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Combinatorics.Enumerative.Bell` exposes:

| Declaration | Candidate role | Boundary |
|---|---|---|
| `Nat.bell` | recursively defined standard Bell-number sequence | exact-topic definition, but not a partition-cardinality type |
| `Nat.bell_succ`, `Nat.bell_succ'` | recurrence candidates | follow from the recursive definition; do not prove its counting interpretation |
| `Nat.bell_zero`, `bell_one`, `bell_two` | boundary values | special values only |
| `Multiset.bell` | formula for partitions with a prescribed multiset of block sizes | refined arithmetic definition, not unrestricted partition cardinality |
| `Multiset.bell_mul_eq` | factorial identity for that refinement | exact formal theorem with a different conclusion |
| `Nat.uniformBell` and related lemmas | equal-size block specialization | restricted partition shape, not the catalog root |

The Bell module itself explicitly marks as TODO proving that its definitions actually count the
indicated partitions, including connecting `Nat.bell n` to the relevant sum of `Multiset.bell`
values. Thus module prose is not kernel evidence for the literal set-partition-counting claim.

Pinned module `Mathlib.Combinatorics.Enumerative.Stirling` defines `Nat.stirlingSecond` recursively
and describes it as counting partitions into exactly `k` nonempty subsets. It supplies recurrence
and boundary interfaces, but no checked bridge in the inspected Bell module proves the desired
Bell cardinality theorem. `IntakeProbe.lean` authenticates these exact definitions, statements, and
candidate trust reports only. The provisional machine status is `M3`, not `M0-W`.

## Source gate

Before statement work can close, independent reviewers must select one preserved proposition,
approve its definition and source locator, map every carrier/partition/cardinality convention,
ordered binder, hypothesis, conclusion, boundary case, dependency, correction, and erratum, and
authorize checked Lean transports. Until then the DLMF identities and pinned mathlib declarations
are uncredited candidates rather than a broadened or substituted theorem.
