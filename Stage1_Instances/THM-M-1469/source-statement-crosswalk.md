# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10721-10726` supplies exactly the title `自适应有限元`
(adaptive finite elements), attribution to Ivo Babuška and Werner Rheinboldt, the year 1978, the
gloss `基于后验误差估计的自适应` (adaptivity based on a posteriori error estimates), importance
"high," and status `已验证`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, proposition,
definitions, binders, hypotheses, conclusion, proof boundary, corrections, or formal artifact.

`Docs/Stage0_Blueprint.md:39946-39971` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine state, and artifact links open. The rev-5.6 manifest retains `已验证` only as untrusted source
metadata and resets the target to `L0 / rework_required`.

## Primary-source lead

I. Babuška and W. C. Rheinboldt, "Error Estimates for Adaptive Finite Element Computations,"
*SIAM Journal on Numerical Analysis* 15(4), August 1978, pages 736-754, DOI
`10.1137/0715049`, is a credible primary-source lead matching the catalog attribution and date.
Crossref metadata was inspected and confirms the title, author pair, journal, year, volume, issue,
and pages. The observed metadata response had SHA-256
`c8515c57a6154543d140c9e520605e9c9b1dc55fe5fce59d41fe1829512fb2c7`.

The publisher PDF endpoint returned HTTP 403 in this environment, and public metadata identifies
the article as closed access. Consequently no article theorem number, exact page passage, equations,
definitions, assumptions, conclusion, proof, or errata were inspected. Crossref is mutable
bibliographic metadata, not an immutable primary theorem receipt. No independent reviewer has
approved a premise-by-premise or node-by-node mapping. This lead therefore establishes neither a
canonical statement nor `H0`.

## Component crosswalk

| Catalog component | Proposition-changing alternatives | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "adaptive finite elements" | estimator theorem, adaptive-loop convergence, contraction, rate optimality, or complexity | a single source-selected `Prop`, not a method label | root unresolved |
| "a posteriori error estimate" | reliable upper bound, efficient lower bound, two-sided equivalence, localized indicator, or oscillation-aware result | normed-space error, estimator and local-indicator predicates | estimator and constants unresolved |
| finite elements | PDE, variational form, mesh, elements, discrete spaces, and solution | source-selected spaces, forms, meshes and discrete equations | all missing |
| adaptivity | marking, refinement, coarsening, solve accuracy, and stopping | indexed state transition or mesh/solution sequence | algorithm unresolved |
| Babuška/Rheinboldt, 1978 | closely matching paper | immutable primary passage and full assumption/proof crosswalk | bibliography only |
| `已验证` | accepted source and kernel receipts | no Lean proposition or proof object | no H or M credit |

## Neighbor boundary

`THM-M-1461` owns the generic finite-element method, `THM-M-1468` hp finite elements,
`THM-M-1470` a posteriori error estimation, and `THM-M-1471` a priori error estimation. Shared
future definitions or lemmas would not transfer canonical-statement identity, proof credit, or
status among these targets. In particular, a source-selected error-estimate theorem must not be
counted twice as both `THM-M-1469` and `THM-M-1470` without an accountable identity decision.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only
probe checks coercive-form solvability, finite-dimensional orthogonal projection, and convergence of
nested projections. Those APIs can support parts of abstract finite-element analysis but define no
mesh, estimator, marking/refinement loop, or adaptive conclusion. A bounded search for adaptive FEM,
posteriori estimators, residual estimators, reliability, and efficiency found no source-identical
terminal declaration in pinned mathlib or repo-local Lean. The unrelated fixed-point a posteriori
estimate was excluded. This is not an exhaustive formal-candidate audit or a global absence claim.

Before leaving `H5`, accountable reviewers must obtain and lawfully preserve an immutable primary
proposition, record its theorem/page/formula locators and correction status, map every definition,
ordered binder, premise, constant, conclusion, proof node, adaptive-algorithm component, and
boundary case, reconcile the `THM-M-1470` overlap, and independently approve the target decision.
Only then may the statement phase elaborate and mutation-test an exact Lean target.
