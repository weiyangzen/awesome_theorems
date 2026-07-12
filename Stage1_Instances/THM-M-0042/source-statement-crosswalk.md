# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:321-326` supplies exactly the title `若尔当标准形定理`, attribution
to Camille Jordan, the year 1870, the gloss `复矩阵可相似于若尔当标准形` ("a complex matrix is
similar to Jordan normal form"), importance "high," and status `已验证`. Git history attributes all
six uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no
bibliography, theorem locator, formula, definitions, ordered binders, hypotheses, proof boundary,
correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:1267-1292` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 target manifest preserves `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

## Inspected modern source lead

Sheldon Axler, *Linear Algebra Done Right*, fourth edition, author-hosted PDF observed on
2026-07-13, was inspected. In Section 8C:

- Definition 8.44, printed page 322, defines a Jordan basis for an operator by requiring a block
  diagonal matrix whose blocks have an eigenvalue on the diagonal, ones immediately above the
  diagonal, and zeros elsewhere.
- Theorem 8.45, printed pages 322-324, proves that every nilpotent operator has a Jordan basis.
- Theorem 8.46, printed page 324, states that every operator on a complex vector space has a Jordan
  basis, under the chapter's standing convention that the vector space is finite-dimensional and
  nonzero, and proves it from generalized-eigenspace decomposition plus the nilpotent result.

The observed PDF SHA-256 is
`45f821b6f51e1f6c42728db6254699d89c14c90fcdb2443c1341188672815d03`. The copy is an
author-hosted, mutable source lead and was not added to the repository. The catalog does not cite
it; its operator-and-basis statement is not literally the catalog's matrix-similarity sentence; a
pinpoint definition/assumption/conclusion transport, correction audit, lawful preservation policy,
and independent review remain open. Thus this source supports provisional `H1`, not `H0`.

Camille Jordan's 1870 historical attribution is retained from the catalog and echoed by Axler, but
no primary 1870 edition, exact passage, translation, or correction history was inspected or
credited. Historical attribution must not be mistaken for a source-statement crosswalk.

## Clause crosswalk

| Catalog component | Source component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "complex matrix" | matrix of an operator on a finite-dimensional complex vector space | `Matrix n n Complex`, `Module.End Complex V`, `LinearMap.toMatrix` | dimension, index, and operator/matrix transport open |
| "similar" | change from an arbitrary basis to a Jordan basis | matrix units or a linear equivalence, conjugation equation | witness type and orientation open |
| "Jordan normal form" | Definition 8.44 block diagonal matrix of Jordan blocks | future block predicate using `Matrix.fromBlocks`, direct sums, or an equivalent encoding | no pinned definition located; block assembly and order open |
| existence theorem | Theorem 8.46 for every finite-dimensional nonzero complex operator | existential basis or existential invertible matrix and block data | exact conclusion, zero-dimensional extension, and checked equivalence open |
| nilpotent core | Theorem 8.45 plus generalized-eigenspace decomposition | nilpotence and `Module.End.iSup_maxGenEigenspace_eq_top` | adjacent ingredient only; no root credit |
| `已验证` | untrusted inventory label | source review and kernel receipt would be required | no H or M credit |

## Pinned Lean boundary

Pinned mathlib contains `Module.End.iSup_maxGenEigenspace_eq_top`, which proves that generalized
eigenspaces span a finite-dimensional space over an algebraically closed field. It also contains
`Module.End.exists_isNilpotent_isSemisimple`, the Jordan-Chevalley-Dunford decomposition, and matrix
units and representation APIs. These results corroborate nearby infrastructure but do not state the
existence of Jordan chains, a Jordan basis, a Jordan block decomposition, or similarity to Jordan
normal form. The discovery probe checks those exact declarations without declaring a target.

A bounded search of repo-local Lean and pinned mathlib found no exact Jordan-block,
Jordan-basis, or Jordan-normal-form declaration. The similarly named Jordan-Chevalley module is an
explicit non-substitute. These observations are intake discovery only, not the later immutable
external anchor audit and not a global absence theorem.

## Source gate

Before leaving `H1`, accountable reviewers must preserve an immutable approved source edition,
select one exact proposition and incorporated definitions, map every binder, hypothesis,
conclusion, matrix/operator transport, and boundary case, audit errata and historical attribution,
and independently approve fidelity to `THM-M-0042`. Only then may the statement phase freeze the
minimal imports, elaborated expression and environment hashes, checked alternate encodings, and
required removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations.
