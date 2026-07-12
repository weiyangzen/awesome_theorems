# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:328-333` supplies only:

- title: `谱定理`;
- attribution: David Hilbert;
- year: 1906;
- claim: `正规矩阵可酉对角化` ("normal matrices are unitarily diagonalizable");
- importance: high; and
- untrusted formalization status: `已验证`.

Git blame places all six uncited fields at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:1294-1319`
repeats them while explicitly leaving exact definitions, premises, proof route, equivalent forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest resets this target to
`L0 / rework_required` and preserves `已验证` only as untrusted metadata.

The repository supplies no source title, publication, edition, theorem/page, quotation,
bibliography, definition, erratum, or reviewer that ties Hilbert in 1906 to this exact finite
normal-matrix formulation. The attribution and date are therefore catalog identity fields, not an
accepted primary-source citation.

## Inspected authoritative source lead

Sheldon Axler, *Linear Algebra Done Right*, fourth edition, Section 7B, Theorem 7.31 (book pages
246-247), "complex spectral theorem," states for a finite-dimensional complex inner-product space
`V` and `T ∈ L(V)` that the following are equivalent: `T` is normal; `T` has a diagonal matrix with
respect to some orthonormal basis; and `V` has an orthonormal basis of eigenvectors of `T`.

The official PDF at `https://linear.axler.net/LADR4e.pdf` was inspected on 2026-07-13 and had
SHA-256 `45f821b6f51e1f6c42728db6254699d89c14c90fcdb2443c1341188672815d03`.
The theorem is an authoritative modern source lead and matches the intended mathematical family.
It is not a historically primary Hilbert source, does not by itself ratify the catalog attribution,
and is phrased for operators and orthonormal bases rather than an explicit matrix unitary-conjugacy
equation. No independent reviewer has admitted its definitions, proof boundary, errata, and exact
matrix transport, so the current human status remains `H1`, not `H0`.

## Clause crosswalk

| Repository phrase or candidate component | Required mathematical meaning | Prospective Lean surface | Intake status |
|---|---|---|---|
| "matrix" | a square matrix indexed by a finite type | `Matrix n n ℂ`, `[Fintype n]`, `[DecidableEq n]` | exact field and binders absent |
| "normal" | commute with the conjugate transpose | `IsStarNormal A`, exposed by `isStarNormal_iff` | predicate available; source convention open |
| "unitarily" | change by a unitary matrix or orthonormal basis | `Matrix.unitaryGroup n ℂ`, `Matrix.mem_unitaryGroup_iff` | API available; orientation open |
| "diagonalizable" | existence of diagonal data and a unitary similarity equation | `Matrix.diagonal d` plus a unitary conjugation equation | witness and equality form absent |
| Axler 7.31 | normal iff diagonal in an orthonormal basis over `ℂ` | matrix/linear-map and basis/unitary transports | strong source lead; transport unchecked |
| `已验证` | untrusted inventory label | no Lean declaration or proof body | explicitly rejected as evidence |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.Matrix.Spectrum` provides `Matrix.IsHermitian.spectral_theorem`. Its type states
that an `RCLike` Hermitian matrix is a unitary conjugate of a real diagonal matrix, and its axiom
report is `[propext, Classical.choice, Quot.sound]`. `IntakeProbe.lean` authenticates that theorem,
the normality predicate, unitary group, and diagonal constructor under the pinned environment.

This is not the received theorem: Hermitian matrices form a strict subclass of complex normal
matrices, and the candidate forces real eigenvalues. The repo-local legacy wrapper
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_192.lean` exposes the same Hermitian theorem for
the unrelated `THM-M-1524` boundary. A bounded search found no finite normal-matrix unitary
diagonalization declaration in repo-local Lean or pinned mathlib. That observation is intake
discovery only, not an exhaustive anchor audit or proof of external absence.

## First source gate

The statement phase must preserve and independently review one lawful source edition, select the
exact theorem and incorporated definitions, resolve the scalar field and Hilbert/1906 provenance,
map every ordered binder, hypothesis, conclusion, equality convention, and boundary case, and then
freeze and mutation-test the exact Lean expression. Until then the canonical mathematical and Lean
targets remain null, no source-to-formal transport is credited, and the root remains H1/M3/R4.
