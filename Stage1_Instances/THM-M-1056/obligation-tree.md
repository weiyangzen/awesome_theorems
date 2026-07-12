# Frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 19 root-relevant obligations for
`S56-M-1056-OBLIGATION_TREE`. Eligibility was assigned from the exact statement,
the classical two-sided proof architecture, and the immutable anchor audit, not
from proof availability. Planned fingerprints are interfaces, not Lean evidence.
Any correction, split, merge, or exclusion requires a new version and an
append-only delta.

## Typed proof route

```text
M1056-ROOT exact canonical target
`-- M1056-T-ASSEMBLE checked conditional composition
    `-- M1056-T-CORE complete Oseledets package (minimal open root cut)
        |-- M1056-C-PROJECTIONS
        |   `-- M1056-L-TRANSVERSAL
        |       |-- M1056-C-FORWARD-FLAG
        |       `-- M1056-C-BACKWARD-FLAG
        |-- M1056-L-EQUIVARIANCE
        |   |-- M1056-C-FORWARD-FLAG
        |   `-- M1056-C-BACKWARD-FLAG
        `-- M1056-L-GROWTH
            |-- M1056-C-FORWARD-FLAG
            |-- M1056-C-BACKWARD-FLAG
            `-- M1056-L-KINGMAN
                `-- M1056-L-SUBADDITIVE
                    `-- M1056-N-ITERATES
```

Both flag constructions additionally require `M1056-N-COORDINATES`. Shared
nodes are counted once. Statement, boundary, foundation, external-anchor,
source, provenance, documentation, trust, and workflow relations live in
separate typed graphs and cannot masquerade as proof premises.

## Node ledger

### m1056-root
Exact elaborated target. `[H1, M3, R3]`; no inhabitant is supplied.

### m1056-s-interface
Checked cocycle, logarithm, and projection-splitting interfaces.
`[H1, M0-L, R3]`; definition elaboration is not theorem closure.

### m1056-s-boundary
Positive dimension, nonzero vectors, repeated exponent blocks, and a common
conull set must be handled explicitly. `[H1, M4, R3]`.

### m1056-s-foundation
Classical choice, measurable selection, imports, axioms, and TCB closure remain
to be audited. `[H1, M4, R3]`.

### m1056-n-iterates
Normalize `cocycleVector` to product and cocycle laws. Budget 40;
`[H1, M4, R3]`.

### m1056-n-coordinates
Transport the arbitrary finite-dimensional Borel normed fiber to matrices,
including measurability and norm-independent growth. This is not supplied by
the external anchor. Budget 40; `[H1, M4, R3]`.

### m1056-l-subadditive
Build integrable exterior-power subadditive processes. Budget 40;
`[H1, M4, R3]`.

### m1056-l-kingman
Obtain deterministic exterior-power growth limits from an exact Kingman
theorem. Pinned mathlib has no such terminal theorem. Budget 100;
`[H1, M4, R3]`.

### m1056-c-forward-flag
Construct the measurable forward filtration with dimension, invariance, and
growth invariants. Budget 100; `[H1, M4, R3]`.

### m1056-c-backward-flag
Construct the corresponding filtration for the inverse cocycle. Budget 100;
`[H1, M4, R3]`.

### m1056-l-transversal
Prove almost-sure transversality and intersection dimensions, producing a
direct-sum family. Budget 100; `[H1, M4, R3]`.

### m1056-c-projections
Construct strongly measurable complementary continuous projections from the
subspaces. Budget 40; `[H1, M4, R3]`.

### m1056-l-equivariance
Prove projection intertwining on a common invariant conull set. Budget 40;
`[H1, M4, R3]`.

### m1056-l-growth
Prove the limit for every nonzero vector in every summand simultaneously.
Budget 100; `[H1, M4, R3]`.

### m1056-t-core
Assemble every `LyapunovSplitting` field. This is the minimal open root cut;
`[H1, M4, R3]`.

### m1056-t-assemble
`root_of_oseledetsCorePackage` kernel-checks exact child-to-root composition.
`[H1, M0-L, R3]`; its explicit premise prevents proof credit.

### m1056-x-external
The pinned `ErgodicTheory.oseledets_splitting` anchor is matrix-specific,
toolchain-incompatible, and not imported. It is a provenance/source boundary,
not an exact proof. `[H1, M4, R3]`.

### m1056-x-source
Primary-source node locators, assumptions, conventions, errata, and independent
review remain pending. `[H1, M4, R3]`.

### m1056-x-provenance
Terminal bodies, wrappers, imports, axioms, TCB, and replay receipts remain
pending. Informational overlay; `[H1, M4, R3]`.

## Status boundary

The frozen minimal root cut is `M1056-T-CORE`. The checked conditional assembly
introduces no Oseledets proof. This phase claims no H0, root closure, audit
completion, theorem completion, or accepted receipt.
