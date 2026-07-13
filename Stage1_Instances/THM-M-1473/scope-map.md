# Scope map

## Preserved repository scope

The repository fixes only target `THM-M-1473`, the label `CFL条件`, Courant/Friedrichs/Lewy, the
year 1928, and the gloss `双曲型方程的稳定性条件`. This recognizes the CFL theorem family, but it is
not a truth-valued statement. In particular, it does not justify treating "CFL" as a universal
sufficient stability criterion.

The inspected 1928 source studies finite-difference approximations to several elliptic,
hyperbolic, and parabolic problems. Its hyperbolic part includes:

1. a one-dimensional wave equation on particular rectangular grids;
2. source-specific discrete recurrences and initial rows;
3. comparison of discrete and continuous domains of dependence;
4. nonconvergence when the discrete dependence region is too narrow;
5. convergence proofs in other mesh regimes under regularity and discrete-data convergence; and
6. higher-dimensional and more general linear hyperbolic extensions.

These are related propositions, not interchangeable statements of one unqualified stability rule.

## Candidate roots not selected or credited

- A general necessity theorem: convergence of a consistent approximation to a hyperbolic
  initial-value problem requires the numerical domain of dependence to contain the differential
  domain of dependence in the refinement limit.
- The source's one-dimensional wave-equation nonconvergence result when the spatial/time mesh
  ratio places the numerical dependence region strictly inside the physical one.
- The source's convergence theorem for the same wave equation in a permitted mesh-ratio regime,
  with its stated smoothness and discrete initial-data hypotheses.
- A scalar linear-advection upwind theorem with a Courant number such as `|a| * dt / dx <= 1`.
- A source-specific stability theorem for Lax-Friedrichs, Lax-Wendroff, leapfrog, finite-volume,
  finite-element, or another scheme.

No candidate receives canonical-statement, `H0`, machine, or proof credit at intake.

## Statement decisions required

An approved source decision must freeze all of the following before Lean elaboration:

- the PDE or hyperbolic system, coefficients, spatial dimension, domain, time interval, initial and
  boundary data, and solution/regularity class;
- continuous and discrete spaces, grid geometry and index sets, time and spatial mesh parameters,
  refinement sequence, and whether their ratio is fixed or bounded;
- the exact difference/finite-volume operator, stencil, time recurrence, startup values, boundary
  treatment, and discrete-solution predicate;
- consistency, solvability, stability, convergence, or error hypotheses and their precise notions;
- continuous and numerical domains of dependence and the exact containment/limit relationship;
- norm or topology, uniformity, constants, rates, horizons, and ordered dependency of quantifiers;
- whether the conclusion is necessity, sufficiency, equivalence, nonconvergence, convergence, or a
  conjunction of separately sourced results; and
- the arithmetic model, allowed computation, universes, typeclasses, logical profiles, alternate
  encodings, and every excluded boundary case.

## Degenerate cases to resolve

- zero, negative, unequal, or vanishing mesh widths and undefined or unbounded mesh ratios;
- zero characteristic speed, changing-sign or discontinuous coefficients, characteristic
  boundaries, and degenerate hyperbolicity;
- empty, singleton, finite, periodic, bounded, and unbounded grids and terminal-time truncation;
- nonsmooth or incompatible initial/boundary data and nonexistent or nonunique PDE solutions;
- singular recurrences, missing startup rows, unstable parameter regimes, and finite versus
  infinite time horizons;
- equality at the CFL boundary versus strict inequality, constant/exact solutions, and schemes with
  wider or implicit stencils; and
- exact real/rational arithmetic versus floating-point roundoff and solver tolerance.

No degenerate case is excluded at intake because no proposition has been selected.

## Neighbor and substitution boundary

- `THM-M-1465` owns the broader finite-difference method family; it cannot supply this theorem.
- `THM-M-1472` owns Lax equivalence; stability plus consistency plus convergence may be related but
  is not the CFL domain-of-dependence condition.
- `THM-M-1474` owns von Neumann stability analysis; a Fourier-mode bound cannot silently replace
  CFL necessity or a source-specific convergence statement.
- Scalar advection, the wave equation, or one named numerical scheme cannot be selected merely
  because it yields a familiar Courant-number inequality.
- A structure or hypothesis storing the desired stability, convergence, domain containment, or
  conclusion is circular and receives no theorem credit.
- A finite numerical experiment, plot, residual, floating-point simulation, unchecked certificate,
  catalog label, or discovery probe is not proof evidence.

## Lean and trust boundary

The intended backend is pinned Lean 4 plus mathlib. The probe checks `fwdDiff`, the Newton
forward-difference identities, and abstract coercive-form bounds. These are adjacent substrate only:
they define no hyperbolic evolution, stencil, domains of dependence, or CFL theorem. Exact imports,
formal target, normalized expression, environment fingerprint, transports, mutation fixtures,
terminal proof body, transitive axioms, and computation policy remain open until source selection.
