# Scope map

## Included theorem family

- Chordal Schramm-Loewner evolution in a simply connected planar domain, transported to a standard
  domain such as the upper half-plane, with source and target boundary points.
- A Virasoro highest-weight representation associated with the SLE parameter `kappa`, including
  the source's conventions for central charge `c(kappa)` and conformal weight `h(kappa)`.
- A level-two degeneracy or null-vector identity, commonly expressed using `L_{-1}` and `L_{-2}`
  after fixing Virasoro and Loewner normalizations.
- The stochastic consequence of that identity, such as a stopped local martingale or a statement
  about CFT correlation/partition functions evaluated along the Loewner flow.

## Decisions required at statement freeze

The statement phase must select and inspect one exact primary result. It must freeze: chordal versus
radial or dipolar SLE; the domain and marked boundary points; half-plane-capacity and Brownian-motion
normalizations; the permitted range and boundary behavior of `kappa`; the precise Virasoro algebra,
module, highest-weight vector, and operator conventions; the formulas and denominator side
conditions for `c` and `h`; the ordering and coefficients of the level-two null vector; whether the
claim is algebraic degeneracy, a local-martingale construction, conformal covariance, restriction,
or a converse; the observable and filtration; collision/explosion stopping times; integrability
needed to upgrade a local martingale; and the order of all domain, time, and expectation quantifiers.

These choices change the proposition and cannot be hidden as implementation details. In particular,
an informal path-integral CFT expression is not automatically a measure-theoretic Lean object.

## Explicit exclusions

- The definition or conformal invariance of SLE alone, or a deterministic Loewner-chain theorem.
- A formula for central charge and conformal weight without the representation/null-vector and
  stochastic consequence required by the selected source result.
- An SLE duality, restriction, locality, crossing-probability, or critical-exponent theorem merely
  because it uses conformal ideas.
- Radial, multiple, or `SLE(kappa,rho)` results substituted for a selected chordal theorem.
- A structure that takes the null-vector identity, martingale property, or desired correlation
  equation as a field or hypothesis.
- A formal power-series calculation, numerical simulation, physics heuristic, or the repository
  metadata value `已验证` as source or kernel evidence.

No canonical Lean expression is frozen at intake. A later target must expose concrete analytic and
algebraic objects and must distinguish a stopped local martingale from a true martingale.
