# Scope map

## Included claim

- The open unit disc `D = {z in C | |z| < 1}`.
- A nonempty finite family `f_i` in `H^infinity(D)`, meaning analytic and bounded on `D`.
- A uniform corona condition `sum_i |f_i(z)| >= delta > 0` for all `z` in `D`.
- Existence of `g_i` in `H^infinity(D)` satisfying `sum_i f_i(z) g_i(z) = 1` on `D`.

This is the classical finite-generator Bezout formulation associated with Carleson's theorem. It is
a human-level scope freeze, not yet an exact Lean statement.

## Decisions required at statement freeze

The selected primary passage must settle whether it uses `sum |f_i|`, `sum |f_i|^2`, or a maximum;
whether the upper bound on the `f_i` is normalized; whether `delta` is explicit; and whether the
conclusion includes a quantitative bound on the `g_i`. The formal encoding must also choose between
functions on the subtype `Complex.UnitDisc` and ambient functions restricted to `Metric.ball 0 1`,
and between a finite index type, `Fin n`, and a list/finset presentation.

Boundary cases requiring explicit decisions are an empty generator family, `delta <= 0`, a singleton
family, constant generators, and behavior at the boundary circle (which is not part of the open
disc). Binder order, coercions, and the definition of boundedness must be frozen with these choices.

## Explicit exclusions

- The several-variable corona problem, corona problems for other domains or Banach algebras, and
  operator corona theorems.
- A special case for polynomials, finite Blaschke products, or two generators as a substitute.
- Bezout coefficients assumed as structure fields or supplied as hypotheses.
- Mere pointwise absence of a common zero without the uniform positive lower bound.
- The maximal-ideal-space density formulation without a checked equivalence to the frozen target.
- The repository label `已验证` as human-proof, formal-proof, or release evidence.

