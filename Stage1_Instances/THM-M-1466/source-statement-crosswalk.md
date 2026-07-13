# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10700-10705` supplies exactly the title `有限体积法` (finite
volume method), attribution to many mathematicians, the 20th century, the gloss `守恒律的离散方法`
(`discrete method for conservation laws`), importance "high," and status `已验证`. Git history
places all six uncited fields in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record
contains no bibliography, formula, binders, hypotheses, conclusion, proof boundary, correction
history, or formal artifact.

`Docs/Stage0_Blueprint.md:39865-39890` repeats the gloss while leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate formulations,
axioms, machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
untrusted source metadata and resets the target to `L0 / rework_required`.

## Source lead

Robert Eymard, Thierry Gallouet, and Raphaele Herbin, "Finite volume methods," *Handbook of
Numerical Analysis*, 2000, pages 713-1018, DOI `10.1016/S1570-8659(00)07005-8`, is a credible
modern survey lead. Crossref bibliographic metadata was inspected and confirms the authors, title,
book series, year, pages, publisher, and DOI. Only mutable bibliographic metadata was observed: no
immutable chapter body, pinpoint theorem, complete assumptions, proof, correction audit, catalog
root selection, or independent review was admitted. It therefore supplies no `H0` evidence.

The lead covers a theory and collection of schemes, not one automatically canonical result. It
does not resolve whether the repository intends discrete conservation, monotonicity, stability,
convergence, an error estimate, entropy consistency, or implementation correctness. The catalog
selects none, so the canonical statement remains open.

## Component crosswalk

| Catalog component | Mathematical alternatives | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "finite volume method" | balance update, local/global conservation, stability, convergence, error, or implementation theorem | one source-selected proposition, not an algorithm label | root result unresolved |
| "conservation law" | scalar/system; steady/evolutionary; homogeneous/forced; weak/entropy solution | flux, PDE, domain, data, solution predicate, admissibility | continuous problem unresolved |
| "discrete" | cell-centered/vertex-centered; semidiscrete/fully discrete; explicit/implicit | mesh incidence, cell states, time indices, update relation | discretization unresolved |
| "volume" | general control volumes, polyhedral mesh, Cartesian grid, Voronoi cells | finite cells/faces, measures, orientations, neighbors | geometry unresolved |
| numerical flux | consistent/conservative/monotone/entropy-stable flux and boundary closure | face flux and hypotheses | flux convention absent |
| `已验证` | untrusted inventory label | no Lean proposition or proof object | no H or M credit |

## Neighbor boundary

`THM-M-1461` through `THM-M-1465` separately own finite-element, Galerkin, Petrov-Galerkin,
discontinuous-Galerkin, and finite-difference families; `THM-M-1467` owns spectral elements.
`THM-M-1199` through `THM-M-1205` separately own shock theory, the Rankine-Hugoniot condition,
generic, Lax, and Oleinik entropy conditions, the Kruzkov theorem, and compensated compactness.
These continuous-PDE-side jump, admissibility, uniqueness, and compactness records may later provide
definitions or bridge lemmas, but none transfers finite-volume statement identity, proof credit,
or status to this target.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only
probe checks finite-set sums, reindexing, disjoint-union decomposition, additive distribution, and
subtraction distribution. These are possible algebraic ingredients for a future exact proof that
oriented internal face fluxes cancel. A bounded case-insensitive search for finite-volume,
numerical-flux, cell-average, and conservation-law-discretization terms found no exact-topic
declaration in pinned mathlib or repo-local Lean. Repo-local conservation-law matches in legacy
`S1_M_170` and `S1_M_207` concern continuous compensated-compactness or KdV packages, not a
finite-volume scheme; other "finite volume" and "conservative" matches were unrelated. This is
not a global absence claim or the later external anchor audit.

Before leaving `H5`, accountable reviewers must admit one immutable primary-source proposition,
map every definition, ordered binder, premise, conclusion, proof node, and correction, reconcile
the broad method gloss and neighbor boundaries, and independently approve the target decision.
Only then may the statement phase freeze minimal imports, an elaborated expression, checked
transports, and the required statement mutations.
