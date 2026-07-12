# Scope map

## Included claim

- The open unit disc `D = {z in C | |z| < 1}`.
- A nonempty finite family `f_i` in `H^infinity(D)`, meaning analytic and bounded on `D`.
- A uniform corona condition `sum_i |f_i(z)| >= delta > 0` for all `z` in `D`.
- Existence of `g_i` in `H^infinity(D)` satisfying `sum_i f_i(z) g_i(z) = 1` on `D`.

This is the classical finite-generator Bezout formulation associated with Carleson's theorem.
`Statement.lean` freezes its exact Lean representation.

## Statement-freeze decisions

The formal statement selects `sum |f_i|`, an explicit positive `delta`, no normalized common upper
bound, and no quantitative conclusion beyond boundedness of each `g_i`. It uses ambient functions
restricted to `Metric.ball (0 : ℂ) 1` and an arbitrary type with `Fintype` and `Nonempty` instances.
The exact primary-source passage must still be inspected and independently reviewed; a mismatch
would invalidate this freeze rather than being silently transported.

The empty family and `delta <= 0` are excluded. Singleton and constant families are admitted. The
boundary circle is excluded. Boundedness means `Bornology.IsBounded` of the image of the open disc.

## Explicit exclusions

- The several-variable corona problem, corona problems for other domains or Banach algebras, and
  operator corona theorems.
- A special case for polynomials, finite Blaschke products, or two generators as a substitute.
- Bezout coefficients assumed as structure fields or supplied as hypotheses.
- Mere pointwise absence of a common zero without the uniform positive lower bound.
- The maximal-ideal-space density formulation without a checked equivalence to the frozen target.
- The repository label `已验证` as human-proof, formal-proof, or release evidence.
