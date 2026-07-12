# Scope map

## Preserved theorem family

The intake preserves the algebraic stability criterion named by the catalog: relating strict
left-half-plane roots of a real polynomial to signs of determinants formed from its coefficients.
The source-selected root is not yet frozen. Candidate components, none credited as the theorem,
include:

- a degree-`n` polynomial `p(z) = a_0 z^n + a_1 z^(n-1) + ... + a_n` with real coefficients and
  positive leading coefficient;
- stability meaning every complex root has strictly negative real part;
- the finite `n x n` Hurwitz matrix whose alternating coefficient rows begin
  `[a_1, a_3, ...]`, `[a_0, a_2, ...]`, followed by shifted copies, with out-of-range
  coefficients zero; and
- positivity of each leading principal determinant, indexed from `1` through `n`, as an
  `if and only if` criterion.

Hurwitz's 1895 pages 273-274 and Barkovsky's Theorem 40 support that candidate family. They do not
authorize intake to resolve every formal convention or to claim the statement gate.

## Decisions required at statement freeze

1. Select an approved source edition and exact theorem passage; record translation, incorporated
   definitions, proof boundary, corrections or errata, and independent review.
2. Fix whether `n` is positive, how a degree-`n` polynomial is represented, and whether coefficients
   are a vector, function, or extracted from `Polynomial R` in descending order.
3. Fix the real coefficient domain, the embedding into complex polynomials, and whether root
   multiplicity affects the logical statement or only the root carrier.
4. State the exact leading coefficient premise. Merely padding a lower-degree polynomial to length
   `n + 1` is not equivalent to requiring degree `n` and `a_0 > 0`.
5. Define stability as strict `re z < 0` for every complex root. Closed-half-plane variants and
   nonpositive determinant variants are different and cannot be substituted.
6. Define every Hurwitz-matrix entry, row/column orientation, zero extension, finite index type,
   leading-principal submatrix, determinant, and the `k = 1, ..., n` range.
7. Decide whether the canonical root is Hurwitz determinant positivity, Routh-array sign behavior,
   another equivalent criterion, or a checked transport among them.
8. Freeze the exact equivalence directions, ordered binders, quantifier dependencies, hypotheses,
   conclusion, foundation profile, minimal imports, and all required mutations.

For a future `p : Polynomial Real` representation with `p.natDegree = n`, Lean's coefficients are
ascending, so source coefficient `a_j` must be transported as `p.coeff (n - j)`. With zero-based
row `i` and column `j`, the displayed source matrix has coefficient index `2 * j + 1 - i` when
`i <= 2 * j + 1` and that index is at most `n`, and zero otherwise. This formula is a design note,
not a frozen definition; the statement phase must compile and cross-check it against the displayed
source matrix before use.

## Degenerate and boundary cases

Source review must explicitly dispose of `n = 0`; the zero polynomial; a vanishing or negative
leading coefficient; a coefficient list with trailing zeros that lowers the degree; roots on the
imaginary axis, including zero; repeated roots; zero Hurwitz determinants; nonnegative rather than
positive minors; complex coefficients; reversal or rescaling of coefficients; empty determinant
conventions; and the relation between the final determinant and the constant coefficient.

## Substitution exclusions

- A low-degree criterion (quadratic, cubic, quartic, or a numeric example) cannot replace the
  arbitrary finite-degree theorem family.
- A Routh table algorithm, count of right-half-plane roots, Lienard-Chipart reduction, discrete-
  time Schur/Jury stability test, or Lyapunov matrix criterion is a different theorem unless an
  approved checked transport is supplied.
- Barkovsky's ascending-coefficient reciprocal-polynomial exercise and Holtz's infinite-matrix
  factorization are not silently identical to the finite descending-coefficient theorem.
- Nonnegative Hurwitz minors do not justify a closed-left-half-plane conclusion; Barkovsky's
  Problem 45 explicitly warns that this implication is false.
- Generic polynomial roots, complex real parts, matrices, submatrices, or determinants are only
  substrate. A definition, structure field, or hypothesis that assumes the desired equivalence is
  not a proof.
- The catalog's `verified` label, the source scans, and the API probe provide no machine-proof
  credit.

## Formal boundary

Pinned mathlib provides `Polynomial.IsRoot`, `Polynomial.roots`, `Polynomial.map`, complex real
parts, finite matrices, submatrices, and determinants. The intake probe checks those names only.
The statement phase must build a source-mapped coefficient/Hurwitz-matrix interface, minimize
imports, elaborate and fingerprint one exact proposition, and mutation-test the required changes.
No obligation registry or proof graph is frozen at intake.
