# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:11707-11712` supplies exactly the title `线性码`, the
attribution `众多数学家`, the period `20世纪`, the gloss `线性纠错码`, importance `高`, and
status `已验证`. Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no formula, definition chain,
binders, hypotheses, conclusion, citation, proof boundary, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:43201-43226` repeats the gloss while explicitly leaving the target formal
system, foundation, exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

The repository has no second exact `线性码` record. It does contain the narrower Stage0-only item
`THM-C-0377`, `线性码对偶`, whose gloss is merely `线性码与对偶码的关系`; its exact proposition is also
open. That record cannot choose a duality theorem for this target or transfer any status.

## Inspected source lead

Venkatesan Guruswami, *Introduction to Coding Theory*, CMU Spring 2010, Notes 1:
*Introduction, linear codes* (January 2010), was inspected from the author's course site. It is a
modern pedagogical source lead, not the catalog's cited authority because the catalog cites none.

The notes make the source ambiguity concrete:

- Definition 7, printed page 5: a linear code is a subspace `C` of `Sigma^n` when `Sigma` is a
  field.
- Definition 8, printed page 5: a generator matrix has columns spanning a dimension-`k` code and
  induces a linear encoding map.
- Exercise 1, printed page 5: minimum distance equals minimum nonzero Hamming weight.
- Exercises 2 and 3, printed pages 6: systematic generator form and full-row-rank parity-check
  kernel representation.
- Lemma 9, printed page 6: minimum distance is characterized by dependent columns of a parity-check
  matrix.
- Definition 15 and Exercise 4, printed page 9: dual-code definition, dimension, double dual, and
  generator/parity-check relationships.

These are distinct definitions, exercises, and theorems. The source therefore helps discriminate
the family but does not select one root on the repository's behalf. Its observed external PDF
SHA-256 is `9948552eeea3d451644cb0c5196a18f391ab197c0c23cd06b476e0350b1d0df8`.
No source copy is added to the repository; no H0 proposition, complete errata audit, or independent
source review is claimed.

## Component crosswalk

| Catalog component | Source lead surface | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `线性` / linear | Definition 7 requires a field and subspace | `Submodule F (I -> F)` or an equivalent matrix image/kernel | object definition only; field and representation open |
| `码` / code | Definition 3 treats a block code as a subset of words | a set/submodule of a finite function type | alphabet, block length, finiteness, and encoder convention open |
| `纠错` / error correcting | Lemma 6 relates distance to correction and detection | `hammingDist`, a corruption relation, and a decoder correctness predicate | no decoder, radius, error model, or conclusion supplied |
| generator representation | Definition 8 and Exercise 2 | `Matrix.mulVec`, `Matrix.mulVecLin`, image/range, rank | candidate theorem family, not selected |
| parity-check representation | Exercise 3 | kernel of a matrix linear map | candidate theorem family, not selected |
| distance property | Exercise 1 and Lemma 9 | `hammingNorm`, nonzero minimum, column dependence | minimum conventions and exact claim open |
| duality | Definition 15 and Exercise 4 | orthogonal submodule and dimension APIs | belongs also near `THM-C-0377`; not selected here |

There is no row for an exact conclusion because the repository provides none. The canonical human
statement, ordered binders, hypotheses, conclusion, and formal expression remain null rather than
being inferred from the source lead.

## Formal candidate boundary

A bounded search over pinned mathlib and repository-local Lean found Hamming-space infrastructure
but no obvious exact `linear code`, `LinearCode`, `codeword`, or `error-correcting code` declaration.
The following are discovery candidates only:

- `Mathlib.InformationTheory.Hamming`: `hammingDist`, `hammingNorm`, `Hamming`, and metric/weight
  lemmas;
- `Mathlib.LinearAlgebra.Matrix.ToLin`: `Matrix.mulVec`, `Matrix.mulVecLin`, and
  `Matrix.mulVecLin_apply`; and
- generic `Submodule` and finite-dimensional linear-algebra APIs imported transitively.

They do not package a source-selected code, establish a generator or parity-check representation,
state a minimum-distance or duality result for that code, or prove decoder correctness. No proof
body is credited, and the downstream anchor audit remains open.

## Exact-statement blocker

The first failed theorem gate is source target identity. The catalog names a code class, whereas the
inspected source lead contains multiple inequivalent claims. Choosing Definition 7, Exercise 1,
Exercise 3, Lemma 9, Exercise 4, or another familiar theorem would invent or substitute
mathematics. Retry requires an immutable reviewed source decision that selects one exact result and
maps every incorporated definition, premise, conclusion, boundary case, proof passage, and erratum.
