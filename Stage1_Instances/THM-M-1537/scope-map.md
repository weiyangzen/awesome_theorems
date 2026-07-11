# Scope map

## Included claim

- The Bekenstein-Hawking entropy-area law for a black-hole event horizon.
- Horizon area `A`, entropy `S_BH`, and the constants `k_B`, `c`, `G`, and `hbar`.
- The Planck-unit form `S_BH = A / 4` and its dimensionful SI restatement, once a source fixes conventions.
- Positivity and dimensional hypotheses required to interpret the physical quantities.

## Decisions deferred to the statement phase

Primary-source inspection must fix the spacetime/black-hole class (for example stationary or
Schwarzschild), semiclassical assumptions, horizon notion and area measure, unit system, whether
the result is a derived equality or a thermodynamic identification, and the treatment of zero area
or degenerate horizons. It must also decide whether Lean represents physical dimensions or states a
dimensionless algebraic consequence of an explicitly axiomatized physical model.

## Explicit exclusions

- The generalized second law, Hawking temperature, or holographic bound as substitutes.
- A bare definition `S_BH := A / 4` presented as a derivation of the physical law.
- Entanglement entropy or higher-curvature corrections in place of the Einstein-gravity area law.
- Experimental/observational assertions that have no axiomatized mathematical semantics.
- Algebraic cancellation alone as proof of the source-level physical premises.

