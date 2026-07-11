# THM-M-0394 Frozen Obligation Tree

Item: `S56-M-0394-OBLIGATION_TREE`  
Registry version: `1`  
Status: architecture self-test only; root open

The registry freezes 17 root-relevant semantic obligations before proof execution. Every obligation
is machine-, human-source-, and readability-required. Aliases and presentation rows add no credit.
The machine-readable authority is `obligation-registry.json`; `typed-graphs.json` stores separate
proof, refinement, provenance, evidence, trust, documentation, and workflow graphs.

## Proof Route

```text
M0394-ROOT exact Siegel statement
`-- M0394-T terminal exact-root composition
    |-- M0394-N semantic realization of genus/boundary/coordinates
    |-- M0394-N1 model-independent integrality transport
    `-- M0394-B checked two-branch recomposition
        |-- M0394-B1 positive-genus branch
        |   |-- M0394-C1 divisor/height/approximation construction
        |   `-- M0394-L1 positive-genus finiteness engine
        `-- M0394-B2 genus-zero, three-boundary branch
            |-- M0394-C2 rational parameter/boundary construction
            |-- M0394-L2 finite-fiber reduction to S-units
            `-- M0394-X1 S-unit equation finiteness boundary
```

`M0394-S`, `S1`, `S2`, and `S3` refine the statement interface. `M0394-X2` is a trust/provenance
release boundary and is not a mathematical premise. The checked `M0394-B` composition consumes
abstract proofs of both branches; it proves neither branch.

## Node Ledger

### m0394-root
Exact `Stage1Rev56.THMM0394.Statement`. `[H3, M3, R3]`; root proof remains absent.

### m0394-s
Frozen object-model and integrality interface. `[H3, M3, R3]`.

### m0394-s1
Checked exact statement expansion. `[H3, M0-L, R3]`; definition transport only.

### m0394-s2
Checked coordinatewise S-integrality expansion. `[H3, M0-L, R3]`; definition transport only.

### m0394-s3
Positive-genus versus genus-zero/three-boundary split embedded in `IsSiegelCurve`. `[H3, M3, R3]`.

### m0394-n
Planned bridge from explicit compatibility fields to genuine curve semantics. `[H3, M4, R3]`.

### m0394-n1
Planned model/coordinate independence theorem for integral-point finiteness. `[H3, M4, R3]`.

### m0394-b
Kernel-checked conditional recomposition of the two exact branches. `[H3, M0-L, R3]`; no branch proof.

### m0394-b1
Positive-genus branch. `[H3, M4, R3]`; split into `C1` and `L1` before proof work.

### m0394-b2
Genus-zero branch with at least three boundary points. `[H3, M4, R3]`; split into `C2`, `L2`, `X1`.

### m0394-c1
Positive-genus height/approximation construction package. `[H3, M4, R3]`.

### m0394-l1
Positive-genus Diophantine approximation finiteness engine. `[H3, M4, R3]`.

### m0394-c2
Genus-zero rational parameter and boundary normalization. `[H3, M4, R3]`.

### m0394-l2
Finite-fiber reduction from integral points to an S-unit equation. `[H3, M4, R3]`.

### m0394-x1
S-unit equation finiteness theorem boundary. `[H3, M4, R3]`; no pinned terminal anchor was found.

### m0394-t
Terminal composition targeting the exact root. `[H3, M4, R3]`; minimal open root cut set.

### m0394-x2
Terminal trust, axiom, proof-body, dependency, and provenance audit. `[H3, M4, R3]`; release-only edge.

## Boundary

The registry is an execution architecture, not a proof. Planned targets are not Lean declarations.
No H0/R0, substantive branch closure, exact terminal proof, theorem completion, or master acceptance
is claimed.
