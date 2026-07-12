# THM-M-0989 frozen obligation architecture

Item: `S56-M-0989-OBLIGATION_TREE`.

The registry freezes 15 semantic obligations before proof execution. It uses
the characteristic-function route supported by pinned mathlib's Levy theorem.
No exact triangular-array CLT anchor exists in the pinned dependency closure.

## Typed proof route

```text
M0989-ROOT exact frozen proposition
`-- M0989-T-ASSEMBLE checked conditional composition
    |-- M0989-S-MEAS finite row sums are AE-measurable
    |-- M0989-T-CHARFUN row-law characteristic functions converge
    |   |-- M0989-C-FACTOR independence gives a finite product
    |   |-- M0989-N-MOMENTS centered/unit-variance normalization
    |   |-- M0989-L-INFINITESIMAL uniform asymptotic negligibility
    |   |-- M0989-L-TRUNCATE Lindeberg tail control
    |   |-- M0989-L-TAYLOR small-increment exponential remainder
    |   `-- M0989-L-PRODUCT product/logarithm limit
    `-- M0989-T-LEVY pinned characteristic-function criterion
```

Definitions, trust, source mapping, documentation, and provenance are separate
typed graphs and cannot be counted as proof premises.

## Node ledger

### m0989-root
Exact `Statement`. `[H2, M3, R4]`; no inhabitant is supplied.

### m0989-s-definitions
Checked normalized array, truncation, and row-sum interface. `[H2, M0-L, R4]`.

### m0989-s-meas
Finite row-sum AE-measurability from increment measurability. `[H2, M4, R4]`.

### m0989-s-foundation
Pending transitive axiom, TCB, and no-oracle certificate. `[H2, M4, R4]`.

### m0989-c-factor
Row independence to the exact finite characteristic-function product. `[H2, M4, R4]`.

### m0989-n-moments
Centering and total-variance-one normalization. `[H2, M4, R4]`.

### m0989-l-infinitesimal
Uniform asymptotic negligibility derived from Lindeberg. `[H2, M4, R4]`.

### m0989-l-truncate
Large-increment remainder bounded by the Lindeberg sum. `[H2, M4, R4]`.

### m0989-l-taylor
Uniform second-order complex exponential remainder. `[H2, M4, R4]`.

### m0989-l-product
Finite product/logarithm convergence to `exp (-t^2/2)`. `[H2, M4, R4]`.

### m0989-t-charfun
Assembly of the six analytic packages into `RowLawCharFunConverges`. `[H2, M4, R4]`.

### m0989-t-levy
Pinned mathlib Levy bridge. The bridge declaration is checked, but its premise
is open. `[H2, M0-L, R4]`.

### m0989-t-assemble
Kernel-checked conditional composition from measurability and characteristic
functions to the exact target. `[H2, M0-L, R4]`; open inputs prevent root credit.

### m0989-x-source
Pending node-level primary-source passage, assumption, convention, and errata map. `[H2, M4, R4]`.

### m0989-x-provenance
Pending terminal-body, import, axiom, TCB, and replay inventory. `[H2, M4, R4]`.

## Freeze boundary

The minimal open root cut is `M0989-S-MEAS` plus `M0989-T-CHARFUN`.
The checked conditional assembly proves neither premise. Any registry split,
merge, correction, exclusion, or eligibility change requires version 2 and an
append-only delta. This phase supplies no root closure, audit completion, or
theorem completion.
