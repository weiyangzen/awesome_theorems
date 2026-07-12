# THM-M-0158 frozen obligation architecture

Item: `S56-M-0158-OBLIGATION_TREE`.

The registry freezes 15 semantic obligations before proof execution. No exact formal anchor exists,
so the route differentiates the unit and orthogonality identities and solves the resulting Gram
systems. The source boundary remains open and the architecture does not improve H debt.

## Typed proof route

```text
M0158-ROOT exact canonical proposition
`-- M0158-T-ASSEMBLE checked conditional composition
    `-- M0158-T-RECONSTRUCT reconstruct each N_i in the ambient basis
        |-- M0158-C-BASIS derive the basis N,x_0,x_1 from unit normal and det(I) != 0
        |-- M0158-L-UNIT differentiate norm-one to get <N,N_i> = 0
        |   `-- M0158-N-WITHIN justify local within-derivative rules at p
        `-- M0158-L-GRAM-SOLVE solve I*c_i = -II_i
            |-- M0158-L-ORTHOG differentiate <N,x_k> = 0
            |   `-- M0158-N-WITHIN
            `-- M0158-N-SIGN-INDEX fix the sign and matrix-column convention
```

Definitions, domain and boundary checks, foundation policy, source mapping, provenance, evidence,
documentation, and workflow order are separate typed graphs. They cannot count as proof premises.

## Node ledger

### m0158-root
Exact elaborated target. `[H1, M3, R4]`; no inhabitant is supplied.

### m0158-s-definitions
Checked definitions of partials, `I`, `II`, inverse, indices, and scalar action. `[H3, M0-L, R4]`.

### m0158-s-domain
Open-domain, interior-point, smoothness, unit normal, orthogonality, and Gram regularity contract.
`[H1, M4, R4]`.

### m0158-s-boundary
Singular and outside-domain exclusions plus orientation reversal behavior. `[H1, M4, R4]`.

### m0158-s-foundation
Pending classical-choice, import-closure, axiom, TCB, and no-oracle audit. `[H3, M4, R4]`.

### m0158-n-within
Interior reduction needed to apply derivative rules to identities stated on `U`. `[H1, M4, R4]`.

### m0158-n-sign-index
Show differentiated orthogonality yields the frozen `II k i` and negative inverse-column convention.
`[H1, M4, R4]`.

### m0158-l-unit
Differentiate `||N|| = 1` to obtain `<N,N_i> = 0`. `[H1, M4, R4]`.

### m0158-l-orthog
Differentiate `<N,x_k> = 0` to obtain `<x_k,N_i> = -II k i`. `[H1, M4, R4]`.

### m0158-c-basis
From the nonsingular Gram matrix prove `x_0,x_1` independent; with unit orthogonal `N`, construct an
ambient basis suitable for extensionality. `[H1, M4, R4]`.

### m0158-l-gram-solve
Use both nonsingular-inverse identities to solve the two coefficient systems. `[H1, M4, R4]`.

### m0158-t-reconstruct
Match inner products against `N,x_0,x_1` and derive the exact vector equality for every `i`.
`[H1, M4, R4]`.

### m0158-t-assemble
Kernel-checked composition from the exact derivation package into the canonical root.
`[H1, M0-L, R4]`; its premise remains open.

### m0158-x-source
Pending exact source theorem/page, hypotheses, sign conventions, proof boundary, and errata map.
`[H1, M4, R4]`; this node has no machine-proof eligibility.

### m0158-x-provenance
Pending terminal-body, declaration dependency, axiom, TCB, and replay inventory. `[H3, M4, R4]`.

## Freeze boundary

The minimal open root cut is `M0158-T-RECONSTRUCT`. The conditional assembly is deliberately not a
proof of that premise. This phase supplies no root closure, H0, R0, audit completion, or theorem
completion. Any split, merge, correction, or eligibility change requires registry version 2 and an
append-only delta.
