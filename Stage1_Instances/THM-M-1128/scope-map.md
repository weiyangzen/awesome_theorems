# Scope map

## Preserved source scope

- Subject: a solution formula for a three-dimensional wave equation.
- Attribution and date: Gustav Kirchhoff, 1883, as secondary repository metadata only.
- Mathematical family: propagation of wave initial data in three spatial dimensions.
- Claimed status: the repository label `已验证` is untrusted intake metadata, not evidence.

## Decisions required before statement freeze

The statement phase must identify a primary source and freeze: homogeneous versus forced equation;
normalization `u_tt = c^2 Delta u` and the sign convention for `Delta`; `c > 0`; the time interval;
the domain (`R^3` or another space); scalar field; initial displacement and velocity; their
regularity and support; classical, weak, or distributional solution; uniqueness class; sphere
measure normalization; surface-integral versus spherical-mean presentation; and whether the target
asserts the formula, PDE satisfaction, initial conditions, uniqueness, or all of these. It must also
handle `t = 0`, zero wave speed exclusion, zero data, negative time if included, and differentiation
at the initial-time boundary.

## Candidate mathematical shape, not adopted

For the homogeneous Cauchy problem on `R^3`, a common normalized candidate uses spherical means
`M_r h(x)` and has the shape
`u(x,t) = d/dt (t * M_(c*t) f(x)) + t * M_(c*t) g(x)` (with normalization conventions affecting
the second term). This line is a discovery aid only. The sparse source record does not authorize it
as the canonical target.

## Explicit exclusions

- Kirchhoff's diffraction formula, Kirchhoff's circuit laws, and Kirchhoff's matrix-tree theorem.
- A one- or two-dimensional wave formula, Huygens principle alone, or a radial special case.
- A convenient spherical-average identity substituted without source fidelity.
- Any abstract structure whose fields assume the desired PDE or representation result.
