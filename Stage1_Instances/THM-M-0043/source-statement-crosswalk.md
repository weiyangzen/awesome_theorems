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

## Selected authoritative statement source

Sheldon Axler, *Linear Algebra Done Right*, fourth edition, Section 7B, Theorem 7.31 (book pages
246-247), "complex spectral theorem," states for a finite-dimensional complex inner-product space
`V` and `T ∈ L(V)` that the following are equivalent: `T` is normal; `T` has a diagonal matrix with
respect to some orthonormal basis; and `V` has an orthonormal basis of eigenvectors of `T`.

The official PDF at `https://linear.axler.net/LADR4e.pdf` was inspected on 2026-07-13 and had
SHA-256 `45f821b6f51e1f6c42728db6254699d89c14c90fcdb2443c1341188672815d03`.
The statement phase selects the implication from Axler 7.31(a) to 7.31(b): normality implies
diagonal form in an orthonormal basis. This fixes complex scalars, finite dimension, the sole
normality antecedent, and the one-way conclusion that the catalog gloss requests. It is not a
historically primary Hilbert source and does not ratify the catalog attribution. No independent
reviewer has admitted its definitions, proof boundary, errata, and full source genealogy, so the
human status remains `H1`, not `H0`.

## Clause crosswalk

| Repository phrase or source component | Frozen mathematical meaning | Lean surface | Statement status |
|---|---|---|---|
| "matrix" | a square matrix on a nonzero finite-dimensional space | `Matrix n n Complex`, `[Fintype n]`, `[DecidableEq n]`, `[Nonempty n]` | frozen; empty index excluded |
| "normal" | commute with the conjugate transpose | `IsStarNormal A` | frozen sole antecedent |
| "unitarily" | change by a unitary matrix | `U : Matrix.unitaryGroup n Complex` | frozen subtype witness |
| "diagonalizable" | unitary similarity to a diagonal matrix | `A = U * Matrix.diagonal d * star U` | frozen canonical orientation |
| Axler 7.31(a) to (b) | normal implies diagonal in an orthonormal basis over `Complex` | finite matrix/unitary encoding above | selected claim; source review remains H1 |
| `已验证` | untrusted inventory label | no Lean declaration or proof body | explicitly rejected as evidence |

## Checked matrix transport

`Statement.lean` freezes `SpectralTheoremTarget` with the two direct imports
`Mathlib.Data.Complex.Basic` and `Mathlib.LinearAlgebra.UnitaryGroup`. The declaration
`spectralTheoremTarget_iff_explicitUnitaryMembershipTarget` checks that carrying `U` as a unitary
subtype is equivalent to carrying a matrix and its membership proof. The declaration
`spectralTheoremTarget_iff_conjugatedDiagonalTarget` uses both unitary inverse identities to check
the equivalence between `A = U * diagonal d * star U` and
`star U * A * U = diagonal d`.

The source is phrased using an orthonormal basis. For a fixed coordinate space, a matrix whose
columns are that basis is unitary, and its change-of-basis equation has the second checked
orientation above. The statement phase freezes this standard finite matrix encoding but does not
claim a proof of Axler's spectral theorem or H0 historical/source fidelity.

## Adjacent pinned candidate boundary

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

## Remaining source gate

Independent review must still admit the Axler edition, incorporated definitions, proof boundary,
errata status, and matrix/orthonormal-basis crosswalk, and must resolve the separate Hilbert/1906
attribution. Those open source tasks keep the root at `H1`. The exact Lean statement, direct imports,
two transports, expression fingerprint, and four mutation classes are now frozen at `M3`; no proof
body or theorem-completion credit follows.
