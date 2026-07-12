# Scope map

## Included claim

- Domain: elliptic curves over the rational field `Q`.
- Root assertion: every such curve is modular.
- Meaning of modular: any of the six equivalent conditions in the primary paper, with the exact
  formal encoding and checked transports to be chosen at statement freeze.
- Likely formal ingredients: elliptic curves, conductors, modular curves or weight-two eigenforms,
  L-series, Tate modules, Galois representations, and the equivalences connecting these views.

## Boundary cases to freeze

- `E` must be nonsingular; a bare or singular Weierstrass equation is outside the domain.
- The base field is exactly `Q`, not an arbitrary number field.
- The level in the strongest classical formulation is the conductor `N(E)` and the weight is `2`.
- A formal choice between isomorphism classes and concrete Weierstrass models must be accompanied
  by checked invariance/transport, rather than silently changing the quantifier.
- The theorem is unconditional. Semistability, irreducibility of a selected residual
  representation, or local reduction assumptions may occur in proof branches but not at the root.

## Explicit exclusions

- Theorem B of the same paper concerning irreducible mod-5 representations.
- Wiles's earlier semistable-elliptic-curve modularity theorem as a substitute for all curves.
- Serre modularity, modularity lifting, potential modularity, or modularity over other fields.
- Higher-dimensional abelian varieties and singular cubic curves.
- A new uninterpreted `Modular` predicate, or an assumed modularity field followed by projection.
- The repository label `已验证` as human-source or kernel evidence.

The human scope is frozen at intake. The representation of elliptic curves and modularity in Lean,
including all equivalence transports, remains owned by the statement phase.
