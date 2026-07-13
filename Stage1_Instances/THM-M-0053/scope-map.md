# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-0053`, title `盖尔圆盘定理`, attribution Semyon Gershgorin,
year 1931, and the gloss `矩阵特征值的定位定理`. The record supplies no bibliography, formula,
definition, ordered binders, hypotheses, conclusion, proof boundary, correction history, or formal
artifact. Importance `中` and status `已验证` are inventory metadata only.

The title and attribution identify the Gershgorin circle/disc theorem family. They do not select
one exact truth-valued proposition. The most likely basic reading is that every eigenvalue of a
finite square complex matrix lies in at least one closed row disc centered at a diagonal entry,
whose radius is the sum of absolute values of the other entries in that row. This is a candidate
scope, not a frozen canonical statement.

## Decisions required at statement freeze

1. Preserve a lawful immutable source edition, select a pinpoint result and proof boundary, map
   every incorporated definition and assumption, audit corrections, and obtain independent review.
2. Fix the scalar domain: complex numbers as in the classical disc theorem, or a justified
   generalization to an arbitrary `NormedField` as in the pinned mathlib candidate.
3. Fix the square matrix representation and finite index type: `Matrix (Fin n) (Fin n) Complex`,
   another nonempty finite type, or the arbitrary finite type used by mathlib.
4. Choose row discs or column discs and prove any credited transpose transport. Do not combine
   both conventions by name alone.
5. Fix the eigenvalue encoding: characteristic-polynomial root, existence of a nonzero eigenvector,
   or `Module.End.HasEigenvalue (Matrix.toLin' A) mu`, with checked transports as needed.
6. Define each radius as the sum excluding the diagonal and fix closed-disc membership versus the
   equivalent norm inequality.
7. Decide whether the target is only the basic union/localization inclusion or also Gershgorin's
   stronger claim that a disjoint union of `k` discs contains exactly `k` eigenvalues counting
   multiplicity. The latter is not supplied by `eigenvalue_mem_ball`.
8. Freeze ordered binders, universes, typeclass instances, foundation/TCB/computation profiles,
   alternate encodings, and all boundary cases before the statement gate.

## Degenerate and boundary cases

No case is excluded at intake. Source review must dispose of the empty index type, dimensions zero
and one, the zero matrix, diagonal and scalar matrices, zero radii, repeated eigenvalues, defective
matrices, repeated or coincident discs, overlapping connected components, and eigenvalues lying on
disc boundaries. It must also decide whether multiplicity is set-level, algebraic, or absent.

The pinned theorem handles an empty index type vacuously because the eigenvalue hypothesis is then
impossible; that implementation fact must not silently determine the source theorem's dimension
convention. Likewise, a theorem generalized from complex matrices to arbitrary normed fields needs
an approved source-to-generalization relationship rather than mere type compatibility.

## Neighbor and substitution exclusions

- The row and column strict diagonal-dominance determinant corollaries in the same mathlib module
  are applications, not substitutes for eigenvalue localization.
- A spectral-radius-only upper bound, diagonal-dominance invertibility result, or one finite
  numerical example does not prove the union-of-discs statement.
- Brauer Cassini ovals, Schur decomposition, the spectral theorem, Perron-Frobenius, and generic
  eigenvalue existence are related but distinct targets.
- The component-counting refinement cannot be dropped if a reviewed source selects it; conversely,
  it cannot be added merely because some expositions call both claims Gershgorin's theorem.
- A column-disc theorem, fixed-dimension special case, or real/symmetric-only result cannot replace
  a source-selected complex row-disc root without a checked relationship.
- A structure, hypothesis, axiom, oracle, or certificate storing the desired localization is not a
  proof. The catalog's `已验证` label and the discovery probe supply no proof credit.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.LinearAlgebra.Matrix.Gershgorin` contains `eigenvalue_mem_ball`, whose conclusion is row
closed-ball membership for some finite index. The same file contains determinant applications for
strict row and column diagonal dominance. The probe checks these interfaces only. No canonical Lean
target, elaborated-expression hash, checked source transport, statement mutation suite, accepted
terminal-body provenance, obligation registry, or proof receipt is created at intake.
