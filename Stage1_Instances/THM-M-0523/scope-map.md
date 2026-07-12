# Scope map

## Candidate named-theorem boundary

- A modular curve associated with a source-specified congruence subgroup.
- Its compactification and cusps, with the field of definition made explicit.
- The Jacobian or degree-zero Picard group of that curve.
- The divisor class of a difference of two cusps.
- The conclusion that this class has finite additive order.

This is the standard mathematical topic attached to the name "Manin-Drinfeld theorem". It is a
candidate boundary, not yet the canonical claim for this repository ID.

## Conflict to resolve at statement freeze

The repository's only prose statement says "properties of Heegner points on elliptic curves".
Heegner points are noncuspidal special points used in results such as Gross-Zagier and Kolyvagin;
their arithmetic properties are not the cusp-difference torsion theorem. The statement phase must
inspect an immutable primary source and either correct the source mapping to the named theorem or
identify the exact Heegner-point proposition actually intended. It may not merge the two.

For the cusp-divisor reading it must additionally fix:

1. the precise class of congruence subgroups and modular-curve construction;
2. the base field and whether cusps/divisors are geometric or rational;
3. Jacobian versus `Pic^0` as the target, plus any checked equivalence;
4. ordered cusp binders, the equal-cusp boundary, and the definition of torsion;
5. whether `X_0(N)` and `X_1(N)` are specializations or the root domain.

## Explicit exclusions

- A theorem about heights, ranks, traces, or non-torsion of Heegner points as a substitute.
- Gross-Zagier or Kolyvagin results merely because they occur near this item in the inventory.
- Torsion of an abstract map supplied as input; that assumes away the geometric construction.
- The duplicate `THM-M-0124` or its legacy statement shape as accepted evidence for this ID.
- Finiteness of cusp orbits as a substitute for torsion of cusp divisor classes.
- The source label `已验证` as human-proof or machine-proof evidence.

No canonical Lean target is frozen at intake because the source statement conflict remains open.
