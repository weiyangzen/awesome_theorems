# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10006-10011` supplies exactly the title `Hamiltonian systems`,
William Hamilton, 1834, the gloss `a mathematical framework for classical mechanics`, importance
`high`, and status `verified`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:37344-37369` repeats that metadata but explicitly leaves the exact
definitions and premises, proof route, dependencies, equivalent forms, axiom policy, machine-
checked status, and artifact links open. The rev-5.6 target manifest retains `verified` only in an
explicitly untrusted field and resets the target to `L0 / rework_required`.

The catalog contains no formula, bibliography, theorem or page locator, ordered binder,
hypothesis, truth-valued conclusion, incorporated definition, proof boundary, correction history,
or reviewer. Its gloss names a formalism, not one stable proposition.

## Historical source lead

Crossref metadata for DOI `10.1098/rstl.1834.0017` identifies William Rowan Hamilton, *On a general
method in dynamics; by which the study of the motions of all free systems of attracting or
repelling points is reduced to the search and differentiation of one central relation, or
characteristic function*, *Philosophical Transactions of the Royal Society of London*, issue 124
(1834), pages 247-308. This is a plausible primary historical family for the attribution and year.

The Royal Society metadata advertises a PDF, but direct retrieval in this intake returned HTTP 403.
No complete edition was preserved or inspected; no precise passage, incorporated definition,
assumption, conclusion, proof boundary, or erratum was mapped. The repository does not cite this
paper, and the bibliographic match cannot decide which of its method, characteristic-function,
canonical-equation, or variational components the catalog intended. This lead is therefore
discovery-only `E5`, not accepted `H0` evidence.

## Component crosswalk

| Catalog component | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Hamiltonian system | canonical Hamilton equations or a symplectic vector field and its integral curves | phase space, symplectic form or `Matrix.J`, Hamiltonian, derivative, vector field, solution predicate | system model and sign convention absent |
| mathematical framework | a definition, equivalence with Lagrangian mechanics, conservation package, or flow theorem | one exact truth-valued root plus checked relationships to alternates | no proposition selected |
| classical mechanics | finite particle mechanics, constrained systems, continuum models, or geometric mechanics | domain, scalar, dimension, configuration/cotangent structure, regularity | carrier and regime absent |
| William Hamilton / 1834 | historical attribution and likely source family | immutable edition and premise-to-binder mapping | plausible locator only |
| `verified` | untrusted inventory label | no Lean declaration or proof body | explicitly rejected as evidence |

## Candidate roots and non-equivalence

Hamilton's coordinate equations, equivalence with Euler-Lagrange equations, autonomous energy
conservation, preservation of the symplectic form, and preservation of phase volume require
different hypotheses and yield different conclusions. The catalog does not choose one or license
their conjunction. Likewise, a statement that a given curve satisfies an equation is not an
existence/uniqueness theorem, and a global-flow result is stronger than a local integral-curve
statement unless completeness is supplied.

The near-duplicate `THM-M-1516` dossier identifies Arnold's *Mathematical Methods of Classical
Mechanics* as a modern discovery lead and records these same distinctions. That dossier and
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_185.lean` belong to another target and are not
accepted source identity for `THM-M-1373`. The legacy file's desired conclusions are unconstrained
`Prop` fields, so it is an abstract interface rather than proof closure. It also records an
unpinned Physlib candidate for Hamilton's equations at a different observed toolchain; intake does
not fetch or integrate it.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean` checks
generic ODE/integral-curve and global-flow interfaces plus `Matrix.J`, its skew-transpose and square
identities, and the linear symplectic group. A bounded exact-topic search located only topic-
adjacent legacy Hamiltonian artifacts and no repo-local or pinned-mathlib declaration for this
unidentified root. This is intake discovery only, not the downstream exhaustive anchor audit or a
claim of global absence.

## Required source admission

The statement phase must preserve and hash a lawful complete source edition, select one exact
result, transcribe every incorporated definition, ordered binder, hypothesis, conclusion, proof
boundary, convention, and boundary case, check corrections and errata, reconcile the near-duplicate
target boundary, and obtain independent source review. It must then elaborate and mutation-test the
same exact Lean expression. Until then the canonical mathematical and Lean targets remain null and
the received target is classified `H5` as not yet a stable proposition. This classification does
not refute Hamiltonian mechanics or any correctly stated theorem in the source family.
