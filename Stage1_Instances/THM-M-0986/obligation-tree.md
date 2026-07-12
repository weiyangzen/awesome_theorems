# Frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 11 root-relevant obligations for
`S56-M-0986-OBLIGATION_TREE`. Eligibility is derived from the exact target and
the strong-law-to-convergence-in-measure route, not from the already discovered
mathlib candidate. Planned fingerprints are architecture identifiers, not Lean
proof evidence. A correction, split, merge, or exclusion requires a new version
and an append-only delta.

## Typed proof route

```text
M0986-ROOT exact Khinchin weak-law target
`-- M0986-T-ASSEMBLE checked conditional composition
    `-- M0986-T-AE-IN-MEASURE measurable AE convergence implies convergence in measure
        |-- M0986-L-STRONG-LAW almost-everywhere iid strong law
        `-- M0986-C-AVERAGE-MEASURABLE every empirical average is measurable
            `-- M0986-N-MEASURABILITY every observation is measurable
```

Definitions, the empty-average boundary, foundation policy, source mapping,
provenance, documentation, and workflow ordering live in separate typed graphs.
They cannot silently become proof premises or inflate machine coverage.

## Node ledger

### m0986-root

The exact real-valued target. `[H1, M3, R3]`; no root inhabitant is supplied.

### m0986-s-definitions

The empirical average, iid assumptions, expectation, and `TendstoInMeasure`
encoding are elaborated. `[H1, M0-L, R3]`; statement credit only.

### m0986-s-boundary

The direct target expansion and empty average at `n = 0` are checked.
`[H1, M0-L, R3]`; this does not establish asymptotic convergence.

### m0986-s-foundation

The transitive axiom, quotient, classical-choice, integration, import, and TCB
certificate remains open. `[H1, M4, R3]`.

### m0986-n-measurability

Transfer integrability and identical distribution to strong measurability of
each `X i`. Planned budget 40; `[H1, M4, R3]`.

### m0986-c-average-measurable

Establish strong measurability of every finite empirical average. The Lean
interface is frozen but has no accepted proof body in this phase. Budget 40;
`[H1, M3, R3]`.

### m0986-l-strong-law

Obtain almost-everywhere convergence under the exact iid-integrability
hypotheses. The anchor audit found `ProbabilityTheory.strong_law_ae`, but
candidate discovery is not accepted closure. Budget 80; `[H1, M3, R3]`.

### m0986-t-ae-in-measure

Use measurable averages to transport almost-everywhere convergence to
convergence in measure. The bridge must retain both children. Budget 80;
`[H1, M4, R3]`.

### m0986-t-assemble

`root_of_strongLaw_packages` kernel-checks the exact final composition while
leaving both substantive packages explicit. `[H1, M0-L, R3]`; conditional
composition is not root proof credit.

### m0986-x-source

The immutable primary-source transcription, historical assumptions,
translation, errata, and stronger-route crosswalk remain open. `[H1, M4, R3]`.

### m0986-x-provenance

The terminal body, wrapper, imports, axioms, TCB, and replay receipts remain an
informational overlay with no independent proof credit. `[H1, M4, R3]`.

## Status boundary

The frozen minimal root cut is the pair `M0986-L-STRONG-LAW` and
`M0986-C-AVERAGE-MEASURABLE`. The checked conditional assembly introduces no
weak-law proof. This phase claims no accepted receipt, H0, root closure, audit
completion, or theorem completion.
