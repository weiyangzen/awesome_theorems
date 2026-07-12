# THM-M-1027 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 20 canonical semantic obligations for
`S56-M-1027-OBLIGATION_TREE` before proof execution. The route uses the immutable external
Brownian-motion anchor found by the preceding audit, but it keeps integration, API normalization,
the five Wiener laws, witness assembly, source fidelity, provenance, and trust as separate debts.
The external repository is not installed and receives no proof credit.

The ordered machine, human-source, readable, and informational denominator ID sets are stored in
`obligation-registry.json`. Any later correction, split, merge, or eligibility change requires
registry version 2 and an append-only delta; proof availability cannot silently change version 1.

## Typed proof route

```text
M1027-ROOT  exact WienerExistenceTarget [open M3]
|-- M1027-T-PACKAGE  one coherent Wiener witness [open M4]
|   |-- M1027-C-CONSTRUCTION  external Brownian construction
|   |   |-- M1027-X-EXTERNAL  pin/import/audit external closure
|   |   `-- M1027-N-API  normalize external API
|   |       |-- M1027-S-DEFS  frozen definitions
|   |       `-- M1027-S-DOMAIN  frozen domains and binders
|   |-- M1027-L-PROBABILITY  probability measure
|   |-- M1027-L-MEASURABLE  coordinate measurability
|   |-- M1027-L-ZERO  almost-sure zero start
|   |-- M1027-N-INCREMENT  ordered Gaussian increment law
|   |   |-- M1027-N-API
|   |   `-- M1027-S-BOUNDARY  equal-time variance
|   |-- M1027-L-INDEPENDENCE  independent increments
|   `-- M1027-L-CONTINUITY  almost-sure continuous paths
`-- M1027-T-ASSEMBLE  checked witness-to-root interface [M0-L]
```

`M1027-S-TRANSPORT`, `M1027-S-FOUNDATION`, `M1027-X-SOURCE`,
`M1027-X-PROVENANCE`, and `M1027-X-TRUST` live in refinement, source, trust,
documentation, and workflow graphs rather than being disguised as mathematical premises.
All proof edges have reciprocal `proof_requires`/`composes` edges.

## Leaf policy

Every current leaf has a substantive planned ledger and a budget no greater than 100. These are
planning ceilings, not proof or readability claims. Execution must split any node that exposes a
hidden construction invariant, case split, representation transport, major imported theorem, or
ledger longer than 100 steps. In particular, the external Brownian theorem cannot be treated as a
one-line primitive: its Kolmogorov-extension dependency, source body, axioms, and API adapters remain
explicit root-relevant obligations.

`ObligationTree.lean` checks only the final child-to-root composition. Its theorem consumes an
explicit `WienerWitnessPackage`; it does not inhabit that package. Thus `M1027-T-ASSEMBLE` is locally
closed while the minimal open root cut is `M1027-T-PACKAGE`.

## Status boundary

This phase freezes and structurally tests the registry and seven typed graphs. It does not fetch or
integrate the external project, construct Brownian motion, close the witness package, establish H0
or R0, complete the audit, perform hermetic replay, or prove the root. Lifecycle remains `planned`,
the root vector remains `[H1, M3, R3]`, and master acceptance is still required.
