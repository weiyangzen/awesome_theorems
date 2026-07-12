# THM-M-1553 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 14 semantic obligations before proof execution. The selected route
expands the concrete Hirota sums and the transformed KdV residual, proves the required logarithmic
and mixed-partial identities, establishes the resulting polynomial identity, and clears the
strictly positive tau denominator pointwise. The anchor audit found no existing exact proof body;
this route selection does not claim otherwise.

Machine, human-source, and readable denominators are ordered ID sets in
`obligation-registry.json`. Provenance and trust overlays remain outside proof coverage. Any split,
merge, correction, or eligibility change requires registry version 2 and an append-only ID delta.

## Typed proof route

```text
M1553-ROOT  exact HirotaKdVTarget [open M3]
|-- M1553-B-POLYNOMIAL  logarithmic bilinear-to-KdV bridge [open M4]
|   |-- M1553-N-HIROTA  expand D_x^4 + D_x D_t
|   |-- M1553-N-TRANSFORM  expand u and the KdV residual
|   |-- M1553-L-LOG  logarithmic derivative identities
|   |   `-- M1553-L-REGULARITY  derivative legality
|   `-- M1553-L-MIXED  mixed-partial commutation
|       `-- M1553-L-REGULARITY
|-- M1553-T-ZERO  positivity, denominator clearing, bilinear zero
|   |-- M1553-B-POLYNOMIAL
|   `-- M1553-S-CONTEXT  exact hypotheses and quantifiers
|       `-- M1553-S-BOUNDARY  constant tau and zero-exclusion cases
`-- M1553-T-ASSEMBLE  checked conditional root interface [M0-L]
```

`M1553-X-SOURCE`, `M1553-X-PROVENANCE`, and `M1553-X-TRUST` are typed source,
provenance, and trust nodes and receive no mathematical proof credit. Seven graphs, including
reciprocal `proof_requires` and `composes` edges, are stored in `typed-graphs.json`.

## Leaf and composition policy

Every node has a substantive semantic ledger and a planning budget no greater than 100 steps.
Proof work must version and split the registry if an exact signature exposes hidden cases or a
larger ledger. A short invocation of a derivative or mixed-partial theorem remains a substantive
bridge requiring provenance and checked composition.

`ObligationTree.lean` checks only that a universal `LogDerivativeBridge` composes into the exact
root. It does not construct that premise. Thus `M1553-T-ASSEMBLE` is locally closed while the root
cut remains `M1553-B-POLYNOMIAL` plus `M1553-T-ZERO`.

## Status boundary

This phase freezes and structurally tests the architecture. It proves neither the analytic bridge
nor the root and establishes no H0/R0, full audit, hermetic replay, or theorem completion. The
lifecycle remains `planned`, the root vector remains `[H2, M3, R3]`, and master acceptance remains
required.
