# Scope map

## Preserved source scope

- Object: a Green function serving as an integral kernel.
- Setting: an unspecified boundary-value problem.
- Attribution and date: George Green, 1828, as repository metadata only.
- Intended role: represent or invert the boundary-value problem, with the precise identity open.

This is all the repository source fixes. A Green function can mean a fundamental solution adjusted
to boundary data, an inverse/resolvent kernel, a heat kernel integral, or a distributional object;
these are not interchangeable statements.

## Decisions required before statement freeze

The statement phase must identify a primary source and freeze the operator and sign convention,
ambient scalar field, dimension, domain and boundary regularity, boundary condition, function or
distribution spaces, source term, solution notion, kernel normalization, existence/uniqueness
hypotheses, singularity and integrability conditions, and the exact representation identity. It
must state whether the claim is construction, existence, uniqueness, inverse-kernel behavior, or
solution representation, and cover zero data, empty/degenerate domains, and diagonal singularities
where meaningful.

## Explicit exclusions

- Green's identities, symmetry, positivity, eigenfunction expansions, or fundamental solutions as
  substitutes for the unidentified root claim.
- A theorem for one convenient ODE/PDE selected only because mathlib exposes an API.
- The adjacent THM-M-1164 symmetry claim and THM-M-1165 expansion claim.
- The untrusted `已验证` metadata label as human or kernel evidence.
