# Frozen obligation architecture

## Freeze boundary

This is registry version 1 for `S56-M-1029-OBLIGATION_TREE`. It freezes 14
root-relevant obligations before proof execution. Eligibility does not depend
on proof availability. Planned fingerprints identify intended interfaces, not
Lean evidence. Any later correction, split, merge, or exclusion requires a new
registry version and an append-only delta.

## Typed proof route

```text
M1029-ROOT exact canonical proposition
`-- M1029-T-ASSEMBLE checked conditional composition
    `-- M1029-T-INCREMENTS independence and Gaussian law for every increment
        |-- M1029-L-GAUSSIAN-LAW characteristic-function uniqueness
        |   `-- M1029-L-CONDITIONAL-CHARACTERISTIC
        |       `-- M1029-L-EXPONENTIAL-MARTINGALE
        |           |-- M1029-N-QUADRATIC-VARIATION
        |           `-- M1029-C-EXPONENTIAL
        `-- M1029-L-INDEPENDENCE conditional characteristic criterion
            `-- M1029-L-CONDITIONAL-CHARACTERISTIC (shared body)
```

Statement definitions, the zero-elapsed boundary, foundation policy, source
mapping, provenance, documentation, and workflow order are separate typed
graphs. None can masquerade as a proof premise.

## Node ledger

### m1029-root
Exact elaborated Levy target. `[H2, M3, R4]`; no inhabitant is supplied.

### m1029-s-definitions
Checked time, process, compensated-square, and Brownian conclusion definitions.
`[H2, M0-L, R4]`.

### m1029-s-boundary
Checked direct target expansion and the `s=t` variance-zero boundary.
`[H2, M0-L, R4]`; this is statement evidence only.

### m1029-s-foundation
Pending import, axiom, classical-choice, measure-theory TCB, and no-oracle
certificate. `[H2, M4, R4]`.

### m1029-n-quadratic-variation
Derive deterministic quadratic variation from the compensated-square
martingale. This is a central stochastic-calculus bridge and cannot be hidden
as a library call. Planned budget 100; `[H2, M4, R4]`.

### m1029-c-exponential
Construct the frequency-indexed complex exponential process and prove its
measurability and integrability invariants. Planned budget 40; split further
if implementation exposes stochastic-integral subpackages. `[H2, M4, R4]`.

### m1029-l-exponential-martingale
Prove the exponential process is a martingale from quadratic variation.
Central bridge, budget 100; exact stochastic-calculus dependencies remain
open. `[H2, M4, R4]`.

### m1029-l-conditional-characteristic
Obtain the conditional characteristic function of each future increment.
This shared semantic body feeds both law and independence and receives credit
once only. Budget 100; `[H2, M4, R4]`.

### m1029-l-gaussian-law
Use characteristic-function uniqueness to identify `gaussianReal 0 (t-s)`,
including zero variance. Budget 40; `[H2, M4, R4]`.

### m1029-l-independence
Use the deterministic conditional characteristic function to prove
independence from `F_s`. Budget 40; `[H2, M4, R4]`.

### m1029-t-increments
Combine law and independence for every `s <= t`. This is the minimal open root
cut. `[H2, M4, R4]`.

### m1029-t-assemble
`root_of_incrementLawPackage` kernel-checks exact composition while keeping the
increment package explicit. `[H2, M0-L, R4]`; conditional composition is not
root proof credit.

### m1029-x-source
Pending primary-source theorem/page/assumption/convention/errata mapping for
every analytic bridge. `[H2, M4, R4]`.

### m1029-x-provenance
Pending terminal-body, wrapper, import, axiom, TCB, and replay inventory.
Informational overlay with no independent proof credit. `[H2, M4, R4]`.

## Status boundary

The frozen minimal root cut is `M1029-T-INCREMENTS`. The checked conditional
assembly introduces no Levy proof. This phase claims no H0, root closure,
audit completion, theorem completion, or accepted receipt.
