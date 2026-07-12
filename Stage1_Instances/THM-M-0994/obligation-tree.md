# THM-M-0994 frozen obligation architecture

Item: `S56-M-0994-OBLIGATION_TREE`.

Registry version 1 freezes 13 semantic obligations before proof execution. The
route uses the pinned mathlib subgaussian candidate, while keeping the exact
real-denominator transport and its zero-width behavior visible as obligations.

## Typed proof route

```text
M0994-ROOT exact canonical proposition
`-- M0994-T-ASSEMBLE checked conditional composition
    |-- M0994-T-PROXY pinned proxy-bound package
    |   |-- M0994-L-CENTER centered independence
    |   |-- M0994-L-INTERVAL-MGF Hoeffding lemma per coordinate
    |   `-- M0994-L-SUM-TAIL finite independent-sum tail theorem
    |-- M0994-L-ENDPOINTS a_i <= b_i from almost-sure interval membership
    |-- M0994-L-PROXY-ALG proxy/coercion/constant normalization
    `-- M0994-B-ZERO-WIDTH empty and zero-total-width boundary
```

`M0994-S-EXACT`, `M0994-X-PINNED`, `M0994-X-SOURCE`, and `M0994-X-TCB`
live in separate refinement, provenance, evidence, trust, documentation, and
workflow graphs. They cannot masquerade as proof premises.

## Node ledger

### root
Exact frozen upper-tail target. `[H2, M1, R3]`; no accepted root proof.

### s-exact
Binder, event, and denominator identity from `Statement.lean`. `[H2, M3, R3]`.

### l-center
Coordinatewise centering preserves independence. `[H2, M1, R3]`.

### l-interval-mgf
Pinned `hasSubgaussianMGF_of_mem_Icc`. `[H2, M1, R3]`.

### l-sum-tail
Pinned `measure_sum_ge_le_of_iIndepFun`. `[H2, M1, R3]`.

### l-endpoints
Checked extraction of `a i <= b i` from an almost-sure witness. `[H2, M0-L, R3]`.

### l-proxy-alg
Normalize `NNReal` proxy sums to the exact real squared-width denominator,
including coercions and the factor `2`. `[H2, M2, R3]`.

### b-zero-width
Preserve empty and zero-total-width families. Lean division by zero makes the
exact right side `exp 0 = 1`; no denominator-positivity premise may be added.
`[H2, M2, R3]`.

### t-proxy
Package the three pinned candidate steps, deduplicated by terminal body.
`[H2, M1, R3]`.

### t-assemble
Kernel-checked conditional assembly from the proxy and transport interfaces.
`[H2, M1, R3]`; its premises are not root closure.

### x-pinned
Immutable mathlib/import/body/alias provenance. `[H2, M1, R3]`.

### x-source
Hoeffding 1963 theorem/page/assumption/errata review remains open. `[H2, M5, R4]`.

### x-tcb
Transitive trust, license, environment, and replay audit remains open.
`[H2, M3, R4]`.

## Freeze boundary

The architecture-level remaining root cut is `M0994-T-PROXY`,
`M0994-L-PROXY-ALG`, and `M0994-B-ZERO-WIDTH`. The first is a pinned feasible
candidate, while the latter two split positive-width algebra from the boundary.
This phase supplies no proof-node acceptance, audit completion, or theorem
completion. Any registry correction needs version 2 and an append-only delta.
