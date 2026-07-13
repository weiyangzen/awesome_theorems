# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10665` supplies exactly the title `有限元方法` (finite element
method), attribution to Richard Courant, the year 1943, the gloss `偏微分方程的变分离散`
(`variational discretization of partial differential equations`), importance "high," and status
`已验证`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, mathematical
formula, binders, hypotheses, conclusion, proof boundary, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:39730` repeats the gloss while leaving the formal system, foundation,
exact definitions and premises, proof route, dependencies, alternate forms, axioms, machine status,
and artifact links open. The rev-5.6 manifest retains `已验证` only as untrusted source metadata and
resets the target to `L0 / rework_required`.

## Primary-source lead

Richard Courant, "Variational Methods for the Solution of Problems of Equilibrium and Vibrations,"
*Bulletin of the American Mathematical Society* 49(1), 1943, pages 1-23, DOI
`10.1090/S0002-9904-1943-07818-4`, is a credible historical lead. Crossref bibliographic metadata
was inspected and confirms the author, title, journal, year, volume, issue, and pages. The article
body was not available through the inspected unauthenticated endpoints, so no exact source passage,
assumption set, proof, erratum, or relationship to the catalog gloss was accepted. Crossref is
mutable bibliographic metadata, not an `H0` source receipt.

The lead itself does not resolve whether the repository intends Courant's variational construction,
a later abstract Galerkin theorem, Cea's lemma, a conforming-element convergence theorem, or a
specific PDE error estimate. Modern finite-element theory contains each as a distinct proposition.
The catalog selects none, so the canonical statement remains open.

## Component crosswalk

| Catalog component | Mathematical alternatives | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "finite element method" | construction, discrete solvability, orthogonality, quasi-optimality, convergence, or error rate | one source-selected proposition, not an algorithm label | root result unresolved |
| "variational" | minimization, symmetric coercive weak form, general Galerkin form, or inf-sup formulation | spaces, form, functional, norms, and solution predicate | formulation unresolved |
| "PDE" | elliptic, parabolic, hyperbolic, eigenvalue, equilibrium, or vibration problem | domain, operator, data, boundary conditions, solution concept | problem unresolved |
| "discretization" | conforming/nonconforming elements, mesh family, basis assembly, or approximation space | indexed finite-dimensional subspaces and approximation maps | discretization unresolved |
| Courant / 1943 | historical bibliographic lead | immutable primary passage and complete assumption crosswalk | bibliography only |
| `已验证` | untrusted inventory label | no Lean proposition or proof object | no H or M credit |

## Neighbor boundary

`THM-M-1462` separately owns the Galerkin method, `THM-M-1463` Petrov-Galerkin, `THM-M-1464`
discontinuous Galerkin, `THM-M-1465` finite differences, `THM-M-1466` finite volumes, and
`THM-M-1467` spectral elements. Those records may later share definitions or lemmas, but none
transfers statement identity, proof credit, or status to this target.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only
probe checks Lax-Milgram equivalence/uniqueness and orthogonal-projection characterization,
minimality, and norm control. A bounded case-insensitive search for finite-element, Galerkin, Cea,
and variational-discretization terms found no exact-topic declaration in pinned mathlib or the
repo-local Lean tree. These APIs are possible analytic ingredients only. They neither define a
mesh or finite-element space nor identify or close the missing root, and this bounded search is not
the later external anchor audit.

Before leaving `H5`, accountable reviewers must admit one immutable primary-source proposition,
map every definition, ordered binder, premise, conclusion, proof node, and correction, reconcile
the broad PDE-discretization gloss and neighbor boundaries, and independently approve the target
decision. Only then may the statement phase freeze minimal imports, an elaborated expression,
checked transports, and the required statement mutations.
