# THM-M-1269 frozen obligation architecture

Item: `S56-M-1269-OBLIGATION_TREE`.

The registry freezes 14 semantic obligations before proof-phase closure is
observed. The proof route uses the pinned `exists_seq_tendsto_sInf` anchor, but
this phase records that theorem as an open bridge rather than installing a
canonical proof or assigning root closure.

## Typed proof route

```text
M1269-ROOT exact canonical proposition
`-- M1269-T-ASSEMBLE checked conditional composition
    `-- M1269-C-VALUES construct convergent values in Set.range F
        `-- M1269-L-SINF pinned exists_seq_tendsto_sInf bridge
            `-- M1269-N-RANGE normalize to the nonempty bounded-below range
```

Definitions, domain and mutation boundaries, absence of case splits, preimage
choice, convergence transport, foundation policy, source mapping, provenance,
documentation, trust, and workflow ordering live in separate typed graphs.
They cannot masquerade as additional proof premises or duplicate coverage.

## Node ledger

### m1269-root
The exact elaborated statement. `[H2, M1, R3]`; this phase supplies no accepted
proof body.

### m1269-s-definitions
The exact `Set.range`, `BddBelow`, `sInf`, `Tendsto`, `atTop`, and `nhds`
interface checked by `Statement.lean`. `[H2, M0-L, R3]` provisionally.

### m1269-s-domain
Universe, domain, functional, nonemptiness, and lower-bound premises preserved.
`[H2, M0-L, R3]` provisionally.

### m1269-s-boundary
Empty and unbounded variants, point convergence, and infimum attainment remain
outside the claim; the mutation surfaces keep these distinctions visible.
`[H2, M0-L, R3]` provisionally.

### m1269-s-foundation
Classical preimage choice and transitive axiom/TCB closure. `[H2, M4, R3]`;
the anchor audit reports `propext`, `Classical.choice`, and `Quot.sound`, but a
release-grade trust certificate is not present.

### m1269-n-range
Normalize the problem to `S = Set.range F`, using nonemptiness and boundedness.
`[H2, M4, R3]` until proof-phase evidence binds the construction.

### m1269-b-none
No case split remains after the two explicit hypotheses. This is an
informational architecture node with no independent proof credit.

### m1269-c-values
Construct range values converging to `sInf (Set.range F)`. `[H2, M1, R3]`;
the pinned anchor is applicable, but this construction is not accepted here.

### m1269-c-preimages
Choose one `X`-preimage for each range value. The conditional composition file
checks this step. `[H2, M0-L, R3]` provisionally.

### m1269-l-sinf
The central pinned mathlib bridge `exists_seq_tendsto_sInf`. `[H2, M1, R3]`;
its audit and wrapper exist, while proof-phase provenance and acceptance remain
open.

### m1269-t-transport
Transport convergence across the function equality supplied by the chosen
preimages. `[H2, M0-L, R3]` provisionally.

### m1269-t-assemble
Kernel-checked conditional composition into `THM_M_1269_statement`.
`[H2, M0-L, R3]`; its explicit bridge premise prevents root proof credit.

### m1269-x-source
The primary-source theorem/page/assumption/errata map remains `[H2]` and open.
This non-machine node supplies no proof credit.

### m1269-x-provenance
Terminal-body, wrapper, import, axiom, TCB, and replay inventory remains open.
This informational overlay supplies no mathematical proof credit.

## Freeze boundary

The minimal open root cut is `M1269-L-SINF`: later proof work must bind the
pinned declaration and exact wrapper as accepted node evidence. This phase
does not claim audit completion, root closure, or theorem completion. Any
split, merge, correction, exclusion, or eligibility change requires registry
version 2 and an append-only old/new obligation delta.

