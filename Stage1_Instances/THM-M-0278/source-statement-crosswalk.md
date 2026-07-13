# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:1999-2004` records:

- title: `里斯表示定理`;
- attribution: Frigyes Riesz;
- year: 1909;
- gloss: `Hilbert空间上线性泛函的表示`;
- importance: high;
- untrusted formalization label: `已验证`.

The same six fields are duplicated under the functional-analysis heading at lines 2225-2230. All
of them originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Neither occurrence contains a bibliography,
definition, formula, theorem locator, assumptions, proof boundary, correction history, or formal
artifact link.

`Docs/Stage0_Blueprint.md:7684-7709` repeats the gloss and attribution while explicitly leaving the
formal system, logical foundation, exact definitions and premises, proof route, equivalent forms,
axioms, machine status, and artifact links open. Those records establish catalogue provenance only.

## Published source lead

Pinned mathlib's Fréchet-Riesz module cites Manfred Einsiedler and Thomas Ward, *Functional
Analysis, Spectral Theory, and Applications*, Springer, 2017, DOI
`10.1007/978-3-319-58540-6`. The mathlib bibliography and Crossref metadata identify the book, but
the module supplies no theorem or page locator. This intake did not preserve and review an
immutable full text, map a theorem and its definitions to every target component, audit
corrections or errata, reconcile the historical 1909 attribution, or obtain independent review.
It is therefore a modern source lead, not E4/H0 evidence.

## Component crosswalk

| Catalogue/source element | Prospective mathematical meaning | Pinned Lean component | Intake status |
|---|---|---|---|
| Hilbert space | complete real or complex inner-product space | `[RCLike K] [NormedAddCommGroup E] [InnerProductSpace K E] [CompleteSpace E]` | conventional and directly supported, but exact source domain remains open |
| linear functional | bounded/continuous scalar-valued linear map | `StrongDual K E`, definitionally `E ->L[K] K` | continuity is necessary but omitted from the catalogue gloss |
| representation | a vector `y` with the functional equal pointwise to inner product against `y` | `InnerProductSpace.toDual K E` and `toDual_symm_apply` | representing-vector-first orientation is a pinned convention, not source-frozen |
| uniqueness | exactly one representing vector | injectivity/bijectivity of `toDual`; the intake probe checks an explicit `ExistsUnique` wrapper | catalogue does not say whether uniqueness is part of the root |
| norm identity | representative and functional have the same norm | isometric-equivalence structure of `toDual` | possible theorem clause or corollary; source decision open |

## Formal candidate boundary

The direct candidate is `InnerProductSpace.toDual` in
`Mathlib.Analysis.InnerProductSpace.Dual`. Its visible type is a conjugate-linear isometric
equivalence `E equiv StrongDual K E` for a complete inner-product space over an `RCLike` field. The
pointwise inverse law says that the inner product of the inverse image of a functional with `x`
equals the functional applied to `x`.

`IntakeProbe.lean` re-elaborates these declarations and a candidate `ExistsUnique` consequence.
That authenticates the pinned interface and theorem-family match only. Exact source identity,
expression serialization, minimal target imports, checked source transport, terminal proof-body
provenance, transitive dependency and trust audit, and mutation tests remain downstream work.

## Open mapping

The statement phase must admit one exact source proposition and map every domain, binder,
hypothesis, conclusion, inner-product orientation, norm clause, and degenerate case to one
elaborated Lean expression. The source audit must provide edition and pinpoint locators,
definition/premise/proof-node and errata crosswalks, historical-formulation reconciliation, and an
independent review. Until then the human axis is H1 and the pinned formal surface is M3; no H0 or
machine closure is claimed.
