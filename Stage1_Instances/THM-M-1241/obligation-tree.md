# THM-M-1241 frozen obligation architecture

Item: `S56-M-1241-OBLIGATION_TREE`.

The registry freezes 15 obligations before proof execution. It separates the
finite-exponent analytic route from the infinite endpoints, including the
source's special zero-order hypothesis. No exact local mathlib anchor exists,
so the substantive analytic nodes remain open.

## Typed proof route

```text
M1241-ROOT exact canonical proposition
`-- M1241-T-ASSEMBLE checked conditional composition
    |-- M1241-T-FINITE finite q and r package
    |   |-- M1241-R-SMOOTH density/approximation
    |   |-- M1241-L-LOCAL local scale estimate
    |   |-- M1241-L-NORM global derivative norm estimate
    |   |-- M1241-C-OPTIMIZE scale optimization
    |   `-- M1241-B-CRITICAL integer critical branch
    `-- M1241-T-ENDPOINT q or r infinite package
        |-- M1241-B-INFINITY infinite-norm estimates
        `-- M1241-B-ZERO exceptional zero-order branch
```

The interface, foundation, source, provenance, documentation, and workflow
nodes live in separate typed graphs and supply no proof premises.

## Node ledger

### m1241-root
Exact elaborated target. `[H2, M3, R4]`; no proof inhabitant is claimed.

### m1241-s-interface
Checked definitions and fixed-parameter conclusion used by the conditional composition. `[H2, M0-L, R4]`.

### m1241-s-foundation
Pending transitive import, axiom, TCB, classical-choice, and no-oracle audit. `[H2, M4, R4]`.

### m1241-r-smooth
Transfer from `ContDiff` inputs with finite seminorms to a proof-ready dense class while preserving limiting estimates. `[H2, M4, R4]`.

### m1241-l-local
Taylor/finite-difference estimate for each ordered coordinate derivative at a free scale. `[H2, M4, R4]`.

### m1241-l-norm
Global `eLpNorm` estimate and uniform finite supremum over coordinate directions. `[H2, M4, R4]`.

### m1241-c-optimize
Choose the scale to derive the product with real powers `a` and `1-a`. `[H2, M4, R4]`.

### m1241-b-critical
Finite-r integer critical case, respecting the source's `a < 1` exclusion. `[H2, M4, R4]`.

### m1241-t-finite
Assemble arbitrary finite `q,r` into `FiniteExponentPackage`. `[H2, M4, R4]`.

### m1241-b-infinity
Handle `q = infinity` or `r = infinity` and the reciprocal-exponent convention. `[H2, M4, R4]`.

### m1241-b-zero
Use exactly `ZeroOrderExceptionalHypothesis` in the printed `j=0`, subcritical, `q=infinity` case. `[H2, M4, R4]`.

### m1241-t-endpoint
Assemble the complement of finite `q,r` into `InfiniteEndpointPackage`. `[H2, M4, R4]`.

### m1241-t-assemble
Kernel-checked exhaustive split and exact root composition. `[H2, M0-L, R4]`; both package premises remain open.

### m1241-x-source
Pending theorem-passage, assumption, convention, and errata map for each analytic node. `[H2, M4, R4]`.

### m1241-x-provenance
Pending terminal-body, wrapper, import, axiom, TCB, and replay inventory. `[H2, M4, R4]`.

## Freeze boundary

The minimal open root cut is `M1241-T-FINITE` plus `M1241-T-ENDPOINT`.
The conditional assembly proves neither package. Changes to the inventory or
eligibility denominators require a new registry version and append-only delta.
This phase supplies no audit completion or theorem completion.
