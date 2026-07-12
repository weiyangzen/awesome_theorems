# Source-statement crosswalk

## Repository sources inspected

`Docs/researches/math_theorems.md:4748-4753` is the complete repository research record. It gives
the Chinese theorem name, Solomon Lefschetz, 1926, the gloss `莱夫谢茨数与不动点`, importance
"high", and `已验证`. Git history traces all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. This establishes repository provenance, not a
mathematical source or proposition.

`Docs/Stage0_Blueprint.md:17530-17555` repeats that metadata while explicitly leaving precise
definitions and premises, proof history and route, dependencies, equivalent forms, axioms,
machine-checked status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the item to `L0 / rework_required`.

No repository-local target artifact, exact source quotation, bibliography, theorem locator,
definition chain, assumption list, errata disposition, translation review, or independent source
review was found.

## Primary-source discovery leads

- Crossref bibliographic metadata identifies Solomon Lefschetz, "Intersections and transformations
  of complexes and manifolds", *Transactions of the American Mathematical Society* **28** (1926),
  no. 1, 1-49, DOI `10.1090/S0002-9947-1926-1501331-3` (alias `10.2307/1989171`). The author and
  year match the catalog. The paper itself, an exact theorem/page, incorporated definitions, and
  assumptions were not admitted in this intake.
- A later primary-source lead is Solomon Lefschetz, "On the fixed point formula", *Annals of
  Mathematics* (2) **38** (1937), 819-822. Its relationship to the catalog's 1926 date and intended
  implication-versus-formula scope remains to be audited.

These citations are discovery anchors only. Network bibliographic metadata does not establish H0,
and no immutable primary text, page-level crosswalk, errata search, or independent review is
credited.

## Crosswalk

| Repository phrase | Possible mathematical component | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `莱夫谢茨不动点定理` | one classical global fixed-point theorem in the Lefschetz family | future source-selected declaration | recognizable family, not a proposition |
| "Lefschetz number" | finite alternating sum of traces of induced (co)homology endomorphisms | singular/simplicial (co)homology functor, induced map, finite-dimensional trace, finite sum | theory, coefficients, finiteness, signs, and reduction absent |
| "and fixed points" | usually nonzero number implies existence of a fixed point; possibly a stronger index formula | `Exists (Function.IsFixedPt f)` or a source-selected index equality | implication direction and conclusion strength absent |
| Solomon Lefschetz, 1926 | historical attribution and likely foundational paper family | source provenance only | bibliographic match found; pinpoint identity open |
| `已验证` | catalog classification | no Lean proposition or proof object | explicitly rejected as evidence |

## Pinned Lean boundary

The discovery-only probe elaborates:

- `AlgebraicTopology.singularChainComplexFunctor` and
  `AlgebraicTopology.singularHomologyFunctor` from
  `Mathlib.AlgebraicTopology.SingularHomology.Basic`;
- `LinearMap.trace` from `Mathlib.LinearAlgebra.Trace`; and
- `Function.IsFixedPt` and `Function.fixedPoints` from
  `Mathlib.Dynamics.FixedPoints.Basic`.

These APIs show that pieces of a future encoding exist. They do not supply a compact-polyhedron or
finite-complex target, a finite alternating trace, a source-selected Lefschetz number, or the
terminal theorem. A bounded case-insensitive search for `Lefschetz`, fixed-point theorem terms, and
trace/homology combinations found only unrelated Lefschetz-principle and neighboring legacy-topic
hits, not a target declaration. This is an intake feasibility boundary, not an exhaustive anchor
audit or an absence claim beyond the pinned trees searched.

Before H0 or the statement gate can pass, accountable reviewers must pin an immutable primary
edition; select the exact theorem and incorporated definitions by page; map every space, map,
coefficient, finiteness, trace, sign, nonzero, and fixed-point clause; inspect corrections and
errata; resolve the 1926-versus-1937 and implication-versus-formula boundaries; approve the
translation; and independently review the result.
