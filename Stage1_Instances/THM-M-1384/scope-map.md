# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1384`, the title `Sturm-Liouville理论`, the gloss
`二阶线性边值问题`, the attribution to Jacques Sturm and Joseph Liouville, and the date 1836.
Importance `high` and status `已验证` are inventory metadata, not human-source or kernel evidence.

The title identifies a mathematical theory and the gloss a problem family. Neither supplies a
truth-valued root. A later statement phase may select or correct a proposition only from an
immutable, independently reviewed source passage while preserving the neighboring target
boundaries below.

## Candidate interpretations not credited

1. Definition and well-posedness of a regular second-order boundary-value problem.
2. Existence or uniqueness for an inhomogeneous Sturm-Liouville equation.
3. Symmetry or self-adjointness of a differential-operator realization.
4. Reality, simplicity, discreteness, ordering, or lower boundedness of eigenvalues.
5. Orthogonality, completeness, or convergence of an eigenfunction expansion.
6. A Green-function or compact-resolvent construction.
7. A comparison, separation, oscillation, asymptotic, variational, or inverse-spectral theorem.
8. A singular, half-line, whole-line, periodic, coupled-boundary, or matrix-valued theory.

These readings have different binders, hypotheses, conclusions, exceptional cases, and proof
dependencies. None, including their conjunction, is asserted or credited at intake.

## Proposition-changing decisions

Before the statement phase can close, an immutable source and independent review must fix:

- one exact numbered proposition or explicitly delimited conjunction and its proof boundary;
- the sign and normalization of the equation, including whether the spectral parameter and weight
  occur in `-(p u')' + q u = lambda w u` or another checked form;
- a finite regular interval, half-line, whole line, singular endpoint, periodic domain, or abstract
  Hilbert-space formulation;
- real or complex scalars and the exact regularity, integrability, positivity, and nonvanishing
  assumptions on `p`, `q`, and the weight;
- classical, weak, almost-everywhere, first-order-system, or operator-domain solution semantics;
- separated Dirichlet, Neumann, Robin, mixed, periodic, antiperiodic, or coupled boundary forms,
  including all endpoint parameters and self-adjointness restrictions;
- the requested result: existence, uniqueness, Green representation, symmetry, self-adjointness,
  compactness, spectral properties, basis expansion, convergence, or another exact clause;
- every ordered quantifier, universe and typeclass assumption, incorporated definition, edition,
  page, correction or erratum, and source-to-clause mapping.

## Degenerate and boundary cases

The selected source must resolve an empty, reversed, or zero-length interval; zero, sign-changing,
discontinuous, or singular leading coefficient or weight; unbounded or complex potential; regular
versus singular endpoints; redundant or inconsistent boundary forms; a zero solution; zero or
repeated eigenvalues; empty, finite, one-sided, or two-sided spectrum; boundary eigenvalues and
spectral accumulation; real versus complex eigenfunctions; normalization; convergence topology;
and whether distributional or almost-everywhere equalities are admitted.

No case is excluded now because doing so without a selected proposition would alter the target.

## Neighbor and substitution exclusions

- `THM-M-1383` owns the general two-point boundary-value-problem theory.
- `THM-M-1385`, `THM-M-1386`, and `THM-M-1387` own comparison, separation, and oscillation.
- `THM-M-1388` owns the Sturm-Liouville eigenvalue-problem target.
- `THM-M-1389` and `THM-M-1390` own Weyl asymptotics and the Courant min-max principle.
- `THM-M-1391` and `THM-M-1392` own the Pruefer transformation and Green functions.
- A generic finite-dimensional eigenvalue theorem, compact spectral theorem, Fredholm alternative,
  local ODE theorem, or Rayleigh extremum is supporting substrate, not this root.
- A structure or hypothesis storing the desired solution, operator, spectrum, basis, or conclusion
  is not a proof; neither is a numerical solver, discretization, plot, or floating-point spectrum.
- The `已验证` label and the discovery-only Lean probe provide no source or proof credit.

## Formal boundary

Pinned mathlib exposes generic derivative and ODE predicates and bounded-operator spectral tools.
The probe authenticates several such interfaces. It neither models an unbounded Sturm-Liouville
operator with a source-selected domain and boundary conditions nor states any candidate root.
