# THM-M-0346 frozen obligation architecture

Item: `S56-M-0346-OBLIGATION_TREE`.

The registry freezes 11 obligations before proof execution. It uses the audited external
Carleson-Hunt candidate as an anchor only: integration, trust, and every encoding transport remain
explicit obligations and receive no machine-proof credit.

## Typed proof route

```text
M0346-ROOT exact canonical proposition
`-- M0346-T-ASSEMBLE checked conditional composition
    |-- M0346-C-REPRESENTATIVE Lp representative and MemLp certificate
    |-- M0346-N-NORMALIZATION circle, Haar, character, and coefficient conventions
    |-- M0346-N-CUTOFF upstream partial sum equals inclusive [-N,N] sum
    |-- M0346-L-CARLESON-HUNT integrated, kernel-checked p=2 theorem
    `-- M0346-T-AE-REP transport the limit back to the Lp coercion a.e.
```

`M0346-S-ENCODING`, `M0346-S-FOUNDATION`, `M0346-X-SOURCE`, and
`M0346-X-PROVENANCE` live in separate refinement, trust, provenance, documentation, and workflow
graphs. They cannot masquerade as mathematical proof premises.

## Node ledger

### m0346-root
Exact elaborated target. `[H3, M3, R4]`; no inhabitant is supplied.

### m0346-s-encoding
Checked frozen statement definitions and conventions. `[H3, M0-L, R4]`.

### m0346-s-foundation
Open axiom, TCB, import-closure, classical-choice, and no-oracle audit. `[H3, M4, R4]`.

### m0346-c-representative
Construct a measurable representative of the `Lp` class and its `MemLp 2` certificate. `[H3, M4, R4]`.

### m0346-n-normalization
Match period, Haar probability normalization, character sign, and coefficients. `[H3, M4, R4]`.

### m0346-n-cutoff
Prove equality of the upstream cutoff and `Finset.Icc (-N) N`. `[H3, M4, R4]`.

### m0346-l-carleson-hunt
Integrate and kernel-check the external theorem at `p = 2`; the audited upstream revision currently
uses a different Lean and mathlib pin and is anchor-only. `[H3, M4, R4]`.

### m0346-t-ae-rep
Use representative equality a.e. to transport the limit to the exact frozen conclusion. `[H3, M4, R4]`.

### m0346-t-assemble
Kernel-checked conditional conversion from the fully transported contract to the exact root.
`[H3, M0-L, R4]`; the explicit premise prevents root proof credit.

### m0346-x-source
Pending node-level primary-source theorem/page/assumption/errata map. `[H3, M4, R4]`.

### m0346-x-provenance
Pending terminal-body, dependency, license, axiom, TCB, and replay inventory. `[H3, M4, R4]`.

## Freeze boundary

The minimal open root cut is the five children of `M0346-T-ASSEMBLE`. The conditional assembly is
not a proof of any child. This phase supplies no root closure, audit completion, or theorem
completion. Registry changes require a new version and an append-only delta.
