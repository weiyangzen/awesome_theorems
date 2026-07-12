# THM-M-1006 frozen obligation architecture

Item: `S56-M-1006-OBLIGATION_TREE`.

The registry freezes 18 semantic obligations before proof execution. It uses a finite
stopping-time and good-lambda route suited to the exact all-`p > 0` ENNReal target. The bounded
anchor audit found no exact Lean theorem, and the source audit remains H2, so this architecture
does not claim source or machine closure.

## Typed proof route

```text
M1006-ROOT exact StatementShape
`-- M1006-T-ASSEMBLE checked conditional pairing
    |-- M1006-T-LOWER square function <= maximal function
    |   |-- M1006-N-DIFFERENCES martingale differences and partial sums
    |   |-- M1006-N-SQUARE quadratic-variation/square-function transport
    |   |-- M1006-L-GOOD-LOWER reverse good-lambda inequality
    |   |   |-- M1006-C-STOPPING first-crossing stopping times
    |   |   `-- M1006-L-STOPPED stopped-martingale estimates
    |   |-- M1006-L-LAYERCAKE tail bounds to ENNReal moments
    |   `-- M1006-B-P-RANGE all positive exponent regimes
    `-- M1006-T-UPPER maximal function <= square function
        |-- M1006-N-DIFFERENCES
        |-- M1006-N-SQUARE
        |-- M1006-L-GOOD-UPPER good-lambda inequality
        |   |-- M1006-C-STOPPING
        |   `-- M1006-L-STOPPED
        |-- M1006-L-LAYERCAKE
        `-- M1006-B-P-RANGE
```

The refinement graph separately records definitions, ordered scope, boundary cases, and foundation
policy. Provenance, source, trust, documentation, and workflow edges cannot masquerade as proof
premises.

## Node ledger

### m1006-root
Exact elaborated target. `[H2, M3, R3]`; no inhabitant is supplied.

### m1006-s-definitions
Checked definitions of the finite maximal process and discrete quadratic variation. `[H2, M0-L, R3]`.

### m1006-s-scope
Checked binder order, uniform constants, probability and martingale premises, zero start, and finite
horizon. `[H2, M0-L, R3]`.

### m1006-s-boundary
Open exact lemmas for horizon zero, the zero martingale, and infinite ENNReal moments. `[H2, M4, R3]`.

### m1006-s-foundation
Open transitive axiom, TCB, import, and no-oracle certificate. `[H2, M4, R3]`.

### m1006-n-differences
Construct adapted martingale differences and prove finite partial-sum reconstruction. `[H2, M4, R3]`.

### m1006-n-square
Transport squared increments and square-root moments to the frozen `quadraticVariation^(p/2)`
integrand without changing infinite-value behavior. `[H2, M4, R3]`.

### m1006-c-stopping
Construct bounded first-crossing stopping times with measurability and adaptedness invariants.
`[H2, M4, R3]`.

### m1006-l-stopped
Establish the quantitative stopped-martingale estimates needed by both distribution inequalities.
`[H2, M4, R3]`.

### m1006-l-good-upper
Good-lambda tail control of the maximal process by the square function. `[H2, M4, R3]`.

### m1006-l-good-lower
Reverse distribution control of the square function by the maximal process. `[H2, M4, R3]`.

### m1006-l-layercake
Convert the tail inequalities to exact `lintegral` `rpow` moment inequalities for real `p > 0`,
including infinite moments. `[H2, M4, R3]`.

### m1006-b-p-range
Recompose subunit, unit, and superunit exponent regimes with constants depending only on `p`.
`[H2, M4, R3]`.

### m1006-t-lower
Assemble the lower directional package `LowerBDG`. `[H2, M4, R3]`.

### m1006-t-upper
Assemble the upper directional package `UpperBDG`. `[H2, M4, R3]`.

### m1006-t-assemble
Kernel-checked composition from both directional packages to the exact root. `[H2, M0-L, R3]`;
its explicit premises prevent root proof credit.

### m1006-x-source
Pending theorem-level primary-source passages, assumptions, conventions, errata, and review.
`[H2, M4, R3]`; this node has no machine-proof eligibility.

### m1006-x-provenance
Pending terminal-body, import, axiom, TCB, placeholder, and replay inventory. `[H2, M4, R3]`;
this informational overlay supplies no mathematical proof credit.

## Freeze boundary

The minimal open root cut is `M1006-T-LOWER` plus `M1006-T-UPPER`. The checked conditional assembly
does not prove either direction. This phase supplies no root closure, audit completion, H0/R0,
validation, release, or theorem completion. Any split, merge, correction, or eligibility change
requires a new registry version and an append-only delta.
