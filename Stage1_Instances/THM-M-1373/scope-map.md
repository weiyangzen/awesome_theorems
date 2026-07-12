# Scope map

## Preserved topic family

The intake preserves only the catalog's Hamiltonian-system topic: a mathematical framework for
classical mechanics attributed to Hamilton. A later statement phase may select an exact root only
from an immutable, independently reviewed source passage. Candidate components, none credited as
the theorem at intake, include:

- canonical phase coordinates `(q, p)`, a Hamiltonian `H`, and Hamilton's coordinate equations;
- a coordinate-free symplectic manifold, Hamiltonian vector field, and local or global flow;
- equivalence with Euler-Lagrange dynamics under a regular Legendre transform;
- conservation of an autonomous Hamiltonian along its trajectories;
- preservation of a symplectic form or phase-space volume by Hamiltonian flow; and
- integrability, action-angle coordinates, recurrence, or stability under additional hypotheses.

## Decisions required at statement freeze

1. Preserve and hash one lawful complete source edition, select a numbered theorem or precisely
   delimited result, map incorporated definitions and proof boundaries, review corrections and
   errata, and obtain independent source approval.
2. Decide whether the root is a definition/equation characterization, an equivalence theorem, a
   conservation theorem, a flow-preservation theorem, or another exact result. A framework title
   cannot silently combine these claims.
3. Fix the phase space: `R^(2n)`, a cotangent bundle, a finite-dimensional symplectic manifold, or
   another source-selected carrier; also fix scalar field, dimension, universes, and coordinates.
4. Fix the Hamiltonian's time dependence and regularity, the derivative/gradient and symplectic-
   form conventions, sign convention for the Hamiltonian vector field, and any Legendre transform.
5. Fix the trajectory or flow model, time domain, local/global existence and uniqueness premises,
   completeness, initial conditions, and solution equality convention.
6. Freeze the exact conclusion, all ordered binders and typeclass assumptions, alternate encoding
   relations, logical principles, and every boundary case.

## Degenerate and boundary cases

Source review must explicitly dispose of zero-dimensional or empty coordinate types; degenerate or
nonclosed two-forms; singular Legendre transforms; constant Hamiltonians; stationary trajectories;
time-dependent Hamiltonians; empty, singleton, disconnected, or unbounded time domains; local
solutions leaving the chart; incomplete vector fields; nonsmooth Hamiltonians; constrained or
singular systems; and infinite-dimensional phase spaces. Conservation and flow-preservation
claims must state whether they are pointwise, local-in-time, global, almost-everywhere, or
measure-theoretic.

## Neighbor and substitution exclusions

- `THM-M-1516` Hamiltonian mechanics has nearly synonymous wording and a legacy discovery artifact,
  but there is no accepted alias, deduplication, or root-ownership decision. Its evidence cannot be
  inherited.
- `THM-P-0756` separately states Hamilton's coordinate equations; those equations cannot be chosen
  as this theorem merely because they are familiar.
- `THM-M-1375` and `THM-M-1520` own Liouville volume-preservation families; `THM-M-1374` owns
  Noether's theorem; `THM-M-1547` owns the completely integrable/action-angle family.
- KAM, Nekhoroshev, recurrence, Hamilton-Jacobi, least-action, canonical-transformation, and Poisson-
  bracket targets have additional premises or different conclusions.
- A structure that stores desired symplectic, conservation, equivalence, or integrability outputs
  as proposition fields is an interface, not a proof.
- Canonical matrix identities, generic ODE/flow APIs, simulations, numerical trajectories, and the
  catalog's `verified` label provide no source-statement or proof credit.

## Formal boundary

Pinned mathlib exposes integral curves, global topological flows, the canonical matrix `Matrix.J`,
and a linear symplectic group. The probe authenticates only those adjacent interfaces. It does not
define the source-selected Hamiltonian, symplectic manifold, Hamiltonian vector field, Legendre
bridge, conservation law, or flow theorem. No canonical Lean target, expression fingerprint,
checked transport, mutation suite, or proof body is claimed at intake.
