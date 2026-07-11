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

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Lefschetz duality" | duality for a manifold with boundary | cap-product isomorphism | included, exact map open |
| "manifold with boundary" | pair `(M, ∂M)` and dimension `n` | concrete manifold boundary and pair inclusion | included, API open |
| compact-support cohomology | handles noncompact `M` | compactly supported cochain/cohomology object | included, coefficients open |
| relative homology | homology of `(M, ∂M)` | concrete relative singular homology | included, API open |
| orientation class | class inducing degree reversal | fundamental/orientation class and cap product | included, formal encoding open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_119.lean` is useful discovery evidence: it records
available manifold and singular-homology APIs and a historical mathlib relative-homology blocker.
Its terminal `LefschetzDualityPackage` assumes the desired isomorphism as structure data, so neither
that structure nor `StatementShape` closes the source theorem. Its dated upstream audit must be
repeated at the pinned revision during anchor audit.

Before `H0`, an independent reviewer must verify the chosen edition, theorem/page, definitions,
all assumptions, coefficient conventions, and errata, then approve a row-by-row source-to-Lean
mapping.
