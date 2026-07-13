# THM-M-0476 frozen obligation architecture

Item `S56-M-0476-OBLIGATION_TREE` freezes registry version 1 against the exact statement and the
immutable formal-anchor audit. Its 26 canonical semantic IDs are the denominator for later
machine, human-source, and readable coverage. Availability of `ZMod.wilsons_lemma` was not used to
exclude or merge material work. Any statement correction, split, merge, eligibility change, or
terminal-body change requires a new registry version and an append-only delta.

## Proof Route

```text
M0476-ROOT exact explicit-prime Wilson target [open M3]
`-- M0476-S-FACT-TRANSPORT explicit-prime to Fact interface
    `-- M0476-T-COMPOSE checked conditional composition
        |-- M0476-N-FACTORIAL-PRODUCT factorial to cast interval product
        |   |-- M0476-L-FACTORIAL-INTERVAL prod_Ico_id_eq_factorial
        |   `-- M0476-T-NAT-CAST-PRODUCT prod_natCast
        |-- M0476-C-RESIDUE-UNITS-BIJECTION interval representatives to all units
        |   |-- M0476-N-PRIME-ENDPOINT normalize (p - 1) + 1 to p
        |   |-- M0476-B-UNIT-VAL-RANGE positive and bounded representatives
        |   |-- M0476-L-UNIT-VAL-INJECTIVE unit and ZMod value injectivity
        |   |-- M0476-C-RESIDUE-TO-UNIT nonzero residue packaged by Units.mk0
        |   `-- M0476-T-REPRESENTATIVE-COE natCast_val agreement
        `-- M0476-T-UNITS-COE-NEGONE coerce the unit-product identity
            `-- M0476-T-INSERT-NEGONE insert negative one into the erased product
                `-- M0476-C-INVERSE-PAIRING cancel by inversion
                    `-- M0476-L-INVERSE-FIXED-POINTS classify fixed units
```

`M0476-L-WILSON` records the exact audited candidate body while provenance maps its visible route.
It is outside the local proof relation, is not a semantic leaf, and receives no accepted proof
credit in this phase.
`M0476-N-PRIME-ENDPOINT` separately owns the positivity and truncated-subtraction endpoint work as
an exact residue-bijection child.
The related product wrapper, stronger primality iff, converse, and external `Int.ModEq` theorem are
deduplicated and receive no independent root or proof-body credit.

Every parent-to-child `proof_requires` edge has a reciprocal child-to-parent `composes` edge.
The source-body expansions of `ZMod.wilsons_lemma` and
`FiniteField.prod_univ_units_id_eq_neg_one` are recorded as non-crediting provenance edges. Source,
evidence, trust, documentation, and workflow relations are separate graphs and cannot become proof
premises. A separate static task graph freezes all seven authoritative task contracts while
excluding mutable states and attempt counters from its hash.

## Node Boundaries

### m0476-root

The root is exactly `WilsonTheoremTarget`: natural `p`, explicit `p.Prime`, forward direction, and
equality of the factorial cast with negative one in `ZMod p`. It remains open at `H1/M3/R4`.

### m0476-s-interface

The natural domain, ordered explicit premise, factorial of `p - 1`, cast, modulus, equality, and
direction are fixed by expression fingerprint `ee76ed...a4ac`. This node creates no new theorem.

### m0476-s-boundary

The prime `p = 2` remains included. Zero, one, and composites are excluded only because they are
not prime. No oddness, nonzero, lower-bound, converse, or `p != 1` premise is added.

### m0476-s-fact-transport

`root_of_factWilsonAnchor` installs `Fact p.Prime` from the explicit hypothesis and consumes an
exact `FactWilsonAnchor`. The checked transport does not invoke the pinned Wilson theorem.

### m0476-s-foundation

The conditional composition declarations report `propext`, `Classical.choice`, and `Quot.sound`.
Complete transitive foundation, executable TCB, computation, and independent replay acceptance is
still required.

### m0476-t-compose

`factWilsonAnchor_of_bridges` consumes the factorial, residue-unit, and unit-product conclusions and
returns only the Fact-premise anchor. The separate parent `M0476-S-FACT-TRANSPORT` uses
`root_of_factWilsonAnchor` to return the canonical target. Both are conditional interfaces, so
their elaboration supplies no accepted root proof.

### m0476-l-wilson

The exact candidate body is
`git-blob:9401f7b96b43c2c0afa1f823857bd31a20ae0ac2:ZMod.wilsons_lemma`, pinned at
mathlib revision `8a178386...ea95`. Proof installation and release-grade provenance remain later
work.

### m0476-n-factorial-product

`factorialProduct_of_identities` checks the exact composition of the primitive factorial interval
identity with the product-cast transport. Neither child is silently absorbed.

### m0476-l-factorial-interval

`Finset.prod_Ico_id_eq_factorial` owns the induction identifying the interval product with the
factorial. It is an imported core lemma, not a notation rewrite.

### m0476-t-nat-cast-product

`Finset.prod_natCast` owns the representation crossing from a natural product to a product in
`ZMod p`.

### m0476-n-prime-endpoint

Primality yields `0 < p`, which aligns `succ (p - 1)` with `p` despite natural subtraction. This
normalization is visible in the pinned source and remains separately accountable.

### m0476-c-residue-units-bijection

`residueUnitsProduct_of_components` uses `Finset.prod_bij` and consumes all five endpoint, landing,
injectivity, surjectivity, and product-value children. The construction is checked only
under those five explicit premises.

### m0476-b-unit-val-range

A unit cannot have value zero; `ZMod.val_lt` supplies the upper bound. Together with the prime
endpoint normalization, this places each value in the exact interval.

### m0476-l-unit-val-injective

`Units.ext_iff` and `ZMod.val_injective` recover equality of units from equality of representative
values.

### m0476-c-residue-to-unit

Every interval member is nonzero in `ZMod p`; `Units.mk0` constructs the inverse-bearing unit and
`ZMod.val_cast_of_lt` identifies its representative.

### m0476-t-representative-coe

`ZMod.natCast_val` proves that casting a unit's canonical natural value returns its underlying
residue. This is the value-preservation field of the product bijection.

### m0476-l-units-product

The candidate generalized body is
`git-blob:fb3668d594f865e52f20c8af45e91e7e3b1eebd8:FiniteField.prod_univ_units_id_eq_neg_one`.
A same-typed local interface conditionally reconstructs inverse pairing, fixed-point
classification, and reinsertion of negative one. It does not invoke or certify identity with the
pinned body and grants no accepted proof credit.

### m0476-c-inverse-pairing

`unitEraseProduct_of_inversion` checks the `Finset.prod_involution` composition over all units
except negative one. Primitive group laws are kernel-derived locally; the exact fixed-point
classification is its only mathematical child premise.

### m0476-l-inverse-fixed-points

`Units.inv_eq_self_iff` classifies a unit fixed by inverse as one or negative one. Erasing negative
one and the `prod_involution` non-one premise remove both possible fixed points.

### m0476-t-insert-negone

`unitProductIdentity_of_erase` inserts negative one back into the paired erased product and uses
the child equality to obtain the full unit product.

### m0476-t-units-coe-negone

`unitsProductBridge_of_components` consumes the unit-valued identity. Finite-product coercion and
negative-one coercion are kernel-derived locally, yielding the exact final `ZMod p` product.

### m0476-x-source

The catalog formula has no accepted primary edition, theorem/page, assumption map, errata audit,
or independent review. Node-specific H0 evidence remains open and the root stays H1.

### m0476-x-provenance

The Wilson and generalized unit-product bodies have immutable identities and source hashes. The
complete transitive declaration, dependency, license, and replay packet remains a later gate.

### m0476-x-trust

This phase records the observed axiom set and no-oracle boundary only. It does not provide a
release-grade executable or transitive trust closure.

### m0476-x-readable

This file documents architecture and status boundaries. It is not a complete independently
reviewed readable proof reconstruction; R4 therefore remains unchanged.

### m0476-x-workflow

Proof installation, node validation, hermetic replay, independent verification, release,
freshness, and revocation acceptance remain open and never act as proof premises.

## Freeze Boundary

The checked Lean declarations are conditional compositions whose mathematical children are
parameters. They do not call `ZMod.wilsons_lemma` to construct the root. The exact pinned candidate
remains uninstalled and unaccepted, accepted closed obligations remain empty, and the authoritative
vector remains `[H1, M3, R4]`. This worker artifact claims neither
H0, accepted M0, R0, AUDIT-Z, release, nor theorem completion.
