# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:398-403` supplies exactly the title `盖尔圆盘定理`, attribution
Semyon Gershgorin, year 1931, gloss `矩阵特征值的定位定理`, importance `中`, and status
`已验证`. Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, theorem
locator, formula, definitions, binders, hypotheses, exact conclusion, proof boundary, correction
history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:1564-1589` repeats the sparse record while explicitly leaving the target
formal system, foundation, precise definitions and premises, proof route, dependencies, alternate
forms, axiom policy, machine status, and artifact links open. The rev-5.6 manifest preserves
`已验证` only as untrusted metadata and resets the target to `L0 / rework_required`.

## Inspected human source lead

Revision 56196 of the *Encyclopedia of Mathematics* entry “Gershgorin theorem,” attributed there
to Richard S. Varga as the original contributor, was inspected on 2026-07-13 at
`https://encyclopediaofmath.org/index.php?title=Gershgorin_theorem&oldid=56196`. It states for a
complex `n x n` matrix, with `n >= 2`, that every eigenvalue lies in some closed row disc centered
at `a_ii` with radius `sum_{j != i} |a_ij|`, and supplies the standard maximal-eigenvector-coordinate
proof. It also records a stronger disjoint-disc-component counting result.

The entry identifies the primary bibliographic lead as S. Gerschgorin, “Ueber die Abgrenzung der
Eigenwerte einer Matrix,” *Izv. Akad. Nauk. SSSR Ser. Mat.* 1 (1931), pages 749-754. This
secondary source is a strong statement/proof and bibliography lead, but the original paper was not
admitted or mapped at theorem resolution. No original-language passage, translation audit,
correction/errata disposition, immutable repository copy, or independent reviewer is recorded.
Consequently this intake proposes `H1`, not `H0`.

The zbMATH Open JFM record 2560682 (identifier `57.1340.06`), available from
`https://api.zbmath.org/v1/document/2560682` and `https://zbmath.org/2560682`, independently
identifies the same 1931 paper as VII Series, issue 6, pages 749-754. This differs from the EoM
volume-number rendering and must be reconciled during primary-source admission. Its German review
states both that all characteristic roots lie
in the closed union of the row circles and that a connected component made from `m` circles contains
exactly `m` characteristic roots. The API record is dynamically serialized and no immutable hash
is credited. It corroborates the theorem family but still does not replace inspection and
independent admission of the primary paper.

## Clause crosswalk

| Catalog component | Inspected secondary formulation | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| matrix | complex finite square `n x n` matrix, `n >= 2` | `A : Matrix n n K` with finite index and normed field | complex/generalized field and dimension not selected |
| eigenvalue | characteristic root with nonzero eigenvector | `Module.End.HasEigenvalue (Matrix.toLin' A) mu` | checked characteristic-root/eigenvector transport still open |
| localization | membership in the union of row discs | `Exists fun k => mu ∈ Metric.closedBall ...` | direct candidate located; canonical identity not accepted |
| center | diagonal entry `a_ii` | `A k k` | aligned in the candidate |
| radius | `sum_{j != i} |a_ij|` | `sum j in Finset.univ.erase k, norm (A k j)` | aligned modulo finite-index and absolute-value/norm encodings |
| closed disc | `|lambda - a_ii| <= r_i` | `Metric.closedBall (A k k) r` | checked membership/inequality transport deferred |
| stronger refinement | a separated union of `k` discs contains exactly `k` eigenvalues with multiplicity | no candidate in the inspected mathlib module | root inclusion versus refinement unresolved |
| verified | untrusted catalog label | no declaration or receipt | explicitly rejected as evidence |

## Pinned Lean candidate

Pinned mathlib module `Mathlib.LinearAlgebra.Matrix.Gershgorin` explicitly names
`eigenvalue_mem_ball` as Gershgorin's circle theorem. Its interface is:

```text
{K n : Type*} [NormedField K] [Fintype n] [DecidableEq n]
{A : Matrix n n K} {mu : K}
(hmu : Module.End.HasEigenvalue (Matrix.toLin' A) mu) ->
  exists k, mu in closedBall (A k k) (sum j in univ.erase k, norm (A k j))
```

The module is pinned at mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` and the
current file has SHA-256 `d55fd47dd6fc18289d04c9ac628c74b6f3813bbc569efcfd276e308fe170cb79`.
Git history locates the original theorem addition at commit
`a075669f9771fca06315e01c59a1c20a41a8408d`. Pinned `docs/1000.yaml` maps Wikidata
`Q978688`, title “Gershgorin circle theorem,” to the declaration. The module itself cites only a
Wikipedia page, so its docstring is not primary human-source evidence.

The pinned source can be inspected at
`https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/LinearAlgebra/Matrix/Gershgorin.lean#L27-L31`,
and the origin commit at
`https://github.com/leanprover-community/mathlib4/commit/a075669f9771fca06315e01c59a1c20a41a8408d`.
`IntakeProbe.lean` verifies the candidate and related API interfaces and reports direct axioms
`[propext, Classical.choice, Quot.sound]`. It does not freeze the canonical target or audit the
terminal body, full transitive dependencies, TCB, source equivalence, placeholders, or wrapper.
The candidate therefore supports provisional `M3`, not `M0-W`.

## Required statement/source admission

Before statement execution, an independent reviewer must preserve and hash a lawful primary or
authoritative source, select the basic inclusion or stronger refinement, transcribe all definitions,
binders, hypotheses, conclusions, and degenerate cases, audit corrections and translation, and
approve the mapping to the exact Lean expression. Complex-to-`NormedField`, row-to-column,
characteristic-root-to-`HasEigenvalue`, finite-index, closed-ball, and boundary transports must be
machine-checked wherever credited. Until then the canonical mathematical and Lean targets remain
null.
