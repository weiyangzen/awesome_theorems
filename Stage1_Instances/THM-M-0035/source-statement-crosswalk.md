# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records only:

- title: `雅各布森密度定理`;
- attribution: Nathan Jacobson;
- year: 1945;
- gloss: `本原环的稠密性定理`;
- importance: high;
- untrusted formalization label: `已验证`.

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md` repeats them while
explicitly leaving exact definitions, premises, proof route, equivalent formulations, axioms,
machine status, and artifact links open. These records establish catalogue identity only.

## Historical source lead

Crossref metadata for DOI `10.1090/S0002-9947-1945-0011680-8` identifies N. Jacobson,
"Structure theory of simple rings without finiteness assumptions," *Transactions of the American
Mathematical Society* 57(2) (1945), pages 228-245. The metadata payload also records
`10.2307/1990204` in its `aliases` field.
The retrieved metadata payload had SHA-256
`5d7f2b7b84d949e0efdbec307c418748972b04ddc0f6eefada7cbc0e4111d4ae`.

This is a bibliographic lead, not an H0 source. The full article was not retrieved from the AMS
endpoint during intake, so no theorem/page passage, incorporated definition, exact assumption,
proof boundary, or erratum was inspected. The catalogue-to-article identity and historical naming
also require independent review.

## Clause crosswalk

| Repository phrase or candidate component | Required mathematical meaning | Pinned Lean component | Intake status |
|---|---|---|---|
| "primitive ring" | a ring admitting a faithful simple module, with handedness and unit convention fixed | `IsSimpleModule R M` and `FaithfulSMul R M` are available; no primitive-ring predicate was found in the bounded search | family boundary only |
| endomorphism division ring | `D = End_R(M)` with composition/opposite convention | `Module.End R M`; Schur division-ring instance exists for a simple module with decidable equality | API located; bridge unaudited |
| finite independent inputs | a finite `D`-linearly independent family `x_i` | `LinearIndependent (Module.End R M) x` | prospective encoding only |
| arbitrary outputs | a same-index family `y_i : M` | function or finite-family encoding | absent from repository source |
| simultaneous interpolation | some `r : R` sends every `x_i` to `y_i` | `jacobson_density f s` gives agreement with a `D`-linear endomorphism on a finite set | strong candidate; exact transport open |
| density | density of the action image in a finite/pointwise topology | no topology is named in `jacobson_density`; its finite-set property is an algebraic density interface | topological equivalence unproved |
| finite-dimensional special case | scalar action map is onto all `D`-linear endomorphisms | `Module.Finite.toModuleEnd_moduleEnd_surjective` | stronger hypothesis; not root substitute |
| `已验证` | untrusted inventory status | no expression, source receipt, or accepted proof | explicitly rejected as credit |

## Pinned formal provenance lead

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the declarations live at
`Mathlib/RingTheory/SimpleModule/Basic.lean:570` and `:582`. They entered mathlib in commit
`2396a85794e2337ad47bdb725b3af885bbfd1638` (2026-01-13, PR #33906). The source comment says
the statement and proof follow `[Lorenz2008]`, Chapter 28, F20. The pinned bibliography identifies
Falko Lorenz, *Algebra, Volume II*, first edition, Springer, 2008, DOI
`10.1007/978-0-387-72488-1`. Mathlib's `docs/1000.yaml` maps the Wikidata Jacobson-density item to
`jacobson_density`.

These are unusually strong formal and source leads, but intake is not the exhaustive anchor audit.
The later source and anchor phases must inspect the cited book passage, compare it to the 1945
article and catalogue gloss, serialize the exact Lean type, audit terminal bodies and dependency
closure, and prove every claimed transport before any H0 or M0 status is considered.

## First failed source gate

There is no accepted immutable primary theorem passage with a complete definition, assumption,
conclusion, proof-boundary, translation, and errata crosswalk. Until one is independently reviewed,
choosing the faithful-simple formulation, the semisimple mathlib formulation, or the finite
surjectivity corollary as the canonical root would substitute missing mathematics.
