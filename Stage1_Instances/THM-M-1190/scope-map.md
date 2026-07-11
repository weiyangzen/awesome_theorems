# Scope map

## Preserved source scope

- Subject: an unspecified heat or more general parabolic equation.
- Claimed result: an unspecified `L^p` estimate or `L^p` theory.
- Historical scope: twentieth-century work attributed only to multiple mathematicians.
- Formal scope: Lean 4 is the intended system, but no canonical proposition is frozen.

## Decisions required before statement freeze

The statement phase must identify a primary theorem and freeze the operator and coefficients,
spatial dimension, time interval, domain and boundary/initial conditions, forcing and initial data,
weak/mild/strong solution notion, measure and Bochner spaces, exponent range and endpoints, the
quantity estimated, constant dependencies, and local/global or homogeneous/inhomogeneous form.
It must explicitly handle zero data, infinite time, `p = 1` and `p = infinity` when relevant, and
any compatibility or smoothness hypotheses.

## Explicit exclusions

- Substituting heat-semigroup `L^p` contractivity for maximal parabolic regularity, or conversely.
- Substituting an `L^p-L^q` smoothing/decay estimate, a Gaussian heat-kernel bound, an energy
  estimate, or an elliptic Calderon-Zygmund theorem without primary-source identification.
- Treating the title's "heat equation" and the source phrase's broader "parabolic equations" as
  equivalent without resolving their scope difference.
- Treating the metadata label `已验证` as human-source or kernel evidence.

