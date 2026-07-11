# Scope map

| Surface | Frozen intake scope | Boundary |
|---|---|---|
| Curves | Elliptic curves defined over `Q` | All singular cubics and curves over other fields are excluded |
| Group | The full group `E(Q)_tors` of rational torsion points, up to abstract group isomorphism | No choice of Weierstrass model, generators, or embedding is part of the conclusion |
| Cyclic cases | `Z/nZ`, `1 <= n <= 10` or `n = 12` | `n = 1` denotes the trivial group |
| Noncyclic cases | `Z/2Z x Z/2mZ`, `1 <= m <= 4` | Equivalently the second factor has order `2,4,6,8`; this equivalence needs a checked transport |
| Logical direction | Every rational elliptic-curve torsion group is on the list | Realizability of every listed group is not included in this root |
| Lean candidate | `AwesomeTheorems.Stage1.S1_M_088.StatementShape` | Historical discovery input, not yet accepted as canonical and not proved |
| Foundations | Lean 4 kernel and pinned mathlib, with any classical principles disclosed | Exact imports, toolchain fingerprint, transitive axioms, and TCB remain open |

Degenerate and encoding-sensitive points for the statement phase are: nonsingularity through
`E.IsElliptic`, the meaning of `E(Q)` for the chosen Weierstrass model, finiteness implicit in the
classification, `ZMod 1` as the trivial group, additive rather than multiplicative equivalence,
and the reparameterization `n = 2*m` in the noncyclic cases.
