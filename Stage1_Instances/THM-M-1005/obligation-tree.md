# THM-M-1005 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 14 canonical obligations before proof work: 12 required machine
obligations and two external/source overlays. The denominator projection is content-addressed in
`obligation-registry.json`. Eligibility follows the exact strong `L^p` architecture, not the
availability of the weaker pinned theorem. Any later correction, split, merge, or eligibility
change requires a new registry version and an append-only ID delta.

The two `X` nodes cannot supply machine proof credit. `M1005-X-WEAK-PROVENANCE` records the body and
trust boundary of `MeasureTheory.maximal_ineq`; `M1005-X-SOURCE` records the still-open pinpoint
human-source mapping. The anchor audit's search result therefore does not silently close any
analytic node.

## Typed proof route

```text
M1005-ROOT [open M3]
`-- M1005-T-ROOT-TRANSPORT [checked conditional composition]
    `-- M1005-T-STRONG-ESTIMATE [remaining root cut, M4]
        |-- M1005-N-ABS-SUBMARTINGALE
        |   |-- M1005-S-DEFINITIONS
        |   `-- M1005-S-BOUNDARIES
        |-- M1005-C-MAXIMUM
        |   |-- M1005-S-DEFINITIONS
        |   `-- M1005-S-BOUNDARIES
        |-- M1005-L-WEAK-MAXIMAL
        |   |-- M1005-N-ABS-SUBMARTINGALE
        |   `-- M1005-C-MAXIMUM
        |-- M1005-L-LAYER-CAKE
        |   `-- M1005-C-MAXIMUM
        |-- M1005-L-HOLDER
        |   |-- M1005-L-WEAK-MAXIMAL
        |   `-- M1005-L-LAYER-CAKE
        `-- M1005-L-CONSTANT
            `-- M1005-S-BOUNDARIES
```

`M1005-S-FOUNDATION` refines the root as a release-gating trust obligation. Separate provenance,
evidence, trust, documentation, and workflow graphs prevent those relations from masquerading as
proof dependencies. Every `proof_requires` edge has a reciprocal `composes` edge; the structural
validator checks reciprocity, acyclicity, uniqueness, and root reachability.

## Node ledger anchors

### m1005-root
Exact frozen public target. It remains open at `M3`.

### m1005-s-definitions
Elaborated process, filtration, maximum, exponent, norm, and constant vocabulary.

### m1005-s-boundaries
Planned checks for `1 < p < infinity`, inclusive `0,...,n`, and `n = 0`.

### m1005-s-foundation
Planned transitive import, axiom, TCB, and noncomputable-boundary certificate.

### m1005-n-abs-submartingale
Planned martingale-to-nonnegative-submartingale normalization for `|f|`.

### m1005-c-maximum
Planned measurability and norm/tail interfaces for the finite running maximum.

### m1005-l-weak-maximal
Bridge to the pinned weak theorem, with exact specialization still to be implemented.

### m1005-l-layer-cake
Planned tail-integral representation of the `L^p` moment.

### m1005-l-holder
Planned integration and Holder-duality estimate.

### m1005-l-constant
Planned `ENNReal` arithmetic identifying the exact `p / (p - 1)` coefficient.

### m1005-t-strong-estimate
The complete analytic package and the minimal open root cut.

### m1005-t-root-transport
`ObligationTree.lean` kernel-checks that the exact terminal package yields the exact public root.

### m1005-x-weak-provenance
Immutable support-only provenance for `MeasureTheory.maximal_ineq`; never strong-theorem credit.

### m1005-x-source
Open primary-source theorem/page, assumption, transition, and errata crosswalk.

## Status boundary

This phase freezes and structurally validates an architecture. It proves neither the weak-to-strong
analytic route nor Doob's strong inequality. No parent is credited merely because a conditional
composition harness elaborates. `H2`, root `M3`, and `R4` remain; there is no audit or theorem
completion claim.
