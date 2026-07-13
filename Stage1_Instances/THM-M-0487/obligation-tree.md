# THM-M-0487 frozen obligation architecture

Item `S56-M-0487-OBLIGATION_TREE` freezes registry version 1 against the exact statement and the
bounded anchor audit. Its 54 canonical IDs are the denominator for later machine, human-source,
and readable coverage. The IDs and eligibility derive from the inspected Helfgott analytic route,
the Helfgott-Platt finite route, and a selected fail-closed formal certificate refinement. The
certificate format and kernel replay nodes are future architecture, not historical artifacts
claimed by the paper. They do not derive from candidate availability or current closure. Any
target change, split, merge, exclusion, risk change, or proof-body identity change requires a new
registry version and an append-only delta.

## Exact Composition

`ObligationTree.lean` defines `analyticCutoff = 10^27` and the disjoint packages

```text
AnalyticRangePackage: 10^27 <= n -> Odd n -> ThreePrimeRepresentation n
FiniteRangePackage:   5 < n -> n < 10^27 -> Odd n -> ThreePrimeRepresentation n
```

`cutoff_cases` checks exhaustiveness, `finiteCoverage_of_publishedUpper` checks that the exact
finite-source endpoint covers the finite side, `finiteRange_of_publishedFiniteUpper` consumes that
coverage and the open upper theorem, and `root_of_analytic_and_finite` consumes the cutoff
partition and both range packages to return the canonical target. These are conditional interfaces.
Neither range package is implemented or accepted.

## Proof Route

```text
M0487-ROOT exact weak Goldbach target [open H1/M3/R3]
`-- M0487-T-ASSEMBLE checked conditional composition
    |-- M0487-B-RANGE-SPLIT at 10^27 [checked interface]
    |-- M0487-T-ANALYTIC [open M4]
    |   `-- weighted Fourier identity and common parameters/weights
    |       |-- exhaustive major/minor arc construction
    |       |-- major characters, positive main factor, and all errors
    |       |-- minor exponential sums, prime large sieve, total bound
    |       |-- explicit dominance at the 10^27 cutoff
    |       `-- prime-power removal and actual-prime witness extraction
    `-- M0487-T-FINITE checked conditional restriction
        `-- exact finite upper theorem [open M4]
            |-- base/ladder case split and ternary reduction
            |-- selected certificate format and complete prime ladder refinement
            |-- Proth and general-prime certificates
            |-- exhaustive gap/endpoint checker soundness
            `-- finite binary Goldbach verification
```

The analytic route follows the main source's sections 1.3 and 2 through 7: one weighted
von-Mangoldt sum, common major/minor arc parameters, explicit lower and upper bounds, the strict
numeric margin, and removal of non-prime contributions. Major and minor estimates are not treated
as primitive one-line leaves; each has separate source, construction, case, error, and composition
obligations.

The finite route follows the Helfgott-Platt prime-ladder reduction, then selects a fail-closed
certificate-replay refinement for future Lean implementation. The exact inclusive upper
endpoint is `8,875,694,145,621,773,516,800,000,000,000`, recorded as the natural literal
`8875694145621773516800000000000`. The primary arXiv `1305.3062v2` source was inspected at its
abstract lines 94-96 and interval theorem lines 206-211. The local arithmetic theorem checks only
that `10^27` lies below this endpoint. It does not authenticate the historical computation, data,
primality certificates, independent checker, or binary Goldbach verification.

## Assurance Overlays

### m0487-s-interface

The exact natural binders, strict threshold, parity hypothesis, three independent prime witnesses,
repetition policy, addition association, and equality orientation remain fixed. The canonical
expression fingerprint is `29ac94dd...e703`.

### m0487-s-domain

The already checked integer/natural `Iff` transports the source's positive integer domain. No
negative, zero, or nonintegral input enters the root.

### m0487-s-boundary

Five is excluded, seven is included as `2 + 2 + 3`, eight is outside the odd premise, and neither
distinctness nor oddness of the summands is added.

### m0487-s-foundation

The final route may require classical Fourier analysis, explicit prime-distribution theorems,
interval arithmetic, primality certificate checking, and imported compiled artifacts. Their exact
axioms, executables, hashes, and TCB closure remain open.

### m0487-x-source-main

Helfgott arXiv `1312.7748v2` was inspected and content-hashed. The main theorem is at source lines
123-127, the proof architecture at lines 298-548, and final composition at lines 5313-5391. Full
dependency admission, assumptions, corrections, errata, and independent review remain H1 work.

### m0487-x-source-major

The main paper explicitly imports the upstream major-arcs Main Theorem and a bounded L-function
computation. Exact editions, statement maps, computation inputs, and review remain open.

### m0487-x-source-minor

The main paper explicitly imports the upstream minor-arcs section 1.1 estimates. Exact editions,
assumption maps, constants, and review remain open.

### m0487-x-source-prime-bounds

Every explicit theta, von-Mangoldt, prime-power, and final error estimate needs a pinpoint primary
source and assumption/constant crosswalk. None is H0 here.

### m0487-x-source-finite

Helfgott-Platt arXiv `1305.3062v2` supplies the exact finite theorem as an H1 lead. The compressed
source SHA-256 is `376ec723...1bf408`; decompressed TeX SHA-256 is `5a9026c9...50dac`.
The published narrative is not an admitted formal certificate.

### m0487-x-computation

No producer output, ladder data, complete domain digest, seed/environment, certificate bundle,
checker theorem, replay, deterministic resource record, tamper fixture, or incomplete-domain
fixture is admitted. The intended route is `certificate_replayed_by_kernel`; every required field
remains open and no computation receives proof credit.

### m0487-x-provenance

The anchor audit found no exact placeholder-free Lean proof body. The exact Formal Conjectures
surface is rejected, bounded placeholder-ancestry and binary projects are statement-mismatched,
and the exact foolishair surface is conditional scaffolding only. These records have no proof edge.

### m0487-x-readable

This file exposes the whole route and boundaries but is not a node-complete mathematical proof or
an independently reviewed `R0` reconstruction. Each open package's budget is a split threshold,
not a claim that a substantive leaf ledger already exists.

### m0487-x-workflow

Proof implementation, node evidence, source/trust admission, hermetic replay, independent
verification, release, freshness, and revocation receipts remain open. Workflow edges never act as
mathematical proof premises.

## Freeze Boundary

Registry scope, typed graph semantics, exact endpoint arithmetic, and conditional compositions are
self-tested pending master acceptance. Accepted closed obligations and accepted receipts are empty.
The root remains `[H1, M3, R3]`; no proof, H0, accepted M0, R0, `AUDIT-Z`, release, or `THEOREM-Z`
is claimed.
