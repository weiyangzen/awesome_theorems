# THM-M-1234 frozen obligation architecture

Item: `S56-M-1234-OBLIGATION_TREE`.

The registry freezes 14 root-relevant obligations before proof execution. It
uses the approximation, uniform-estimate, compactness, and limit-passage route.
The anchor audit found no exact external closure, and the primary-source
premise crosswalk remains incomplete, so this architecture gives no new H or
root-proof credit.

## Typed proof route

```text
M1234-ROOT exact Statement
`-- M1234-T-ASSEMBLE checked conditional composition
    |-- M1234-A-STRUCTURE construct candidate fields
    |   |-- M1234-A-APPROX smooth global approximants
    |   |-- M1234-A-ENERGY uniform energy and vorticity bounds
    |   `-- M1234-A-COMPACT nonlinear-compatible compactness
    `-- M1234-E-CLOSURE close equation and trace
        |-- M1234-E-LINEAR linear weak limits
        |-- M1234-E-NONLINEAR quadratic weak limit
        `-- M1234-E-TRACE one-sided initial vorticity trace
```

The statement definitions, foundation policy, primary-source map, provenance,
documentation, and workflow edges are separate typed graphs and cannot be used
as proof premises.

## Node ledger

### m1234-root
Exact elaborated whole-plane existence target. `[H1, M3, R3]`; open.

### m1234-s-definitions
Checked statement interface for data, solution, weak equations, and trace.
`[H1, M0-L, R3]`.

### m1234-s-foundation
Pending axiom, TCB, choice, and no-oracle certificate. `[H1, M4, R3]`.

### m1234-a-approx
Construct smooth divergence-free approximations with global approximate Euler
solutions. `[H1, M4, R3]`.

### m1234-a-energy
Prove uniform finite-energy and bounded-vorticity estimates. `[H1, M4, R3]`.

### m1234-a-compact
Extract convergence strong enough to pass the nonlinear tensor term.
`[H1, M4, R3]`.

### m1234-a-structure
Pass measurability, integrability, divergence, and curl compatibility to a
`CandidateFields` witness. `[H1, M4, R3]`.

### m1234-e-linear
Pass the time derivative and initial linear terms. `[H1, M4, R3]`.

### m1234-e-nonlinear
Pass the quadratic velocity tensor against compact divergence-free tests.
`[H1, M4, R3]`.

### m1234-e-trace
Establish the required one-sided weak initial-vorticity trace. `[H1, M4, R3]`.

### m1234-e-closure
Assemble momentum and trace closure for every candidate. `[H1, M4, R3]`.

### m1234-t-assemble
Kernel-checked construction of `GlobalWeakSolution` from the two explicit
packages. `[H1, M0-L, R3]`; conditional only.

### m1234-x-source
Pending primary-source theorem/page/hypothesis/errata mapping for every analytic
step. Human-source overlay only; `[H1, M4, R3]`.

### m1234-x-provenance
Pending proof-body, import, axiom, TCB, and replay inventory. Informational
machine overlay; `[H1, M4, R3]`.

## Freeze boundary

The minimal open root cut is `M1234-A-STRUCTURE` plus
`M1234-E-CLOSURE`. The checked assembly does not prove either premise. Any
split, merge, correction, or eligibility change requires registry version 2
and an append-only delta. This phase claims no proof, audit completion, or
theorem completion.
