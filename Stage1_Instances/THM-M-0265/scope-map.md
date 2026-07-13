# Scope map

## Received claim

`Docs/researches/math_theorems.md:1908-1913` records the title
`魏尔斯特拉斯逼近定理`, Karl Weierstrass, 1885, and the gloss
`连续函数可用多项式一致逼近` ("continuous functions can be uniformly approximated by
polynomials"). It gives no bibliography, definitions, assumptions, formula, proof boundary, or
formal declaration. The Stage0 projection at `Docs/Stage0_Blueprint.md:7333-7358` repeats the gloss
and explicitly leaves precise definitions and premises, equivalent forms, axioms, machine status,
and artifact links open.

The intake preserves that literal boundary. It does not silently insert the standard real
closed-interval formulation.

## Proposition-changing choices

The statement phase must source and fix:

- a closed interval `[a,b]`, `[0,1]`, an arbitrary compact subset of the reals, or another compact
  space;
- real- or complex-valued functions and real, complex, or another coefficient field;
- a bundled continuous map on a subtype versus a total function continuous on a set;
- density or closure equality, membership in a closure, existence for every positive epsilon, or
  existence of a uniformly convergent polynomial sequence;
- the exact uniform topology, supremum norm, or pointwise quantified error expression;
- strict versus non-strict error and the placement of the positive-epsilon hypothesis;
- the polynomial carrier and evaluation/coercion convention; and
- whether the theorem includes only existence or also a particular approximation construction.

These variants are closely related only after their side conditions and transports are proved.
The theorem name and normalized prose do not establish their identity.

## Pinned Lean candidate boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Topology.ContinuousMap.Weierstrass` exposes:

- `polynomialFunctions_closure_eq_top'` for the unit interval;
- `polynomialFunctions_closure_eq_top (a b : ℝ)` for every real closed interval;
- `continuousMap_mem_polynomialFunctions_closure` for bundled continuous maps;
- `exists_polynomial_near_continuousMap` in the supremum norm; and
- `exists_polynomial_near_of_continuousOn` as an unbundled epsilon statement.

The general interval proof explicitly handles `b <= a` using subsingleton intervals. It is built
from the Bernstein approximation result `bernsteinApproximation_uniform`. These are substantive,
direct exact-topic interfaces and justify provisional `M3`, not M0: the source has not selected one
of them as the root, no expression fingerprint or checked transport exists, and proof-body,
provenance, trust, and composition audits are downstream work.

`Mathlib.Topology.ContinuousMap.StoneWeierstrass` contains a broader compact-set polynomial-density
result. It is not selected here because `THM-M-0266` separately owns Stone-Weierstrass and the
catalog has not authorized that broadening.

## Boundary cases to resolve

- `a < b`, `a = b`, and `b < a`, including the empty interval convention.
- Empty or singleton domains and constant or zero functions.
- Positive, zero, and negative approximation tolerances.
- Degree zero and whether a degree bound or approximation sequence is part of the conclusion.
- Real versus complex coefficients and codomain.
- Bundled maps whose domain is the interval subtype versus total functions restricted to it.
- Uniform norm closure versus the pointwise absolute-value inequality and any endpoint convention.

No boundary case is excluded before an exact proposition is independently sourced and selected.

## Explicit exclusions

- Stone-Weierstrass or density of a separating subalgebra in place of classical interval
  polynomial approximation.
- Bernstein approximation alone in place of the general interval conclusion.
- Taylor approximation, analytic-function approximation, Runge, Mergelyan, or trigonometric
  approximation.
- Pointwise convergence, approximation at finitely many points, or a fixed function/interval.
- A premise, structure field, axiom, oracle, or unchecked certificate that stores the desired
  approximating polynomial.
- The catalog's untrusted `已验证` label, theorem name, or API probe treated as source identity or
  proof credit.

## Neighbor boundary

`THM-M-0266` is the separately cataloged Stone-Weierstrass theorem, with gloss "density of the
algebra of continuous functions." Its general subalgebra-separation scope and proof credit must not
be imported into this target without an explicit, source-reviewed relationship.
