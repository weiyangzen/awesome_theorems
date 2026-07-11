# THM-M-1312 rev-5.6 intake

This directory is the rev-5.6 `planned` dossier for the Choquet-Bruhat-Geroch
theorem. The root is the maximal globally hyperbolic development theorem for
vacuum Einstein initial data, including uniqueness up to an
initial-data-preserving isometry. It is not merely a generic statement of
"global existence."

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Initial data | Smooth 3-manifold, Riemannian metric, second fundamental form, vacuum constraints | Exact regularity, connectedness, orientation, and Lean structures remain open |
| Development | Time-oriented Lorentzian spacetime solving the vacuum Einstein equations and inducing the data on a Cauchy surface | No Lorentzian/PDE API is credited yet |
| Local branch | Gauge reduction, local existence, uniqueness, constraint propagation | Architecture only; no closure claimed |
| Global branch | Common extensions/gluing and a maximality construction | Architecture only; set-theoretic and causal details remain open |
| Root conclusion | Existence of a maximal globally hyperbolic development and uniqueness up to data-preserving isometry | Exact categorical formulation and checked equivalences belong to the statement phase |
| Exclusions | Matter-coupled systems, arbitrary nonconstraint data, nonglobally-hyperbolic extensions, geodesic completeness | These are not silently broadened into the root |

The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_168.lean`
is recorded only as a candidate interface. Its prior checks do not establish a
rev-5.6 normalized expression, source fidelity, or terminal proof.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first
failed theorem gate is the exact Lean statement gate: expression and
environment fingerprints, regularity choices, checked transports, and
mutation tests are absent. The theorem is not complete.

## Validation

The exact commands and results for this dossier are recorded in
`validation.md`. They validate target membership, repository-standard
consistency, JSON syntax, and local references only.
