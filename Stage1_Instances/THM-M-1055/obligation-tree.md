# Frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 14 root-relevant obligations before proof
execution. Eligibility is independent of proof availability. Planned
fingerprints identify intended interfaces, not Lean evidence. Any correction,
split, merge, or exclusion requires a new version and append-only delta.

## Typed proof route

```text
M1055-ROOT exact canonical proposition
`-- M1055-T-ASSEMBLE checked conditional composition
    `-- M1055-T-INVARIANT-LIMIT convergence to the constant integral
        |-- M1055-L-POINTWISE-LIMIT
        |   `-- M1055-A-EXTERNAL-INTEGRATION
        |-- M1055-L-ERGODIC-CONSTANCY
        |   |-- M1055-L-LIMIT-MEASURABLE
        |   `-- M1055-L-LIMIT-INVARIANT
        `-- M1055-L-INTEGRAL-IDENTIFICATION
            |-- M1055-L-POINTWISE-LIMIT (shared body)
            `-- M1055-L-ERGODIC-CONSTANCY (shared body)
```

Statement boundaries, foundation policy, source mapping, provenance,
documentation, and workflow order live in separate typed graphs and cannot
masquerade as proof premises.

## Node ledger

### m1055-root
Exact elaborated Birkhoff target. `[H2, M3, R4]`; no inhabitant is supplied.

### m1055-s-definitions
Checked `Ergodic`, `Integrable`, `birkhoffAverage`, integral, and a.e.
vocabulary. `[H2, M0-L, R4]`.

### m1055-s-boundary
Checked exact expansion, including probability normalization and the `n = 0`
average convention. `[H2, M0-L, R4]`; statement evidence only.

### m1055-s-foundation
Pending import, axiom, classical-choice, integration TCB, and no-oracle
certificate. `[H2, M4, R4]`.

### m1055-a-external-integration
Port the immutable `pointwise-birkhoff` candidate across Lean/mathlib version
drift and declaration collisions. This is an explicit integration obligation,
not an M0 anchor. Budget 100; `[H2, M4, R4]`.

### m1055-l-pointwise-limit
Obtain the general a.e. convergence theorem with the exact local average and
an invariant conditional-expectation limit. Budget 100; `[H2, M4, R4]`.

### m1055-l-limit-measurable
Supply the measurability and integrability interface required to apply the
ergodic-function theorem. Budget 40; `[H2, M4, R4]`.

### m1055-l-limit-invariant
Prove shift invariance of the selected pointwise limit. Budget 40;
`[H2, M4, R4]`.

### m1055-l-ergodic-constancy
Use `Ergodic.ae_eq_const_of_ae_eq_comp_ae` only after its exact hypotheses are
checked. The library declaration is a bridge, not the pointwise theorem.
Budget 40; `[H2, M4, R4]`.

### m1055-l-integral-identification
Preserve the observable's integral through the averages and limit, then use
probability normalization to identify the constant. Budget 100;
`[H2, M4, R4]`.

### m1055-t-invariant-limit
Combine convergence and identification into `InvariantLimitPackage`. This is
the minimal open root cut. `[H2, M4, R4]`.

### m1055-t-assemble
`root_of_invariantLimitPackage` kernel-checks exact final composition while
keeping the analytic package explicit. `[H2, M0-L, R4]`; conditional
composition is not root proof credit.

### m1055-x-source
Pending primary-source theorem/page/assumption/convention/errata map for every
analytic bridge. `[H2, M4, R4]`.

### m1055-x-provenance
Pending terminal-body, external-origin, wrapper, import, axiom, TCB, and replay
inventory. Informational overlay with no proof credit. `[H2, M4, R4]`.

## Status boundary

The frozen minimal root cut is `M1055-T-INVARIANT-LIMIT`. The checked
conditional assembly introduces no Birkhoff proof. This phase claims no H0,
root closure, audit completion, theorem completion, or accepted receipt.
