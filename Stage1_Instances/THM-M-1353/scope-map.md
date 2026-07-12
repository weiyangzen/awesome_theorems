# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-1353`, the label `Floquet定理`, the gloss
`周期系统的基本解矩阵`, the attribution Gaston Floquet, and the year 1883. Importance "high" and
status `已验证` are untrusted catalog metadata, not theorem or proof evidence.

This identifies a result about fundamental matrices of periodic linear differential systems. It
does not select a scalar or first-order system, coefficient class, field, period convention,
normalization, fundamental-matrix predicate, or conclusion.

## Proposition-changing decisions

An approved statement phase must freeze all of the following from an immutable source:

- scalar higher-order equation versus first-order system `x' = A(t)x`, and left versus right
  multiplication conventions for matrix-valued solutions;
- time domain, finite dimension, scalar field `R` or `C`, topology/norm structures, and all Lean
  universes and typeclass assumptions;
- continuity, local integrability, or other regularity of `A`, its global domain, and the exact
  condition that `T` is a positive period rather than the vacuous period zero;
- the definition of a solution matrix and fundamental matrix, pointwise invertibility, and whether
  a normalized matrix `Phi(0) = I` or every fundamental matrix is quantified;
- whether the conclusion is the shift/monodromy identity `Phi(t+T)=Phi(t)Phi(T)`, a factorization
  `Phi(t)=P(t) exp(tB)`, reduction by `x=P(t)y`, a basis of Floquet solutions, or a conjunction;
- existence and field of the constant exponent matrix `B`, periodicity and invertibility of `P`,
  and the exact relationship to a logarithm of the monodromy matrix;
- complex-valued versus real-valued factors, including when `P` has period `T`, period `2T`, or
  needs extra hypotheses for a real logarithm;
- uniqueness or gauge ambiguity of `P` and `B`, ordered binders, endpoint semantics, and all
  equality orientations and coercions.

These choices produce inequivalent propositions. They are a resolution ledger, not a theorem.

## Candidate branches not credited

- For a normalized fundamental matrix, periodic coefficients imply a quasiperiodicity identity
  relating `Phi(t+T)` to the monodromy `Phi(T)`.
- Over `C`, a fundamental matrix has a Floquet representation `Phi(t)=P(t) exp(tB)` with a
  period-`T` matrix `P` and constant `B`.
- Over `R`, a real representation may require a period-`2T` factor or additional real-logarithm
  hypotheses; silently complexifying changes the domain and conclusion.
- A scalar `n`th-order periodic equation may be converted to a companion first-order system, but
  that conversion requires a checked source and formal transport.

No branch is selected, asserted, or credited at intake.

## Neighbor and substitution exclusions

- `THM-M-1352` is the broader Floquet-theory catalog target; this intake does not absorb its full
  solution-space, reduction, or stability scope.
- `THM-M-1354` separately catalogs characteristic exponents; their definition or spectral
  properties cannot replace a fundamental-matrix theorem.
- `THM-M-1355` separately catalogs stability of linear systems; a stability criterion or
  exponential dichotomy is not substituted for this target.
- A periodicity definition, matrix-exponential invertibility, local ODE existence, or an assumed
  fundamental matrix alone is not the Floquet theorem.
- A structure field or hypothesis may not assume the desired monodromy identity, logarithm,
  factorization, periodic factor, or constant-coefficient reduction.
- Numerical integration, sampled monodromy, floating-point eigenvalues, and the untrusted catalog
  label provide no source or kernel proof credit.

## Degenerate and boundary cases

The selected source must decide dimension zero, period zero and negative periods, the zero or
constant coefficient system, identity monodromy, repeated and non-diagonalizable multipliers,
singular candidate solution matrices, real matrices with no real logarithm, nonminimal periods,
and whether changing the base time changes the normalization or conjugates the monodromy.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib supplies `Function.Periodic`,
`IsIntegralCurve`, `NormedSpace.exp`, `Matrix.isUnit_exp`, and
`Matrix.GeneralLinearGroup`. A bounded target-name search found no Floquet or periodic-linear-ODE
fundamental-matrix theorem in pinned mathlib or repository-local Lean. The probe and search are
intake feasibility evidence only, not a complete anchor audit or external absence claim.
