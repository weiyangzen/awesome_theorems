# THM-M-1474 scope map

## Preserved repository scope

The literal repository boundary is the topic `von Neumann稳定性分析`, glossed only as
`有限差分的稳定性分析`. This identifies Fourier-mode stability analysis for finite-difference
methods as a subject family. It does not select one mathematical proposition.

A common scalar, constant-coefficient, one-step, infinite- or periodic-grid analysis inserts a
Fourier mode into a recurrence and obtains an amplification factor `G(theta)`. Under additional
conditions, a bound such as `|G(theta)| <= 1` for all admissible frequencies controls an
`l2` norm. That familiar route is only one candidate. Systems yield amplification matrices;
multistep schemes yield characteristic roots; nonnormal symbols require power bounds rather than a
bare spectral-radius bound; and boundary closures need analysis not captured by the infinite-grid
symbol. None of these choices is fixed at intake.

## Decisions required at statement freeze

1. Select an immutable source proposition and decide whether it is a necessary condition,
   sufficient condition, equivalence, or a scheme-specific stability calculation.
2. Fix the continuous model: PDE or class, space dimension, domain, coefficients, initial and
   boundary data, solution notion, and regularity assumptions.
3. Fix the discretization: spatial and temporal grids, step sizes, stencil, one-step or multistep
   recurrence, scalar or system state, constant or variable coefficients, and boundary closure.
4. Fix the stability predicate: norm, finite or infinite time, uniformity in mesh parameters,
   permitted growth constant, time horizon, and exact parameter restrictions.
5. Fix the Fourier model: finite periodic or infinite lattice, transform normalization, frequency
   domain and endpoint convention, admissible modes, and the relation between physical and Fourier
   norms.
6. Fix the symbol: scalar amplification factor, matrix-valued symbol, or characteristic
   polynomial; normality, diagonalizability, uniform condition numbers, root multiplicities, and
   the distinction between spectral radius and uniform powers.
7. Fix the exact conclusion and quantifier order. Pointwise `|G(theta)| <= 1`, a uniform matrix
   power bound, an `l2` stability estimate, necessity, sufficiency, and equivalence are not
   interchangeable.
8. Fix exact versus floating-point arithmetic, roundoff and computation boundaries, universes,
   foundation/TCB profiles, minimal imports, expression fingerprints, checked transports, and all
   statement mutations.

## Boundary cases

The statement phase must decide zero and negative step sizes; empty or singleton grids; zero and
Nyquist frequencies; equality on the unit circle; repeated unit-modulus roots; zero modes and
constant solutions; vanishing or singular coefficients; finite versus infinite time; scalar versus
matrix symbols; defective or nonnormal amplification matrices; periodic, inflow, outflow,
reflecting, and other boundary closures; and exact versus floating-point evaluation.

No case is excluded at intake. Assuming the desired stability estimate, a uniform power bound, or
the amplification condition as a structure field would be circular if the selected root is meant
to establish it.

## Candidate statements not credited

- Scalar one-step periodic/infinite-grid equivalence between `l2` stability and
  `|G(theta)| <= 1` under source-specified hypotheses.
- A necessary von Neumann condition for a stable constant-coefficient finite-difference scheme.
- A sufficient matrix-symbol criterion with normality or a uniform diagonalization/power bound.
- Scheme-specific FTCS heat, upwind, Lax-Friedrichs, Lax-Wendroff, leapfrog, or other stability
  calculations.
- A multistep root-condition theorem or a finite-grid discrete Fourier version.

These are proposition-changing alternatives. Intake admits none without a source decision and
independent review.

## Neighbor and substitution exclusions

- `THM-M-1465` finite difference methods names the broader PDE discretization family and provides
  no inherited statement or proof credit.
- `THM-M-1472` Lax equivalence relates consistency, stability, and convergence under its own
  hypotheses; it cannot silently become this root.
- `THM-M-1473` CFL is a separately cataloged domain-of-dependence condition, not the same as a
  Fourier amplification criterion.
- `THM-M-1475` Runge-Kutta stability concerns ODE stability functions/regions unless a checked
  method-of-lines bridge and exact source say otherwise.
- Plancherel alone, the inequality that spectral radius is bounded by operator norm, a Fourier
  transform API, or an assumed diagonalization does not define or prove a scheme stability result.
- A numerical plot, sampled frequency sweep, floating-point experiment, theorem-name match, or the
  catalog's `已验证` label supplies no H or M credit.

## Formal and execution boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`MeasureTheory.Lp.fourierTransformₗᵢ` provides an `L2` Fourier linear isometry equivalence,
`MeasureTheory.Lp.norm_fourier_eq` is a Plancherel norm identity, `spectralRadius` defines the
abstract Banach-algebra spectral radius, and `spectrum.spectralRadius_le_nnnorm` bounds it by the
norm. These are possible substrate only. They do not provide a lattice transform, selected
finite-difference recurrence, scheme symbol, boundary treatment, or stability equivalence.

A bounded exact-topic search found no source-selected von Neumann finite-difference stability
declaration in pinned mathlib or repo-local Lean. This is intake discovery, not an exhaustive
anchor audit or global absence proof. Later phases own candidate provenance, obligation freezing,
typed graphs, proof bodies, composition, trust, readable reconstruction, and release evidence.
