# Scope map

## Preserved source family

The intake preserves the family named by the catalog: convert a Sturm-Liouville solution and a
weighted derivative into amplitude and phase variables, then use phase evolution to analyze the
problem. A later statement phase may select an exact root only from an immutable, independently
reviewed source passage. Candidate components, none yet credited as the theorem, include:

- a Sturm-Liouville equation on a real interval, in divergence or first-order Hamiltonian form;
- a nontrivial real solution paired with its derivative or quasi-derivative;
- polar or modified-polar coordinates with a nonnegative or positive amplitude and a phase defined
  modulo a period or as a continuous real lift;
- a source-specific first-order equation for phase and another for amplitude;
- equivalence or reconstruction between the original and transformed systems;
- zeros of the solution represented by phase crossings; and
- monotonicity in position or spectral parameter and an oscillation/eigenvalue consequence.

## Decisions required at statement freeze

1. Select and independently review one complete source result. Identify whether the root is the
   coordinate construction, forward transformed equations, an iff/reconstruction theorem, a
   zero-count theorem, phase monotonicity, or a larger oscillation/spectral theorem.
2. Fix the equation and signs: for example `(k u')' + (l + lambda r) u = 0`,
   `-(p y')' + q y = lambda w y`, or a source-equivalent system. Map every coefficient across
   normalizations rather than treating notation changes as definitional.
3. Fix the interval, endpoint inclusion, scalar field, parameter domain, coefficient regularity,
   positivity or nonvanishing assumptions, and classical/weak/Caratheodory solution notion.
4. Fix the state pair: `(u, u')`, `(u, k u')`, a scaled pair, or a canonical-system vector. State
   the precise relationship between the second-order equation and its first-order form.
5. Fix the convention. Pruefer's inspected page 503 uses `v = rho cos theta` and
   `u = rho sin theta`; modern sources may swap sine/cosine, signs, or scaling. State the amplitude
   range, phase period, initial phase, and whether equality is pointwise or modulo a period.
6. Explain why the state pair never vanishes simultaneously for the selected nontrivial solution,
   how a local/principal angle becomes a continuous real lift, and how phase is continued through
   zeros of either coordinate.
7. Freeze the exact phase and amplitude differential equations, their regularity, the direction of
   every implication, and the uniqueness or gauge freedom of reconstruction.
8. Fix boundary conditions and the phase conventions at each endpoint, including zero/Dirichlet,
   derivative/Neumann, Robin, separated, regular, singular, or whole-line variants.
9. Decide whether zero counting, separation, comparison, oscillation, eigenvalue simplicity or
   ordering, spectral asymptotics, or expansion is part of the root or only a downstream use.
10. Resolve all boundary cases and mutation-test removed assumptions, changed domains, binder
    scope, and endpoints before any proof artifact receives credit.

## Boundary and degenerate cases

The selected statement must decide zero and identically zero solutions; simultaneous zero of the
solution and quasi-derivative; zero, negative, or vanishing leading/weight coefficients; singular
endpoints; a point interval or reversed endpoints; complex-valued solutions; zeros of the sine or
cosine coordinate; amplitude sign and the `rho = 0` case; phase changes by integer multiples of
`pi` or `2*pi`; discontinuous principal arguments; eigenvalues at an endpoint convention; and
whether the spectral parameter is fixed or quantified.

No case is excluded at intake because no truth-valued root has been selected.

## Explicit exclusions

- `THM-M-1385` Sturm comparison, `THM-M-1386` Sturm separation, `THM-M-1387` oscillation theory,
  `THM-M-1388` the eigenvalue problem, `THM-M-1389` Weyl asymptotics, or `THM-M-1390` Courant's
  minimax principle substituted for this method label.
- A generic planar polar-coordinate identity or complex principal argument presented as a global
  continuous Pruefer phase.
- The unrelated mathlib Pruefer fixed-point subgroup or its group-theoretic consequences.
- A structure that stores the desired phase, transformed equations, zero count, or spectral
  conclusion as data or assumptions.
- One constant-coefficient oscillator or numerical phase plot used as the general result.
- The catalog's untrusted `verified` label, an API probe, or the historical paper title used as
  proof or exact-statement credit.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides generic integral-curve and
derivative predicates plus real/complex polar-coordinate APIs. Its `Complex.polarCoord` is an open
partial homeomorphism using the principal `Complex.arg`; it does not by itself construct the
continuous lifted phase required along a nonvanishing state curve. The bounded search found no
Sturm-Liouville or Pruefer-transform theorem. These observations are feasibility evidence only,
not exact-statement elaboration, an exhaustive anchor audit, or machine-proof evidence.
