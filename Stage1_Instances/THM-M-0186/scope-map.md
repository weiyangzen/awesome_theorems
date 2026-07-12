# Scope map

## Included claim

- A smooth immersion `f : T^2 -> R^3` of a compact, boundaryless two-torus.
- The induced area measure and principal curvatures `k1`, `k2`.
- Scalar mean curvature normalized as `H = (k1 + k2) / 2`.
- Willmore energy `W(f) = integral H^2 dA` and the lower bound `W(f) >= 2*pi^2`.

This normalization is material: using the trace `k1 + k2` as mean curvature multiplies the energy
by four. The statement phase must not silently transfer the same constant to that convention.

## Decisions reserved for the statement phase

The formal model must fix a concrete smooth torus, the representation of an immersion, induced
metric and area measure, scalar versus vector mean curvature, integrability, and the ordered Lean
binders. It must also check the bridge between the Euclidean formulation and the conformally
equivalent spherical formulation used by the modern proof.

The equality characterization (stereographic/conformal images of the Clifford torus) is not part of
the Stage0 phrase "lower bound" and is not included in the canonical root. It may later be recorded
as a separate obligation only after a pinpoint source audit.

## Explicit exclusions

- The Willmore inequality `W >= 4*pi` for arbitrary closed surfaces as a substitute.
- Only embedded tori unless a checked reduction covers non-embedded immersions.
- Only minimal embedded surfaces in the round three-sphere.
- A genus-at-least-one area theorem in `S^3` without a checked conformal bridge.
- A finite-dimensional surrogate, sampled curvature, or numerical approximation.
- An abstract structure or hypothesis that contains `W >= 2*pi^2` as a field.

## Downstream dependency surface

The expected architecture contains differential geometry of immersed surfaces, conformal
invariance/stereographic projection, the non-embedded reduction, and the Marques-Neves min-max
theorem. These are discovery headings only; the obligation phase must freeze semantic nodes before
assigning any proof credit.
