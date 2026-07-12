# THM-M-1026 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 16 canonical obligations before proof execution: 14 required machine
obligations and two source/provenance overlays. Eligibility follows the exact stable-law
biconditional, not the availability of the ordinary Gaussian CLT or supporting characteristic-
function APIs. The denominator projection is content-addressed in `obligation-registry.json`; any
later correction, split, merge, or eligibility change requires a new version and append-only delta.

The two `X` nodes carry no machine proof credit. `M1026-X-CHARFUN-PROVENANCE` records the pinned
supporting mathlib boundary. `M1026-X-SOURCE` records the still-open primary-source pinpoint map.

## Typed proof route

```text
M1026-ROOT [open M3]
`-- M1026-T-BRANCH-MERGE [checked conditional composition]
    |-- M1026-T-NECESSITY [remaining root cut, M4]
    |   `-- M1026-B-NECESSITY
    |       |-- M1026-C-BLOCK-DECOMPOSITION
    |       |   |-- M1026-S-DEFINITIONS
    |       |   `-- M1026-S-BOUNDARIES
    |       `-- M1026-L-LIMIT-COMPARISON
    |           |-- M1026-C-BLOCK-DECOMPOSITION
    |           `-- M1026-N-WEAK-CHARFUN
    |               `-- M1026-S-DEFINITIONS
    `-- M1026-T-CONVERSE [remaining root cut, M4]
        `-- M1026-B-CONVERSE
            |-- M1026-C-STABLE-WITNESS
            |   |-- M1026-S-DEFINITIONS
            |   `-- M1026-S-BOUNDARIES
            `-- M1026-L-CONSTANT-WEAK-LIMIT
                `-- M1026-C-STABLE-WITNESS
```

`M1026-S-FOUNDATION` refines and trust-gates the root. Separate refinement, provenance, evidence,
trust, documentation, and workflow graphs prevent those relations from masquerading as proof
premises. Every proof requirement has a reciprocal composition edge.

## Node ledger anchors

### m1026-root
Exact frozen public target; open at `M3`.

### m1026-s-definitions
Elaborated convolution, normalization, weak convergence, probability, nondegeneracy, stability,
and attraction vocabulary.

### m1026-s-boundaries
Positive scaling, `n >= 2`, nondegeneracy, and explicit zero/one index obligations.

### m1026-s-foundation
Open transitive import, foundation, TCB, and noncomputable-boundary certificate.

### m1026-n-weak-charfun
Open checked transport between the frozen weak convergence predicate and pinned Levy/characteristic-
function interfaces.

### m1026-b-necessity
The attraction-to-stability direction.

### m1026-c-block-decomposition
Open comparison of `mn` summands with `m` independent blocks of `n` summands, including affine maps.

### m1026-l-limit-comparison
Open convergence-of-types argument identifying the limit with every finite convolution power after
positive affine normalization.

### m1026-t-necessity
Complete necessity proposition and one member of the minimal root cut.

### m1026-b-converse
The stability-to-attraction direction.

### m1026-c-stable-witness
Open construction choosing the stable law itself and total normalizers, with zero and one handled.

### m1026-l-constant-weak-limit
Open rewrite to a constant sequence and its weak-convergence proof.

### m1026-t-converse
Complete converse proposition and the other member of the minimal root cut.

### m1026-t-branch-merge
`ObligationTree.lean` kernel-checks that the exact two directions yield the frozen biconditional.

### m1026-x-charfun-provenance
Pinned support-only provenance for `charFun_conv` and Levy convergence; never root proof credit.

### m1026-x-source
Open primary-source edition/theorem/page, assumptions, transition map, and errata record.

## Status boundary

This phase freezes and validates architecture. It does not prove either generalized-CLT direction.
The checked branch merge is conditional and supplies no closure credit for its open premises. Root
`M3`, human debt `H2`, readability debt `R4`, and theorem incompleteness remain.
