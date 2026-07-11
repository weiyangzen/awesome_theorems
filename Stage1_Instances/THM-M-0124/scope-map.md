# Scope map

## Included root claim

- Object: the compactified modular curve associated to a congruence subgroup, over the conventional arithmetic base to be fixed at the statement phase.
- Boundary: its cusps.
- Input: a divisor of degree zero supported on those cusps.
- Conclusion: its divisor class is torsion in the Jacobian (equivalently in the degree-zero Picard group after a checked identification).
- Pairwise form: for any two cusps `c` and `d`, `[c-d]` is torsion. The statement phase must check the equivalence between this generator form and the all-cuspidal-degree-zero-divisors form.

## Encoding decisions left to the statement node

- Freeze whether the canonical root ranges over congruence subgroups or uses a level-moduli presentation; `X_0(N)` and `X_1(N)` are specializations, not substitutes for the general root.
- Select concrete mathlib or locally defined compactification, cusp, divisor, Picard/Jacobian, degree, and torsion APIs.
- Freeze base field, connectedness/nonemptiness assumptions, universes, ordered binders, minimal imports, toolchain, and environment fingerprint.
- Add checked transports between Jacobian and `Pic^0`, and between pairwise cusp differences and arbitrary degree-zero cuspidal divisors.
- Mutation-test the congruence condition, degree-zero condition, cusp support, target group, and torsion conclusion.

## Explicit exclusions

- Heegner points on elliptic curves, despite the generated legacy metadata gloss.
- The Gross-Zagier formula, Heegner-point non-torsion results, and complex multiplication statements.
- Mere finiteness of the cusp set or cusp orbits.
- A theorem over an abstract user-supplied map that assumes away the modular curve, Jacobian, or Abel-Jacobi construction.
- A result only for `X_0(N)` or `X_1(N)` presented as the general theorem.
- Any legacy declaration in `S1_M_043.lean` as accepted rev-5.6 evidence.
