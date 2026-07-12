# THM-M-0534 frozen obligation architecture

Item: `S56-M-0534-OBLIGATION_TREE`.

The registry freezes 14 semantic obligations before target-owned proof execution. Imported theorem
names are bridge boundaries, not terminal proof credit.

## Typed proof route

```text
M0534-ROOT exact continuing sequence
`-- M0534-T-ASSEMBLE checked conditional composition
    |-- M0534-L-SAME same-degree exactness
    |   |-- M0534-X-SNAKE snakeInput engine
    |   `-- M0534-X-ENDPOINT endpoint right-exactness
    |-- M0534-L-INTO homologyMap g then delta
    |   |-- M0534-C-DELTA connecting-map construction
    |   `-- M0534-X-SNAKE snakeInput engine
    `-- M0534-L-OUT delta then homologyMap f
        |-- M0534-C-DELTA connecting-map construction
        `-- M0534-X-SNAKE snakeInput engine
```

## Node ledger

### m0534-root
Exact elaborated target. `[H2, M1, R4]`; no target-owned inhabitant is claimed.

### m0534-s-definitions
Checked domains, maps, relations, and exactness interface. `[H2, M0-L, R4]`.

### m0534-s-boundary
Endpoint and arbitrary-shape coverage audit. `[H2, M4, R4]`.

### m0534-s-transport
Checked paired/grouped equivalence. `[H2, M0-L, R4]`.

### m0534-s-foundation
Pending transitive axiom, TCB, and no-oracle acceptance. `[H2, M4, R4]`.

### m0534-c-delta
Connecting morphisms and their two composition-zero witnesses. `[H2, M4, R4]`.

### m0534-l-same
Imported same-degree exactness bridge, including endpoints. `[H2, M1, R4]`.

### m0534-l-into
Imported exactness bridge entering the connecting map. `[H2, M1, R4]`.

### m0534-l-out
Imported exactness bridge leaving the connecting map. `[H2, M1, R4]`.

### m0534-x-snake
The central snake-input proof package, explicitly retained as a bridge. `[H2, M4, R4]`.

### m0534-x-endpoint
The endpoint `opcycles_right_exact` package. `[H2, M4, R4]`.

### m0534-t-assemble
Kernel-checked composition from all three families to the exact root. `[H2, M0-L, R4]`; its
premises remain explicit.

### m0534-x-source
Pending primary-source theorem/page/assumption/errata crosswalk. `[H2, M4, R4]`.

### m0534-x-provenance
Pending terminal-body, import, axiom, TCB, and replay inventory. `[H2, M4, R4]`.

## Freeze boundary

The immediate open root cut is `M0534-L-SAME`, `M0534-L-INTO`, and `M0534-L-OUT`. Their pinned
anchors are known, but this phase supplies neither the target-owned proof wrapper nor accepted
transitive proof-body and trust evidence. Any split, merge, correction, or eligibility change needs
a new registry version and append-only delta. No audit or theorem completion is claimed.
