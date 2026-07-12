# THM-M-1250 frozen obligation architecture

Item: `S56-M-1250-OBLIGATION_TREE`.

The version-one registry freezes 15 semantic obligations before proof execution.
The selected route is the exact mathlib structure route: project `smooth'` and
`decay'` in the forward direction, and provide those same fields to
`SchwartzMap.mk` in the reverse direction.

## Typed proof route

```text
M1250-ROOT exact canonical proposition
`-- M1250-T-ASSEMBLE checked conditional composition
    |-- M1250-F-PACKAGE bundled to classical
    |   |-- M1250-F-SMOOTH project smooth'
    |   |-- M1250-F-DECAY project decay'
    |   `-- M1250-S-EQUALITY rewrite along toFun equality
    `-- M1250-R-PACKAGE classical to bundled
        |-- M1250-R-SMOOTH supply smooth'
        |-- M1250-R-DECAY supply decay'
        |-- M1250-R-CONSTRUCT assemble SchwartzMap.mk
        `-- M1250-S-BOUNDARY retain n = 0 and zero functions
```

## Node ledger

### m1250-root
Exact elaborated target. `[H2, M3, R3]`; no inhabitant is claimed.

### m1250-t-assemble
Kernel-checked composition from the two packages to the exact target.
`[H2, M0-L, R3]`; explicit premises prevent root credit.

### m1250-f-package
Forward implication combining projection and equality transport. `[H2, M4, R3]`.

### m1250-f-smooth
Exact `smooth'` projection anchor. `[H2, M1, R3]`.

### m1250-f-decay
Exact `decay'` projection anchor, preserving non-strict bounds. `[H2, M1, R3]`.

### m1250-r-package
Reverse implication producing the existential representative. `[H2, M4, R3]`.

### m1250-r-smooth
Constructor smoothness field. `[H2, M1, R3]`.

### m1250-r-decay
Constructor decay field with unchanged `k`, `r`, `C`, `x` order. `[H2, M1, R3]`.

### m1250-r-construct
Bundle fields using `SchwartzMap.mk` and establish coercion equality. `[H2, M1, R3]`.

### m1250-s-equality
Transport `ContDiff` and every iterated derivative bound from `phi` to `f`.
This is kept separate because dependent rewriting is the main integration risk.
`[H2, M4, R3]`.

### m1250-s-boundary
No positive-dimension or nonzero-function premise may enter. `[H2, M4, R3]`.

### m1250-s-foundation
Pending transitive axiom, import, TCB, and no-oracle certificate. `[H2, M4, R3]`.

### m1250-x-source
Pending primary-source pinpoint and node crosswalk. `[H2, M4, R3]`.

### m1250-x-provenance
Pending terminal-body and transitive provenance closure. `[H2, M4, R3]`.

### m1250-x-trust
Pending replay and compiled-artifact trust record. `[H2, M4, R3]`.

## Freeze boundary

The minimal open root cut is `M1250-F-PACKAGE` plus `M1250-R-PACKAGE`.
The checked conditional assembly is not a proof of either premise. This phase
supplies no root closure, audit completion, or theorem completion. Registry
changes require a new version and append-only ID delta.
