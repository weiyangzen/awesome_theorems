# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1372`, the label `Nekhoroshev estimate`, Nikolai
Nekhoroshev, 1977, and the gloss `exponential stability of nearly integrable systems`. Intake
preserves the nearly integrable dynamical-systems subject and the intended exponential-time
stability theme. It does not silently turn the gloss into a quantified theorem.

## Proposition-changing decisions

An approved statement transition must freeze all of the following:

- the original steep analytic theorem, a quasi-convex specialization, a Gevrey extension, a
  finitely differentiable analogue, an elliptic-equilibrium result, a time-dependent result, a
  symplectic-map result, or another precisely cited variant;
- finite-dimensional action-angle coordinates, the number of actions and auxiliary canonical
  variables, real and complex domains, torus conventions, norms, universes, and scalar fields;
- a Hamiltonian `H = H0 + H1` or `H = h + f`, its canonical equations, and the exact meaning of
  integrable and nearly integrable;
- analytic widths or other regularity, reality and periodicity conditions, derivative bounds,
  Hessian bounds, and complete domain-margin and trajectory-existence hypotheses;
- steepness coefficients and indices, strict quasi-convexity constants, or another exact
  nondegeneracy contract;
- the perturbation size (`sup |grad H1|`, `sup |H1|`, an analytic/Gevrey norm, or a `C^k` norm),
  its strict or non-strict smallness assumptions, and all constant dependencies;
- every ordered binder, initial-condition condition, forward versus two-sided time convention,
  confinement norm and radius, exponential-time formula, exponent, prefactor, and conclusion; and
- exceptional cases such as zero perturbation, low dimension, boundary escape, incomplete
  trajectories, loss of steepness, critical regularity, and degenerate Hamiltonians.

These choices define materially different propositions. They are a resolution ledger, not a
canonical claim.

## Candidate roots not credited

- Nekhoroshev 1977, Theorem 4.4: the analytic steep-Hamiltonian estimate with parameters and
  auxiliary canonical variables, together with the definitions and Part II proof boundary.
- The paper's introductory Theorem 1.4: explicitly approximate and different in details, so it
  cannot replace Theorem 4.4 merely because its wording is shorter.
- The analytic strictly quasi-convex action-angle estimates of Poeschel and later refinements,
  including differing exponents and radius/time tradeoffs.
- Gevrey or `C^infinity` extensions, whose regularity changes the exponents.
- The finitely differentiable quasi-convex result, which gives polynomial rather than exponential
  time and therefore cannot satisfy the literal exponential gloss.
- Results near elliptic equilibria, for time-dependent perturbations, or for symplectic maps.

No candidate is selected, conjoined, asserted, or credited at intake.

## Neighbor and duplicate boundaries

- `THM-M-1369`, `THM-M-1370`, and `THM-M-1371` separately name KAM theory, the
  Kolmogorov-Arnold theorem, and Moser's twist theorem. Perpetual stability on invariant tori cannot
  replace finite-time stability for all allowed initial conditions.
- `THM-M-1373` owns the broad Hamiltonian-systems topic. Generic Hamiltonian definitions or flow
  APIs are substrate, not the Nekhoroshev estimate.
- `THM-P-0775` is a non-covered physics-catalog semantic duplicate with the stronger gloss that
  actions remain stable for exponentially long times. It is absent from the rev-5.6 target manifest
  and has no accepted alias or ownership decision, so its wording and evidence do not transfer.
- Arnold diffusion bounds, numerical orbit integrations, KAM measure estimates, normal-form
  algorithms, or an assumed stability field cannot substitute for the selected theorem.

## Boundary cases

The statement phase must decide at least zero perturbation versus the source's strict positive
perturbation size; one or two degrees of freedom and the source's dimension bounds; empty or
zero-dimensional domains; initial data at the domain margin; trajectories leaving the auxiliary
domain before the advertised time; finite maximal existence intervals; vanishing gradient of the
integrable Hamiltonian; failure of steepness or quasi-convexity; nonanalytic perturbations; the sign
and positivity of all exponents and constants; forward-only versus absolute-time estimates; and
strict versus weak confinement inequalities.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only probe checks generic
`AnalyticAt`, `IsIntegralCurve`, `Flow`, `Real.rpow`, and `Real.exp` interfaces. Pinned mathlib has
linear-algebraic symplectic-group material but no located source-shaped Hamiltonian action-angle,
Poisson/symplectic-flow, steepness, perturbative normal-form, or Nekhoroshev theorem stack. A
bounded exact-topic search found no `Nekhoroshev` declaration in pinned mathlib or repo-local Lean.
This is not the downstream exhaustive anchor audit or an external absence claim.
