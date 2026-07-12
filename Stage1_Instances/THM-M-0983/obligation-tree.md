# THM-M-0983 frozen obligation architecture

Item: `S56-M-0983-OBLIGATION_TREE`.

The registry freezes ten semantic obligations from the exact statement and anchor audit. Eligibility
is assigned from the mathematics, not from the already observed mathlib candidate.

## Typed proof route

```text
M0983-ROOT exact Bernoulli strong law
`-- M0983-T-ASSEMBLE checked conditional composition
    |-- M0983-R-PAIRWISE joint independence to pairwise independence
    |-- M0983-B-STRONG-LAW pinned real IID strong-law interface
    `-- M0983-T-EXPECTATION expectation-to-p transport
```

Definitions, the empty-average boundary, foundation/trust policy, human-source mapping, terminal
body provenance, documentation, and workflow ordering occupy separate typed graphs. They cannot be
counted as proof premises.

## Node ledger

### m0983-root
Exact frozen target. `[H3, M3, R4]`; the architecture supplies no inhabitant.

### m0983-s-definitions
The empirical frequency and all binders/hypotheses have the statement-frozen meanings.
`[H3, M0-L, R4]`.

### m0983-s-boundary
The empty average is checked as zero; `p = 0` and `p = 1` are not excluded. `[H3, M0-L, R4]`.

### m0983-s-foundation
Foundation, TCB, axiom, and no-oracle classification remains an explicit release obligation.
`[H3, M3, R4]`.

### m0983-r-pairwise
Project family independence with `ProbabilityTheory.iIndepFun.indepFun`. `[H3, M3, R4]`.

### m0983-b-strong-law
Apply the pinned `ProbabilityTheory.strong_law_ae_real` terminal body to obtain convergence to
`mu[X 0]`. The Bernoulli-valued hypothesis is stronger than this analytic bridge needs.
`[H3, M3, R4]` pending proof-node evidence and acceptance.

### m0983-t-expectation
Rewrite the almost-sure limit along `mu[X 0] = p`. `[H3, M3, R4]`.

### m0983-t-assemble
`root_of_packages` kernel-checks that the preceding three interfaces produce the exact root.
`[H3, M0-L, R4]`; explicit package arguments prevent accidental root closure.

### m0983-x-source
The primary-source theorem/page/assumption/errata crosswalk remains unaccepted. `[H3, M4, R4]`.

### m0983-x-provenance
Terminal-body, import, axiom, TCB, and replay provenance remains a downstream evidence obligation.
`[H3, M3, R4]`.

## Freeze boundary

The minimal open root cut is `M0983-R-PAIRWISE`, `M0983-B-STRONG-LAW`, and
`M0983-T-EXPECTATION`. This phase freezes and validates their composition only. It claims neither
proof-node acceptance nor theorem completion. Any semantic split, merge, or eligibility change
requires a new registry version and append-only delta.
