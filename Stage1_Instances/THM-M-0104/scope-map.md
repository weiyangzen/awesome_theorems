# Scope Map

| Surface | Planned meaning | Intake status |
|---|---|---|
| Ambient geometry | Projective plane over an algebraically closed field | selected, not source-pinned |
| Curves | Curves represented by nonzero homogeneous plane equations, or an exact equivalent Lean model | representation unresolved |
| Properness | No common irreducible component | required |
| Degree | Degree of each projective plane curve | convention unresolved |
| Local datum | Intersection multiplicity at each projective intersection point | definition unresolved |
| Root conclusion | Sum of multiplicities equals the product of degrees | planned canonical claim |
| Requested gloss | Distinct intersection points are at most the product of degrees | planned corollary |
| Boundary | Points at infinity are included | required by projective scope |
| Exclusion | Shared components and zero-polynomial pseudo-curves | explicit |

## Not silently included

This target does not currently cover arbitrary-dimensional varieties, higher-dimensional
intersection theory, non-algebraically-closed base fields, an affine-only count that
discards points at infinity, or a count without multiplicity asserted as an equality.
Any move to one of those statements requires an explicit scope revision rather than a
substitution made to obtain an easier Lean theorem.

## Open statement tasks

1. Pin a primary-source edition and pinpoint theorem statement.
2. Decide whether the formal root uses homogeneous polynomials, projective schemes, or another definitionally controlled model.
3. Freeze ordered binders, universes, typeclass assumptions, degree and multiplicity definitions, and all degeneracies.
4. Elaborate the exact expression with minimal pinned imports and record its normalized hash and environment fingerprint.
5. Check the implication from the multiplicity equality to the repository's distinct-point upper-bound gloss.
