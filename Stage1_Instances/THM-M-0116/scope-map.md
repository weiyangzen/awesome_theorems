# THM-M-0116 scope map

## Frozen claim

For an algebraically closed field `k` and a smooth projective algebraic surface `X` over `k`,
the Neron-Severi group `NS(X)`, defined as divisors modulo algebraic equivalence, is a finitely
generated abelian group.

This is the narrow surface formulation recorded by `Docs/Stage0_Blueprint.md`. The familiar
stronger formulation for suitable proper varieties is deliberately not substituted for it.

## Semantic boundary

| Component | Included | Excluded or unresolved |
|---|---|---|
| Base | algebraically closed field | general-field descent and geometric `NS` variants |
| Space | smooth, projective, dimension two | singular, nonproper, analytic-only spaces |
| Group | divisors modulo algebraic equivalence | `Pic(X)` itself; numerical equivalence |
| Result | finite generation as an abelian group | rank, torsion bounds, finite presentation data |
| Lean encoding | scheme/variety plus a quotient class group, to be chosen | no guessed declaration or API at intake |

Projectivity supplies properness but both words remain in the frozen claim to preserve the source
record. Smoothness over an algebraically closed field normally implies the regularity needed for
Cartier/Weil divisor comparisons; those comparisons must be explicit checked transports if used.
Empty and disconnected objects, the precise convention for dimension, and whether the intended
historical term "Severi group" is definitionally the modern `NS(X)` are mutation probes owned by
the statement phase, not silently settled here.

## Assurance state

The instance is `planned`, with `H2 / M4 / R4`. No Lean declaration has been elaborated and no
historical artifact or source label receives proof credit. The next phase must select a minimal
pinned import surface, define or locate algebraic equivalence and `NS(X)`, elaborate the exact
type, and test removal/change of every domain and hypothesis.
