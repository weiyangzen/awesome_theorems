# Scope map

## Included root claim

The target is the standard rank-at-most-one consequence of the
Gross-Zagier formula and Kolyvagin's Euler-system argument. For an elliptic
curve `E/Q`, assume the Hasse-Weil L-function has analytic rank at most one.
The conclusion has both components:

1. the Mordell-Weil rank of `E(Q)` equals the analytic rank; and
2. the Tate-Shafarevich group `Sha(E/Q)` is finite.

The statement phase must make the elliptic-curve model, rational points,
finitely generated group rank, L-function normalization, order of vanishing,
and Tate-Shafarevich group native and explicit. It must not encode any of
these conclusions as an assumed proposition field.

## Required branches and transports

- Analytic rank zero: `L(E,1) != 0`, algebraic rank zero, and finite Sha.
- Analytic rank one: a simple zero at `s = 1`, algebraic rank one, and finite
  Sha.
- Gross-Zagier bridge: relate the central derivative to the Neron-Tate height
  of a Heegner point with audited constants and nonvanishing direction.
- Kolyvagin bridge: carry non-torsion of the relevant Heegner point through
  Euler classes and Selmer control to rank and Sha finiteness.
- Generality bridge: account for the precise Heegner hypothesis, auxiliary
  imaginary quadratic field, twisting, modular parametrization, and any use
  of modularity needed to reach every elliptic curve over `Q` in the root.

These are scope requirements, not a frozen obligation registry and not proof
credit.

## Exclusions

- The full Birch and Swinnerton-Dyer leading-coefficient formula.
- Elliptic curves of analytic rank greater than one.
- Elliptic curves over arbitrary number fields.
- Claims that Sha is trivial, or an exact formula for its order.
- The Gross-Zagier height formula by itself.
- Kolyvagin's theorem stated only under a non-torsion Heegner-point hypothesis,
  unless checked bridges derive that hypothesis and transport its conclusion
  to the canonical root.
- Abstract records whose fields simply assume analytic rank, algebraic rank,
  Sha finiteness, or the desired implication.

## Boundary and mutation obligations

The exact statement must reject a singular cubic in place of an elliptic
curve, a changed base field, deletion of the analytic-rank bound, replacement
of equality by only one inequality, omission of Sha finiteness, and a claim of
the full BSD formula. Boundary tests must distinguish analytic ranks zero,
one, and two. Alternate completed and uncompleted L-function normalizations
may receive credit only after a checked equality of their vanishing orders at
the relevant central point.
