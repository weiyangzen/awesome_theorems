# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1344`, the label `李雅普诺夫间接法` (Lyapunov's indirect
method), the gloss `线性化稳定性` (stability by linearization), Aleksandr Lyapunov, 1892, high
importance, and untrusted status `已验证`. Intake preserves the nonlinear-dynamics theorem family
that transfers stability or instability information from a system's linearization at an
equilibrium. It does not turn the gloss into a stronger proposition or its status into evidence.

## Proposition-changing decisions

An approved statement run must freeze all of the following from an immutable source:

- whether the system is a finite-dimensional autonomous ODE, a nonautonomous equation, a discrete
  dynamical system, or an evolution equation/semigroup on a Banach space;
- the scalar field, finite-dimensional coordinate space or Banach space, open state domain, norm,
  time domain, and local, maximal, or global solution model;
- the vector field and equilibrium, whether the equilibrium is zero or arbitrary, and any coordinate
  translation used to identify the two encodings;
- `C^1`, Frechet differentiability, local Lipschitz, well-posedness, or semigroup differentiability
  assumptions, including the neighborhood on which they hold;
- whether the linearization is a Jacobian matrix, a continuous linear endomorphism, a generator, or
  the derivative of a time map or solution semigroup;
- whether the hypothesis is that every eigenvalue has negative real part, the entire spectrum lies
  in a left half-plane, or the linearized semigroup obeys an exponential norm bound;
- whether the conclusion is Lyapunov, asymptotic, local exponential, or another source-defined
  stability notion, with its exact constants and forward-time quantifier order;
- whether the root includes only the stable direction, only the instability direction, or both;
- the positive-real-part condition used by the instability direction and whether continuous,
  residual, or essential spectrum is material; and
- every universe, ordered binder, typeclass, coercion, neighborhood, radius, time-bound, and
  degenerate or boundary case.

These choices produce inequivalent propositions. They are a resolution ledger, not a canonical
statement.

## Candidate branches not credited

1. Finite-dimensional stable branch: for `z' = F z`, a differentiable vector field with equilibrium
   `z_e`, all eigenvalues of `DF(z_e)` having negative real part imply local exponential stability.
2. Finite-dimensional unstable branch: an eigenvalue of `DF(z_e)` with positive real part implies
   instability of the equilibrium.
3. Banach-space branch: exponential stability or instability of a linearized semigroup transfers to
   the nonlinear semigroup under source-specific well-posedness and Frechet differentiability.
4. A weaker textbook formulation that concludes asymptotic stability rather than recording an
   exponential estimate.

None of these branches is selected, asserted, conjoined, or credited at intake.

## Explicit exclusions and neighbor boundaries

- `THM-M-1343`, Lyapunov's direct method, requires a Lyapunov function and is not a substitute for
  transfer from a linearization.
- `THM-M-1345`, Hartman-Grobman, concerns local topological conjugacy near a hyperbolic equilibrium;
  it is neither definitionally nor automatically the exact indirect-method claim.
- `THM-M-1346`, the stable manifold theorem, supplies stable/unstable manifolds under hyperbolicity,
  not the same root statement.
- `THM-M-1355`, stability of linear systems, is prospective input about the linearized system and
  cannot replace the nonlinear transfer theorem.
- Local existence/uniqueness, an ODE solution predicate, a derivative API, or a spectrum/eigenvalue
  lemma alone is supporting substrate, not the indirect method.
- A structure that assumes nonlinear stability or instability as a field, or the catalog label
  `已验证`, supplies no proof credit.

## Boundary cases

The source selection must decide the zero-dimensional phase space, zero vector field, a constant or
already-linear vector field, a non-isolated equilibrium, multiple or nonunique solutions, an
equilibrium at the boundary of the state domain, an empty spectrum in an infinite-dimensional
encoding, and spectrum on the imaginary axis. In particular, zero real parts are not silently
classified: standard examples show that a critical linearization alone may give no nonlinear
stability conclusion.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, useful substrate includes `IsIntegralCurve`,
`IsPicardLindelof`, `ODE_solution_unique_univ`, `HasFDerivAt`, `fderiv`, `spectrum`, and
`Module.End.hasEigenvalue_iff_mem_spectrum`. The bounded intake search located no Lyapunov indirect
method, nonlinear ODE exponential-stability, or linearization-stability theorem. The probe and
search are discovery inputs only; exact source transport, a complete formal-candidate inventory,
and proof-body provenance belong to later phases.
