# THM-M-1245 frozen obligation architecture

Item: `S56-M-1245-OBLIGATION_TREE`.

The registry freezes nine obligations before proof integration. The selected
route is the exact audited mathlib scalar estimate, not a broadened Sobolev
space, bounded-domain, fractional, or Fourier substitute.

## Typed proof route

```text
M1245-ROOT exact canonical proposition
`-- M1245-T-WITNESS explicit mathlib constant witnesses exists C
    `-- M1245-A-TERMINAL pinned scalar inner-product estimate
        |-- M1245-B-FINRANK Euclidean finrank equals n
        `-- M1245-B-EXPONENT conjugacy transport across finrank
```

`M1245-S-STATEMENT` records the checked binder and definition boundary.
`M1245-X-SOURCE`, `M1245-X-TRUST`, and `M1245-X-PROVENANCE` live in separate
source, trust, provenance, documentation, and workflow graphs and cannot be
counted as proof premises.

## Node ledger

### m1245-root
Exact elaborated target. `[H2, M1, R3]`; it remains open in this phase.

### m1245-s-statement
Checked expansion preserving all binders, hypotheses, norms, and the uniform
constant placement. `[H2, M0-L, R3]`.

### m1245-b-finrank
Checked Euclidean finrank-to-dimension bridge, including positivity.
`[H2, M0-L, R3]`.

### m1245-b-exponent
Checked transport of the inverse-exponent equation to the terminal theorem's
finrank form. `[H2, M0-L, R3]`.

### m1245-a-terminal
Pinned terminal declaration
`MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner`. Its applicability was
checked by the anchor audit, but the named root wrapper is deliberately owned
by the proof node. `[H2, M1, R3]`.

### m1245-t-witness
Kernel-checked conditional composition choosing mathlib's explicit nonnegative
constant outside the function binder. `[H2, M0-L, R3]`; its premise is not
silently treated as closed.

### m1245-x-source
Primary-source theorem/page/assumption/definition/errata mapping remains open.
It is human-source evidence only and receives no machine proof credit.

### m1245-x-trust
Transitive proof-body, axiom, import, TCB, and no-oracle acceptance remains
open even though the audit recorded the immediate axiom probe.

### m1245-x-provenance
Immutable terminal-body, wrapper, recipe, replay, and release evidence remains
open and informational for machine coverage.

## Freeze boundary

The minimal open root cut is `M1245-A-TERMINAL`. The conditional wrapper is not
a proof of that premise. Any split, merge, correction, or eligibility change
requires a new registry version and append-only delta. This phase supplies no
H0, M0 root, R0, audit completion, or theorem completion.
