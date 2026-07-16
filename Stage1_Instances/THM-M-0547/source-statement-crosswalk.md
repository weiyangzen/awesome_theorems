# Source-statement crosswalk

## Candidate primary sources

- Solomon Lefschetz, *Algebraic Topology*, American Mathematical Society Colloquium Publications,
  volume 27 (1942). This is the historical primary monograph candidate; an exact theorem/page and
  its conventions have not yet been inspected.
- Glen E. Bredon, *Topology and Geometry*, Graduate Texts in Mathematics 139, Springer (1993),
  the duality chapter. This is a stable modern theorem source candidate, but exact theorem/page,
  edition wording, and errata still require inspection.

These are discovery anchors, not `H0` evidence. The statement phase must choose and inspect a stable
edition rather than infer details from the theorem name.

## Statement selection

The target-bearing repository record fixes only "the duality theorem for manifolds with boundary."
For this statement node, the selected standard compact integral form is: if `M` is a compact,
Hausdorff, oriented `n`-manifold with possibly nonempty boundary, cap product with its fundamental
class induces, for every natural `q`, an isomorphism from compactly supported integral cohomology
`H_c^q(M; Z)` to relative integral homology `H_{n-q}(M, boundary M; Z)`. Compact support agrees
with ordinary cohomology in this compact specialization. The exact historical edition, page,
definition chain, and errata remain open human-source debt and receive no `H0` credit.

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Lefschetz duality" | duality for a manifold with boundary | cap-product isomorphism | included, exact map open |
| "manifold with boundary" | compact Hausdorff `n`-manifold, boundary allowed to be empty | `ModelWithCorners`, `ChartedSpace`, `IsManifold I top M`, `I.boundary M`, dimension equality | concrete manifold and boundary; pair homology interface missing |
| compact-support cohomology | `H_c^q(M; Z)`, equal to ordinary cohomology for compact `M` | typed additive-group family in `LefschetzHomologyData` | interface frozen; native pinned theory missing |
| relative homology | `H_(n-q)(M, boundary M; Z)` | typed additive-group family indexed by `n - q` | interface frozen; native pinned theory missing |
| orientation/fundamental class | selected integral orientation and cap product with `[M, boundary M]` | orientation carrier/value plus an additive cap-product map | map typed; native class and cap product missing |
| duality conclusion | the cap-product homomorphism is an isomorphism for every `q : Nat` | `Function.Bijective (D.capWithFundamentalClass q)` | exact target conclusion |

The realization predicate in `LefschetzHomologyData` identifies the interface objects and map with
the classical integral constructions. It is a premise, not an isomorphism or proof field: the
target still asserts bijectivity. The compact specialization is narrower than the intake's
provisional compact-or-finite-type wording but is a canonical full Lefschetz-duality theorem, not
Poincare duality for closed manifolds or an abstract package containing the answer.

## Boundary policy

- Empty boundary is included and specializes to the closed-manifold case; it is not substituted
  for the boundary theorem.
- Empty and disconnected compact carriers are not excluded by extra premises. The intended
  classical realization must interpret orientation and the fundamental class componentwise.
- Every natural `q` is included. Lean's `n - q` is truncated at zero for `q > n`; the faithful
  realization predicate must supply the conventional vanishing-degree interpretation. A future
  integer-graded native API requires a checked transport.
- Noncompact finite-type manifolds, local coefficients, arbitrary coefficient rings, cohomology
  relative to the boundary, and homological indexing over integers are not credited alternates in
  this node.

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_119.lean` is discovery evidence only. It records
available manifold and absolute singular-homology APIs and a historical relative-homology blocker.
Its `LefschetzDualityPackage` stores the desired isomorphism as structure data, so neither that
structure nor its `StatementShape` receives statement or proof credit here. The consumer-owned
`Statement.lean` instead stores only the missing objects and cap-product homomorphism and states
bijectivity as its conclusion. No declaration or acceptance state is reused from the legacy file.

At pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, repository-local search found no
relative singular-homology, compactly supported cohomology, cap-product, fundamental-class, or
Poincare/Lefschetz-duality declaration. Therefore `Statement.lean` uses only the concrete pinned
manifold boundary API plus explicit typed realization interfaces. This is statement elaboration,
not an anchor-audit completion claim.

Before `H0`, an independent reviewer must verify the chosen edition, theorem/page, definitions,
all assumptions, coefficient conventions, and errata, then approve a row-by-row source-to-Lean
mapping.
