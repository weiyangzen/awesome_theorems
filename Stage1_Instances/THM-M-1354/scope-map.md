# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1354`, the title `特征指数`, the gloss
`周期系统的特征值`, the attribution to Gaston Floquet, and the year 1883. Importance `high` and
status `已验证` are catalog metadata, not human-source or kernel evidence.

The title and gloss locate the Floquet spectral family but do not identify one truth-valued root.
A later statement phase may select a proposition only from an immutable, independently reviewed
source passage and must preserve the neighboring target boundaries.

## Candidate interpretations not credited

1. Floquet or characteristic multipliers as eigenvalues of a one-period monodromy matrix.
2. Characteristic exponents `mu` related to multipliers `rho` by `exp(T * mu) = rho`, with an
   explicit logarithm-branch equivalence.
3. Eigenvalues of a constant matrix `B` in a Floquet factorization `X(t) = P(t) exp(t B)`.
4. A theorem equating the preceding encodings, including algebraic multiplicity and base-time
   conjugacy.
5. A Floquet solution representation `x(t) = exp(mu * t) p(t)` for periodic or generalized
   periodic `p`.
6. A stability or asymptotic-stability criterion expressed through multiplier moduli or exponent
   real parts.

These interpretations have different binders, hypotheses, conclusions, branch conventions, and
proof dependencies. None is selected, asserted, or credited at intake.

## Proposition-changing decisions

Before the statement phase can close, an immutable source and independent review must fix:

- the exact numbered proposition or source-defined conjunction and its proof boundary;
- first-order systems versus higher-order scalar equations, and homogeneous versus inhomogeneous
  equations;
- real or complex scalar field, finite dimension, matrix or operator state model, and all Lean
  universes and typeclass assumptions;
- the coefficient function, its regularity, global solution assumptions, and a strictly positive
  period versus a minimal or nonminimal period;
- the solution-matrix convention, normalization and base time, multiplication orientation,
  invertibility, and exact definition of the monodromy matrix;
- whether the primary object is a multiplier, an exponent, a logarithm-matrix eigenvalue, or a
  checked equivalence among them;
- the scalar or matrix exponential convention, existence and field of a logarithm, branch choices,
  and equivalence modulo integer multiples of `2 * pi * i / T`;
- algebraic versus geometric multiplicity, repeated and defective spectral values, and whether
  Jordan data enters the conclusion;
- the exact existence, correspondence, invariance, representation, or stability conclusion and
  every ordered quantifier; and
- incorporated definitions, historical edition, translation, corrections or errata, source-node
  mapping, and every boundary case below.

## Degenerate and boundary cases

The selected source must resolve zero-dimensional and scalar systems; zero, negative, nonminimal,
or multiple periods; zero or constant coefficient matrices; identity monodromy; repeated or
defective multipliers; whether a multiplier can be zero; unit-circle multipliers; zero or purely
imaginary exponents; exponent branch changes; real monodromy without a selected real logarithm;
complexification and period doubling; singular solution-matrix candidates; changing the base time;
and whether generalized eigenvectors rather than eigenvectors are required.

## Neighbor and substitution exclusions

- `THM-M-1352` owns the broader Floquet-theory catalog target. A theory chapter or conjunction of
  all Floquet results cannot replace this spectral label.
- `THM-M-1353` owns the fundamental-matrix Floquet-theorem target. A shift identity or
  factorization alone is not silently adopted here.
- `THM-M-1355` owns linear-system stability. A multiplier-modulus or exponent-real-part criterion
  cannot be substituted without an exact source decision.
- An eigenvalue theorem for an arbitrary matrix, matrix-exponential invertibility, or a generic
  logarithm result is substrate rather than a periodic-system characteristic-exponent theorem.
- A structure or hypothesis that stores the desired monodromy, spectral correspondence, exponent,
  solution representation, or stability result provides no proof.
- A scalar example, numerical monodromy, floating-point eigenspectrum, or plotted trajectory does
  not replace a source-selected general theorem.
- The untrusted `已验证` label and the API probe provide no source-fidelity or proof credit.

## Formal boundary

Pinned mathlib exposes generic periodic functions, integral curves, matrices, matrix exponentials,
characteristic polynomials, algebra spectra, and eigenvalue predicates. The probe authenticates
those adjacent interfaces only. It neither defines a periodic linear system or its monodromy nor
states or proves a characteristic-multiplier or characteristic-exponent result.
