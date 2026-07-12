# THM-M-1527 frozen obligation architecture

Item: `S56-M-1527-OBLIGATION_TREE`.

The registry freezes ten obligations before root-proof execution. The proof route is deliberately
small because the exact statement makes the convention-dependent 3+1 calculation explicit in
`CoordinateDecomposition`; that supplied structure must not be mistaken for a formal derivation of
the physics bridge.

## Typed proof route

```text
M1527-ROOT exact canonical proposition
|-- M1527-S-CONVENTIONS carry dimension/signature/orientation/positivity premises
`-- M1527-T-ASSEMBLE checked conditional composition
    |-- M1527-L-HOMOGENEOUS  dF = 0 iff Gauss-magnetic and Faraday
    |-- M1527-L-INHOMOGENEOUS d(star F) = J iff Gauss-electric and Ampere-Maxwell
    `-- M1527-L-CONJUNCTION reassociate the four classical conjuncts
```

`M1527-S-DEFINITIONS`, `M1527-X-SOURCE`, `M1527-X-FOUNDATION`, and
`M1527-X-PROVENANCE` inhabit separate refinement, provenance, trust, documentation, and workflow
graphs. They cannot masquerade as proof premises.

## Node ledger

### m1527-root
Exact elaborated conditional equivalence. `[H2, M3, R3]`; no canonical inhabitant is asserted.

### m1527-s-definitions
Checked component and covariant predicate interface. `[H2, M0-L, R3]`.

### m1527-s-conventions
Carry all dimension, signature, orientation, and positivity premises through the eventual wrapper.
They are model boundaries, not evidence for either coordinate bridge. `[H2, M4, R3]`.

### m1527-l-homogeneous
The homogeneous coordinate bridge exposed by `CoordinateDecomposition.homogeneous_iff`.
`[H2, M4, R3]`; extraction into the root wrapper remains proof-phase work.

### m1527-l-inhomogeneous
The sourced coordinate bridge exposed by `CoordinateDecomposition.inhomogeneous_iff`.
`[H2, M4, R3]`; extraction into the root wrapper remains proof-phase work.

### m1527-l-conjunction
Checked logical reassociation and ordering of all four classical equations. `[H2, M0-L, R3]`.

### m1527-t-assemble
Kernel-checked composition from the two explicit bridge premises to the fixed-field equivalence.
`[H2, M0-L, R3]`; the premises prevent this conditional theorem from claiming root closure.

### m1527-x-source
Pending primary-source theorem/page/convention map for both bridges. `[H2, M4, R3]`.

### m1527-x-foundation
Pending transitive axiom, import, TCB, and no-oracle report. `[H2, M4, R3]`.

### m1527-x-provenance
Pending terminal-body, projection, wrapper, and replay inventory. `[H2, M4, R3]`.

## Freeze boundary

The minimal open root cut is the two coordinate bridges plus convention-preserving root wrapping.
The checked conditional assembly supplies no human-source acceptance, trust closure, root proof,
validation, release, or theorem completion. Registry changes require a new version and append-only
delta.
