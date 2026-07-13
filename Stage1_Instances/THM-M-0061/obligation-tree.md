# THM-M-0061 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 20 semantic obligations before proof-phase acceptance. The denominator
is derived from stable registry fields and is bound to the exact statement and anchor-audit inputs.
The generated additive theorem, checked Fintype encoding, and product-identity support theorem do
not create duplicate root or proof-body credit.

No obligation is accepted closed. The anchor audit found a provisional `M0-W` candidate, while the
frozen `M0061-A-LAGRANGE` node and authoritative root remain `M3` until an exact proof-phase wrapper
and E1 receipt are accepted. The root vector remains `H1/M3/R4`.

## Typed proof route

```text
M0061-ROOT
`-- M0061-T-FINITE-SCOPE
    `-- M0061-A-LAGRANGE
        `-- M0061-L-CARD-PRODUCT
            |-- M0061-L-NATCARD-PROD
            |-- M0061-L-NATCARD-CONGR
            `-- M0061-C-COSET-PRODUCT-EQUIV
                |-- M0061-C-FIBER-DECOMPOSITION
                |-- M0061-T-FIBER-TO-COSET
                |-- M0061-C-LEFT-COSET-EQUIV
                `-- M0061-T-SIGMA-PRODUCT
```

Every proof requirement has a reciprocal composition edge. Source, provenance, evidence, trust,
documentation, and workflow edges remain in separate graphs and confer no proof closure.

## m0061-root

Exact finite-group Lagrange target. It consumes the finite-scope adapter and excludes no finite
group or subgroup boundary. Status: `[H1, M3, R4]`; no accepted proof evidence.

## m0061-s-interface

Freezes the universe, ordered `Group G` and `Finite G` binders, arbitrary `H : Subgroup G`,
`Nat.card`, and divisibility in `Nat`. It is a statement overlay, not another proof body.

## m0061-s-boundary

Retains the trivial group and bottom and top subgroups. No normality, properness, nontriviality,
commutativity, or cyclicity hypothesis may enter the route.

## m0061-s-fintype-transport

Owns the checked iff with the Fintype-card encoding. This representation crossing preserves the
exact group and subgroup and shares the canonical root identity.

## m0061-s-foundation

Owns final review of `propext`, `Classical.choice`, `Quot.sound`, the Lean kernel, compiled imports,
and the no-oracle policy. The current axiom output is provisional, not release-grade trust closure.

## m0061-t-finite-scope

Consumes arbitrary-group divisibility and reintroduces the catalog's explicit `Finite G` binder.
`finiteScope_of_arbitraryGroup` checks this one-way specialization into the exact root.

## m0061-a-lagrange

Central pinned bridge `Subgroup.card_subgroup_dvd_card`. Its short body is not treated as a leaf:
the product-cardinality route below owns its substantive mathematical work. The conditional
`divisibility_of_cardProduct` certificate consumes that route and yields this same canonical
obligation, so it is not counted as a second divisibility claim.

## m0061-l-card-product

States `Nat.card G = Nat.card (G ⧸ H) * Nat.card H`. The checked conditional composition consumes
product cardinality, cardinal congruence, and the coset-product equivalence.

## m0061-l-natcard-prod

Pinned bridge `Nat.card_prod`; it supplies cardinal multiplicativity for the quotient-subgroup
product and is separately provenance-audited rather than hidden as simplification.

## m0061-l-natcard-congr

Pinned bridge `Nat.card_congr`; it transports cardinality across the constructed equivalence and
does not itself construct that equivalence.

## m0061-c-coset-product-equiv

Constructs `G ≃ (G ⧸ H) × H`. `cosetProduct_of_fiber_engines` conditionally consumes every
construction and transport child below; the pinned body remains candidate-only.

## m0061-c-fiber-decomposition

Uses the quotient map to identify `G` with the sigma type of all its fibers via
`Equiv.sigmaFiberEquiv`. This exposes the partition of the group by quotient classes.

## m0061-t-fiber-to-coset

Transports each quotient-map fiber to the left coset represented by `Quotient.out`, using the
quotient-class/left-coset equality and `Quotient.out_eq'` inside a fiberwise sigma congruence.

## m0061-c-left-coset-equiv

Uses translation by a representative to identify every left coset with `H` through
`Subgroup.leftCosetEquivSubgroup`.

## m0061-t-sigma-product

After every fiber has become the constant type `H`, `Equiv.sigmaEquivProd` collapses the sigma
family to `(G ⧸ H) × H`.

## m0061-x-source

Primary-source edition, theorem/page, definition and assumption map, errata review, node crosswalk,
and independent acceptance remain open. The textbook lead and catalog label are not H0.

## m0061-x-provenance

Owns exact wrapper/body identity, pinned `Card.lean` and `Basic.lean` source blobs, imported
declarations, aliases, licenses, and transitive dependency closure without proof credit.

## m0061-x-trust

Owns transitive declaration, compiled-artifact, executable, axiom, replay, and supply-chain closure.
The current warm worker elaboration does not satisfy this release gate.

## m0061-x-readable

Requires a complete independently reviewed mathematical reconstruction of the coset-partition
proof. This architecture outline and its bounded ledgers remain `R4`, not R0.

## m0061-x-workflow

Binds dependency-ordered proof, validation, freshness, revocation, independent verification, and
release receipts without becoming a mathematical premise.

## Status boundary

The registry and seven typed graphs are frozen and self-testable. The anchor is not installed as
the canonical proof, all accepted-proof lists remain empty, and H0, accepted M0, R0, transitive
provenance/trust, validation, `AUDIT-Z`, theorem completion, release, and master acceptance remain
open.
