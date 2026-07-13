# Source-statement crosswalk

## Repository record

The repository catalog at `Docs/researches/math_theorems.md:1915` records the Stone-Weierstrass
theorem, attributes it to Marshall Stone in 1937, and gives only the gloss "density of algebras of
continuous functions." The Stage0 projection at `Docs/Stage0_Blueprint.md:7360` repeats that gloss
and explicitly leaves precise definitions, premises, equivalent formulations, axiom use, formal
status, and artifacts open. The catalog row was introduced by repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

The source status `verified` is untrusted manifest metadata. It is neither a primary-source
citation nor a claim that this repository has checked a source-identical proposition.

## Bibliographic leads, not H0 evidence

Crossref metadata was inspected for Marshall H. Stone, "Applications of the theory of Boolean
rings to general topology," *Transactions of the American Mathematical Society* 41(3) (1937),
375-481, DOI `10.1090/S0002-9947-1937-1501905-7`. Its year matches the catalog, but the catalog
does not cite this paper, and no exact theorem passage or definition chain from it has been
admitted and reviewed.

Crossref also identifies Stone's later two-part article "The Generalized Weierstrass Approximation
Theorem," *Mathematics Magazine* 21(4-5) (1948), deposited at pages 167 and 237, DOI
`10.2307/3029750` and DOI `10.2307/3029337`. This is a relevant historical lead, but its date
conflicts with the catalog's sole year and it likewise has no admitted exact passage, assumption
map, proof boundary, corrections or errata audit, translation, or independent review here.

Consequently the human-source state is `H1`, not `H0`. A future source audit must preserve an
immutable lawful edition, locate the exact theorem and incorporated definitions by page or stable
archival locator, map every premise and conclusion, distinguish the 1937 and 1948 roles, check
corrections and errata, and obtain an identified independent review.

## Clause crosswalk

| Catalog clause | What it establishes | What remains open | Pinned Lean lead, not credited |
|---|---|---|---|
| Stone-Weierstrass theorem | recognizable theorem family | exact source, version, and root proposition | module `Mathlib.Topology.ContinuousMap.StoneWeierstrass` |
| Marshall Stone; 1937 | attribution and date lead | whether the 1937 topology paper owns the intended result; relation to the 1948 article | no Lean statement identity follows from metadata |
| continuous functions | intended object family | domain, codomain, bundled encoding, topology, compactness, universes | `C(X, Real)` and `C(X, k)` candidates |
| algebra | algebraic approximation family | unital constants, real versus RCLike scalars, star/conjugation closure | `Subalgebra Real C(X, Real)` versus `StarSubalgebra k C(X, k)` |
| density | approximation conclusion | closure equality, elementwise closure, norm epsilon, pointwise epsilon, global versus compact-set form | six candidate declarations checked by `IntakeProbe.lean` |
| implicit hypotheses | none stated | separation of points, compactness/Hausdorff conventions, positivity of epsilon, boundary cases | mathlib `SeparatesPoints`, `CompactSpace`, and epsilon premises |
| verified | untrusted source label only | source fidelity, exact expression, proof provenance, trust, reproducibility, review | no H0, M0, or accepted receipt |

## Formal-candidate boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` documents the real
closure-equality declaration as the Stone-Weierstrass theorem in `docs/1000.yaml` and supplies both
real and RCLike variants. The probe validates only availability and representative axiom output.
It does not select one candidate, prove equivalence to an admitted source statement, audit the
terminal proof-body and transitive declaration closure, or satisfy the later anchor-audit phase.

The first downstream retry condition is a reviewed source decision that freezes scalar and domain
scope, every ordered binder and assumption, the exact density conclusion, alternate forms, and
degenerate cases. Only then may the statement phase elaborate and fingerprint a canonical Lean
target and mutation-test it.
