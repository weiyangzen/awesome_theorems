# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1390`, the label `Courant极小极大原理`, Richard Courant,
the year 1920, the gloss `特征值的变分刻画`, and an untrusted `已验证` status. Intake preserves
that eigenvalue-variational theorem-family boundary. It does not replace the sparse record with a
familiar Courant-Fischer statement or assume that a historical PDE formulation is canonical.

## Proposition-changing decisions

An approved source decision must freeze all of the following before statement elaboration:

- the operator model: finite Hermitian matrix, bounded self-adjoint operator, compact self-adjoint
  operator, semibounded unbounded operator or closed quadratic form, Sturm-Liouville operator, or
  Courant's elliptic differential expression;
- scalar field, universes, Hilbert or function space, operator/form domain, density and closure,
  real versus complex conventions, and whether the spectrum is finite or discrete;
- the coefficients, domain regularity, measure or weight, and Dirichlet, Neumann, Robin, mixed, or
  another boundary condition for a differential-operator version;
- self-adjointness/symmetry, compactness or compact resolvent, semiboundedness, regularity, and every
  condition that makes the indexed eigenvalues and variational extrema exist;
- whether eigenvalues are ordered increasingly or decreasingly and repeated by multiplicity, the
  index origin, finite-rank and kernel behavior, and which spectral threshold cases are allowed;
- the Rayleigh quotient or energy functional and its normalization, treatment of the zero vector,
  and use of minimum/maximum versus infimum/supremum;
- the competitor class: dimension-`k` subspaces with a max, codimension-`k-1` constraints with a
  min, arbitrary test functions `v_i`, orthogonal complements, or a quadratic-form subspace; and
- one exact equality, including quantifier order, attainment, dual form, all hypotheses, and every
  exceptional case.

These choices yield inequivalent propositions. They are a resolution ledger, not a canonical claim.

## Candidate families not credited

- Courant's 1920 Satz 3a for the nth eigenvalue of a weighted self-adjoint elliptic boundary-value
  problem, expressed as the maximum over `n-1` test functions of a constrained energy infimum.
- The finite-dimensional Courant-Fischer theorem for a Hermitian matrix or self-adjoint linear map,
  in either min-max or max-min orientation.
- The min-max principle for a compact self-adjoint operator on a Hilbert space.
- A semibounded self-adjoint operator or closed quadratic-form theorem below the essential spectrum.
- A Sturm-Liouville specialization with source-fixed interval, coefficients, weight, and boundary
  conditions.

No family in this list is selected, conjoined, asserted, or credited at intake.

## Neighbor and substitution boundaries

- `THM-M-0055` separately names the Rayleigh quotient theorem and explicitly mentions Hermitian
  matrix eigenvalues. A global smallest/largest Rayleigh-quotient result cannot substitute for the
  nth-eigenvalue Courant principle.
- `THM-M-1384` Sturm-Liouville theory, `THM-M-1388` eigenvalue problems, `THM-M-1389` Weyl's
  asymptotic formula, and `THM-M-1391` the Pruefer transform remain distinct targets. Their future
  statements and evidence cannot close this one.
- A definition of a Rayleigh quotient, sorted eigenvalue list, eigenbasis, or orthogonality API is
  substrate, not the min-max equality.
- A theorem for only the top or bottom eigenvalue is not the indexed result unless an approved
  source explicitly selects that boundary case.
- A structure field, hypothesis, or typeclass that assumes the min-max equality is an interface,
  not a proof.
- Numerical eigensolver output, discretization, floating-point comparison, or finite test samples
  are not proof of the source-selected variational equality.
- The catalog label `已验证` supplies neither human-source fidelity nor kernel evidence.

## Boundary cases

The statement phase must decide zero-dimensional and one-dimensional spaces; `n = 0` versus
one-based indexing; `n` beyond the finite dimension; repeated eigenvalues; zero eigenspaces and
nontriviality assumptions; empty competitor classes; zero test vectors; unattained infima or
suprema; noncompact operators and essential spectrum; unbounded operators and vectors outside the
form domain; nonsymmetric or non-self-adjoint operators; indefinite/unbounded-below forms; singular
weights or coefficients; disconnected, unbounded, or irregular domains; every boundary-condition
variant; and whether extrema are asserted to be attained.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks a Rayleigh quotient, sphere
infimum/supremum transports, extremal-eigenvalue existence, and finite-dimensional sorted
eigenvalues. A bounded name/topic search found no `Courant`, `Fischer`, or eigenvalue-minimax
declaration in pinned mathlib or repo-local Lean. This is intake discovery only, not an exhaustive
anchor audit or proof of absence from external projects.
