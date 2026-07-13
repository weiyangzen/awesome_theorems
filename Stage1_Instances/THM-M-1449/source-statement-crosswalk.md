# Source-statement crosswalk

## Repository source

The catalog record at `Docs/researches/math_theorems.md:10581-10586` contains exactly:

| Catalog field | Literal value | Intake interpretation |
|---|---|---|
| name | `奇异值分解` | recognizable singular-value-decomposition family |
| attribution | `Eugenio Beltrami/Camille Jordan` | historical metadata, not a proof citation |
| time | `1873` | historical metadata without a primary-source locator |
| statement | `矩阵的SVD分解` | "SVD decomposition of a matrix"; not binder-complete |
| importance | `高` | scheduling metadata only |
| formal status | `已验证` | explicitly untrusted; grants no source or machine credit |

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no bibliography, formula, definition,
ordered binders, hypotheses, conclusion, proof boundary, correction record, reviewer, or formal
artifact. `Docs/Stage0_Blueprint.md:39406-39431` repeats the gloss while explicitly leaving the
exact definitions and premises, proof route, dependencies, alternate forms, axioms, machine status,
and artifact links open. It is generated planning metadata, not an independent source.

## Clause crosswalk

| Catalog component | Candidate mathematical component | Prospective Lean surface | Intake state |
|---|---|---|---|
| `矩阵` (matrix) | finite rectangular real or complex matrix | `Matrix (Fin m) (Fin n) K` | scalar, dimensions, and indices open |
| `SVD` | left/right orthogonal or unitary factors and diagonal singular-value factor | matrix existential witnesses | full, thin, or compact shape open |
| singular values | nonnegative square roots of eigenvalues of `A* A`, normally ordered with multiplicity | `LinearMap.singularValues` or explicit data | definition, ordering, and zero padding open |
| decomposition identity | conventionally `A = U * Sigma * V*` | exact matrix equality and star orientation | absent from this catalog record |
| existence/uniqueness | conventionally existence; factors need not be unique | quantified conclusion | not stated |
| `已验证` | screening label | accepted source and kernel receipts would be required | no credit |

No candidate component becomes canonical merely because it is conventional. A later statement
phase must select an approved source and map every incorporated binder, definition, premise,
conclusion, transport, and boundary case.

## Inspected source lead

Sheldon Axler, *Linear Algebra Done Right*, fourth edition, Springer, 2024, Section 7E, was inspected
in the author-hosted PDF observed on 2026-07-13. Definition 7.65 on printed page 271 defines the
singular values of `T` as the nonnegative square roots of the eigenvalues of `T* T`, decreasing and
with eigenspace multiplicity. Theorem 7.70 on printed pages 273-274 proves that a linear map between
finite-dimensional real or complex inner product spaces has an expansion using its positive
singular values and two orthonormal lists. The text immediately after the proof extends both lists
to orthonormal bases and obtains a rectangular diagonal matrix.

The observed PDF SHA-256 is
`45f821b6f51e1f6c42728db6254699d89c14c90fcdb2443c1341188672815d03`. It is an authoritative
modern theorem-family lead, not `H0`: the catalog does not cite it; the observed mutable copy is not
an admitted repository source packet; the book's standing nonzero finite-dimensional convention,
linear-map/list formulation, matrix-factor orientation, empty cases, corrections, historical
attribution, and complete node mapping have not been reconciled or independently reviewed.

## Duplicate collision

The same corpus separately records `THM-M-0044` at
`Docs/researches/math_theorems.md:335-340`. It has the same attribution, year, importance, and
untrusted status, but the sharper gloss `任意矩阵可分解为UΣV*形式` ("every matrix can be decomposed
in `U Sigma V*` form"). Existing work under that target also marks `THM-M-1449` as an unresolved
duplicate. This is strong identity-review evidence, not authorization to merge roots or transfer
scope, source credit, Lean declarations, receipts, debt state, or proof completion. The integration
lane must decide duplicate identity and ownership independently.

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.InnerProductSpace.SingularValues` defines `LinearMap.singularValues` and proves
nonnegativity, ordering/eigenvalue relations, and support facts. The inner-product and matrix
spectrum modules supply spectral bases and Hermitian diagonalization; `UnitaryGroup` supplies the
square unitary-factor predicate. `IntakeProbe.lean` authenticates representative interfaces.

The same bounded search located a stronger repo-local candidate in the separate owned path
`Stage1_Instances/THM-M-0044`. Its `Proof.lean` declares
`Stage1Instances.THM_M_0044.Proof.singularValueDecomposition` for that dossier's exact full
rectangular Real-and-Complex target; `Validation.lean` contains a separately written root.
`proof-validation.md` records successful pinned elaboration and only `propext`, `Classical.choice`,
and `Quot.sound`, while `release.md` records that the receipts remain provisional, the accepted
vector remains `H1/M3/R3`, and duplicate, dependency, provenance, trust, source, and release gates
remain open. Directly running `Proof.lean` without its isolated prerequisite-olean recipe fails at
the expected missing `ObligationTree` module; this intake therefore records the checked recipe and
receipt rather than misreporting that direct failure as a proof failure.

This is a substantive `M3` formal candidate for `THM-M-1449`, not `M0`: the present catalog gloss
has no frozen statement, duplicate identity and root ownership are unresolved, no checked transport
from the sibling target exists, and no sibling receipt is accepted or transferable. The mathlib
declarations remain prerequisites rather than the terminal factorization. These observations are
intake discovery only, not the downstream immutable anchor audit.

## Source gate

Before leaving `H1`, accountable reviewers must select and preserve an immutable source edition,
decide whether this target is identical to `THM-M-0044`, map every definition, binder, hypothesis,
conclusion, factor convention and boundary case, audit corrections and attribution, and approve
the crosswalk independently. Only then may the statement phase freeze an exact Lean expression,
minimal imports, checked transports, expression/environment hashes, and required mutations.
