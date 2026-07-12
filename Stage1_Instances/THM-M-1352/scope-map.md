# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1352`, the title `Floquet理论`, the gloss `周期线性系统的理论`,
the attribution to Gaston Floquet, and the year 1883. Importance `high` and status `已验证` are
catalog metadata, not human-source or kernel evidence.

The title names the theory of periodic linear systems. It does not specify one truth-valued root.
A later statement phase may select a result only from an immutable, independently reviewed source
passage and must respect the separately cataloged neighboring targets.

## Candidate families not credited

The following are distinct discovery hypotheses, not accepted formulations of this target:

1. Period-shift identities for a principal or fundamental matrix solution, including the monodromy
   iteration relation.
2. A Floquet normal-form decomposition such as `X(t) = P(t) exp(t B)` with a periodic factor.
3. A real decomposition, perhaps after doubling the coefficient period, versus a complex
   decomposition at the original period.
4. Definition and invariance properties of Floquet multipliers or characteristic exponents.
5. Reducibility of the periodic system to one with constant coefficients.
6. Stability or asymptotic-stability criteria in terms of multipliers, exponents, or Jordan data.
7. Periodic-solution criteria, scalar or higher-order variants, and applications such as Hill's
   equation.

These results have different binders, assumptions, conclusions, proof dependencies, and boundary
cases. A chapter or theory label cannot silently turn their collection into one conjunction.

## Proposition-changing decisions

Before the statement phase can close, an immutable source and independent review must fix:

- the exact numbered theorem, lemma, corollary, or source-defined conjunction and proof boundary;
- first-order systems versus higher-order scalar equations, and homogeneous versus inhomogeneous
  equations;
- real or complex scalar field, finite dimension or another state space, matrix/operator model, and
  every universe and typeclass assumption;
- the coefficient function's domain, continuity or weaker regularity, and any boundedness or
  integrability assumptions;
- a positive period, whether it must be minimal, and whether conclusions use that period or twice
  that period;
- the solution notion and existence interval, principal/fundamental matrix normalization, base
  time, invertibility, multiplication convention, and monodromy definition;
- whether a matrix logarithm is required, over which field, with what existence theorem and branch
  or nonuniqueness policy;
- the exact periodic-factor, normal-form, multiplier, exponent, reducibility, solution, or stability
  conclusion and its ordered quantifiers;
- incorporated definitions, historical genealogy, translation, corrections or errata, and the
  source-to-proof-node mapping; and
- every boundary case listed below.

## Degenerate cases to resolve

- zero-dimensional systems, empty index types, and scalar one-dimensional systems;
- zero, constant, or identity coefficient matrices and trivial dynamics;
- zero, negative, nonminimal, or multiple periods;
- singular fundamental-matrix candidates and normalization at a different base time;
- real monodromy matrices with no real logarithm, complex logarithm branch choices, and period
  doubling;
- repeated or defective multipliers, zero multipliers, multipliers on the unit circle, and Jordan
  blocks;
- zero or purely imaginary exponents and exponent ambiguity modulo integer multiples of
  `2 * pi * i / T`;
- merely measurable, discontinuous, piecewise-continuous, or unbounded coefficients;
- forward-only, local, half-line, or global solution domains; and
- periodic solutions versus periodic coefficient matrices.

## Neighbor and substitution exclusions

- `THM-M-1353` Floquet theorem or its fundamental-matrix decomposition cannot be substituted for
  the broader, underspecified theory label.
- `THM-M-1354` characteristic exponents and `THM-M-1355` linear-system stability retain their own
  target ownership; their conclusions cannot be bundled into this target without source review.
- Generic periodic functions, integral curves, matrices, determinants, exponentials, or an
  invertible exponential are infrastructure, not Floquet theory.
- A structure that stores the desired decomposition, monodromy relation, logarithm, spectral data,
  reducibility, or stability conclusion as a field supplies no proof.
- A scalar example, numerical fundamental matrix, sampled monodromy, floating-point spectrum, or
  plotted solution is not a substitute for the general source-selected theorem.
- The repository's `已验证` label and this intake probe carry no source-fidelity or proof credit.

## Formal boundary

Pinned mathlib exposes `Function.Periodic`, global and local integral-curve predicates, finite
matrices and determinants, and matrix-exponential results. The probe authenticates those adjacent
interfaces only. No principal-matrix, fundamental-matrix, monodromy-matrix, Floquet decomposition,
or characteristic-exponent target has been frozen, and the later exhaustive anchor audit remains
open.
