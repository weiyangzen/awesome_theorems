# THM-M-0416 frozen obligation architecture

Item: `S56-M-0416-OBLIGATION_TREE`.

The registry freezes nine root-relevant obligations before proof integration.
Candidate availability from the anchor audit is recorded as `M0-W`, not as
accepted proof credit.

## Typed proof route

```text
M0416-ROOT exact canonical proposition
`-- M0416-C-COMPOSE checked conditional conjunction assembly
    |-- M0416-I-FREE free quotient instance
    |-- M0416-I-FINITE finite quotient instance
    |-- M0416-T-RANK quotient finrank equals unit rank
    `-- M0416-T-COORDINATES unique torsion/fundamental-unit coordinates
```

`M0416-X-SOURCE`, `M0416-X-PROVENANCE`, and `M0416-X-TRUST` live in separate
source, provenance, documentation, trust, and workflow graphs. They cannot be
counted as proof premises or mathematical closure.

## Node ledger

### m0416-root
Exact elaborated target. `[H1, M3, R3]`; no proof integration receipt exists.

### m0416-c-compose
Kernel-checked child-to-parent composition. `[H1, M0-L, R3]`; conditional only.

### m0416-i-free
Pinned mathlib typeclass candidate for quotient freeness. `[H1, M0-W, R3]`.

### m0416-i-finite
Pinned mathlib typeclass candidate for quotient finiteness. `[H1, M0-W, R3]`.

### m0416-t-rank
Pinned `NumberField.Units.rank_modTorsion` candidate. `[H1, M0-W, R3]`.

### m0416-t-coordinates
Pinned `NumberField.Units.exist_unique_eq_mul_prod` candidate. `[H1, M0-W, R3]`.

### m0416-x-source
Pinpoint primary-source passage, assumption, convention, and errata map remains
open. `[H1, M4, R3]`.

### m0416-x-provenance
Transitive bodies and the providers of both typeclass instances remain open.
`[H1, M4, R3]`.

### m0416-x-trust
Foundation, axiom, TCB, no-oracle, and replay acceptance remains open.
`[H1, M4, R3]`.

## Freeze boundary

The machine root cut consists of the four mathematical packages. Their pinned
candidates do not become accepted proof bodies until the proof phase records
exact integration and provenance. This phase supplies no root closure, audit
completion, or theorem completion. Registry changes require a new version and
an append-only old/new ID delta.
