# THM-M-1108 frozen obligation architecture

Item: `S56-M-1108-OBLIGATION_TREE`.

The registry freezes 18 semantic obligations before proof execution. It follows
the source-scale Poissonization, Robinson-Schensted, Toeplitz/Riemann-Hilbert,
and de-Poissonization route. The anchor audit found no reusable formal theorem,
so this architecture does not improve the root's machine debt.

## Typed proof route

```text
M1108-ROOT exact CanonicalStatement
`-- M1108-T-ASSEMBLE checked conditional composition
    |-- M1108-T-POISSONIZED PoissonizedAsymptotics
    |   |-- M1108-N-POISSON exact Poissonized CDF
    |   |-- M1108-C-RSK RSK and LIS/first-row identity
    |   |-- M1108-L-TOEPLITZ determinant representation
    |   |-- M1108-C-RHP Riemann-Hilbert steepest descent
    |   |-- M1108-L-PAINLEVE Hastings-McLeod identification
    |   `-- M1108-L-UNIFORM-ERROR uniform edge estimates
    `-- M1108-T-DEPOISSONIZE DePoissonizationTransfer
        |-- M1108-L-MONOTONE fixed-size comparisons
        |-- M1108-L-POISSON-TAIL size concentration
        `-- M1108-L-UNIFORM-ERROR shared uniform estimates
```

The statement, boundary, foundation, source, provenance, trust,
documentation, and workflow surfaces are separate typed graphs. They cannot be
used as undeclared proof premises or counted as mathematical proof bodies.

## Node ledger

### m1108-root
Exact elaborated BDJ target. `[H2, M3, R3]`; no inhabitant is claimed.

### m1108-s-defs
Frozen uniform-permutation, strict-LIS, normalized-CDF, and Tracy-Widom
interfaces. `[H2, M4, R3]`.

### m1108-s-boundary
Preserves `N = 0`, every real threshold, strictness, centering, and the
`N^(1/6)` scale. `[H2, M4, R3]`.

### m1108-s-foundation
Planned transitive axiom, import, computation, and TCB audit. `[H2, M4, R3]`.

### m1108-n-poisson
Defines the Poisson mixture without assuming its asymptotics. `[H2, M4, R3]`.

### m1108-c-rsk
Planned RSK bijection and exact LIS/first-row invariant. `[H2, M4, R3]`.

### m1108-l-toeplitz
Planned bridge from Poissonized Young-diagram counts to the analytic determinant
representation. `[H2, M4, R3]`.

### m1108-c-rhp
Planned Riemann-Hilbert problem, contour transformations, parametrices, and
error problem. `[H2, M4, R3]`.

### m1108-l-painleve
Planned identification of the edge model with the exact Hastings-McLeod
formula used by `IsTracyWidomCDF`. `[H2, M4, R3]`.

### m1108-l-uniform-error
Planned uniform edge-window estimates shared by the analytic limit and
de-Poissonization. `[H2, M4, R3]`.

### m1108-t-poissonized
The complete pointwise Poissonized limit package. `[H2, M4, R3]`; its Lean
interface exists, but it has no proof body.

### m1108-l-monotone
Planned two-sided monotonic comparison for fixed permutation sizes.
`[H2, M4, R3]`.

### m1108-l-poisson-tail
Planned Poisson concentration at the scale needed by the transfer.
`[H2, M4, R3]`.

### m1108-t-depoissonize
The full implication from the Poissonized package to the fixed-size canonical
limit. `[H2, M4, R3]`; its Lean interface exists, but it has no proof body.

### m1108-t-assemble
Kernel-checked composition consuming both terminal packages and returning the
exact root. `[H2, M0-L, R3]`; open premises prevent root proof credit.

### m1108-x-source
Pending node-level primary-source theorem/page/assumption/errata crosswalk.
`[H2, M4, R3]`; human-source boundary only.

### m1108-x-provenance
Pending content-addressed terminal-body and import provenance. `[H2, M4, R3]`;
informational overlay only.

### m1108-x-trust
Pending executable, kernel, dependency, automation, and independent-runner
trust record. `[H2, M4, R3]`; informational overlay only.

## Freeze boundary

The open root cut is `M1108-T-POISSONIZED` plus
`M1108-T-DEPOISSONIZE`. The checked composition theorem merely consumes these
premises. It proves neither package and supplies no root closure, audit
completion, or theorem completion. Registry changes require a new version and
an append-only old/new obligation delta.
