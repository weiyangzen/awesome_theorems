# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6784-6789` supplies exactly the title `波利亚计数定理`, attribution
to George Pólya, year 1937, gloss `考虑对称性的计数`, importance `高`, and status `已验证`. Git
history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The entry contains no formula, bibliography,
definitions, domain, ordered binders, hypotheses, conclusion, proof locator, translation,
correction record, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:25309-25334` repeats the gloss while explicitly leaving exact definitions
and premises, formal system, foundation, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links unresolved. The rev-5.6 manifest records rank 1467, baseline
`L0 / rework_required`, no legacy slot, `lifecycle_mode: planned`, and
`theorem_complete: false`. Its `已验证` field is explicitly untrusted.

## Catalog clause crosswalk

| Catalog component | Mathematical information fixed | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `考虑对称性` | a symmetry action and quotienting are intended | `MulAction`, `MulAction.orbitRel`, a future coloring action | acting objects, action direction, faithfulness, and quotient are absent |
| `计数` | an enumerative conclusion is intended | `Fintype.card`, finite sums, or a polynomial coefficient | orbit total versus inventory-refined generating expression is absent |
| `波利亚计数定理` | conventional theorem-family name | future canonical expression plus checked transports | name cannot choose among several nonidentical variants |
| George Pólya / 1937 | author/year metadata | none | primary bibliographic lead identified, but no admitted pinpoint statement |
| `已验证` | untrusted inventory value | accepted source and kernel receipts would be required | no H or M completion credit |

## Primary bibliographic lead

Crossref metadata for DOI `10.1007/BF02546665` was inspected on 2026-07-13. It identifies:

- G. Pólya, *Kombinatorische Anzahlbestimmungen für Gruppen, Graphen und chemische Verbindungen*;
- *Acta Mathematica* 68 (1937), pages 145-254;
- DOI `10.1007/BF02546665` and Project Euclid resource `euclid.acta/1485888172`.

The observed Crossref response is recorded by digest in `instance.json`. Semantic Scholar and
Unpaywall independently exposed the same Project Euclid PDF lead. Direct requests in this run
returned access-control HTML rather than the article PDF, so no paper text was admitted. In
particular, there is no theorem/formula/page locator, premise-to-conclusion map, proof-node map,
translation audit, correction/errata determination, or independent source review. This is an `H1`
bibliographic lead, not `H0`.

## Candidate mathematical family crosswalk

| Candidate clause | Conventional mathematical role | Source status | Lean status |
|---|---|---|---|
| finite positions and finite symmetry group | objects being permuted | expected but not pinpoint-mapped | adjacent finite group-action APIs exist |
| colors and colorings | configurations being counted | unrestricted versus inventory-weighted choice unresolved | no canonical coloring action selected |
| coloring orbits | equivalence classes modulo symmetry | expected but exact quotient/count convention unresolved | `MulAction.orbitRel` is an adjacent quotient relation |
| fixed colorings of each group element | Burnside summand | expected proof bridge | `MulAction.fixedBy` and Burnside's lemma exist |
| cycle decomposition of the position permutation | evaluates each fixed-coloring count | expected Pólya-specific refinement | `Equiv.Perm.cycleType` exists, but no bridge is credited |
| cycle-index substitution or coefficient extraction | inventory-refined conclusion | variant-dependent | no exact pinned Pólya declaration located in the bounded intake query |

The table is a scope crosswalk only. None of these rows is accepted as the canonical source
statement or a proof obligation registry.

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

| Declaration | Exact adjacent role | Boundary |
|---|---|---|
| `MulAction.sum_card_fixedBy_eq_card_orbits_mul_card_group` | Burnside's finite orbit-counting identity | separate `THM-M-0929` root and only a prospective ingredient here |
| `MulAction.sigmaFixedByEquivOrbitsProdGroup` | equivalence underlying the Burnside count | no cycle-index or coloring evaluation |
| `MulAction.orbitRel`, `MulAction.fixedBy` | orbit and fixed-point vocabulary | generic action infrastructure only |
| `Equiv.Perm.cycleType` | multiset of nontrivial cycle lengths | fixed points are represented separately from this multiset |
| `Equiv.Perm.card_fixedPoints` | relates fixed positions to support/cycle information | not the number of fixed colorings and not Pólya enumeration |

`IntakeProbe.lean` authenticates these declarations and prints candidate axiom reports with the
existing pinned toolchain. It is not a local Pólya wrapper. A bounded repository and pinned-mathlib
text query located no declaration named for Pólya enumeration or cycle index; that query is not an
immutable exhaustive anchor audit or a proof of absence.

The exact Burnside declaration and cycle APIs justify provisional `M3` infrastructure status, not
`M0`: the source-matched Pólya root, coloring action, fixed-coloring cycle formula, cycle-index
substitution, terminal proof body, provenance, and trust closure are all open.

## First failed statement/source gate

Before statement work can close, independent reviewers must admit a preserved source and select
one exact theorem variant, then map every object, binder, premise, conclusion, boundary case, and
source correction into a mutation-tested Lean expression. Until then the primary metadata and
pinned APIs are discovery leads, not a broadened, narrowed, or substituted theorem.
