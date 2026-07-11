# THM-M-0003 frozen obligation architecture

Item: `S56-M-0003-OBLIGATION_TREE`.

The registry freezes 19 obligations before proof execution. It follows the
pinned mathlib construction, but does not credit an upstream declaration,
conditional composition, or an elaboration run as accepted node closure.

## Typed proof route

```text
M0003-ROOT exact canonical proposition
`-- M0003-T-ASSEMBLE conditional four-segment composition
    |-- M0003-L-KERNEL exact kernel row
    |   `-- M0003-C-KERNELS component kernel limits and upper columns
    |-- M0003-L-LEFT exactness of L0.g followed by delta
    |   |-- M0003-C-ZERO bridge zero composites
    |   |   |-- M0003-C-DELTA connecting map
    |   |   |   |-- M0003-C-PULLBACK auxiliary pullback complex
    |   |   |   `-- M0003-C-COKERNELS component cokernel limits
    |   |   `-- M0003-C-PULLBACK
    |   |-- M0003-C-KERNELS
    |   `-- M0003-C-COKERNELS
    |-- M0003-L-RIGHT exactness of delta followed by L3.f
    |   |-- M0003-L-LEFT
    |   `-- M0003-C-DUALITY opposite-category transport
    |       |-- M0003-C-DELTA
    |       `-- M0003-C-PULLBACK
    `-- M0003-L-COKERNEL exact cokernel row
        |-- M0003-L-KERNEL
        `-- M0003-C-DUALITY
```

Input shape, six-term encoding, statement transport, foundation, provenance,
source, documentation, trust, evidence, and workflow are separate typed graphs.
Support edges never count as proof premises.

## Node ledger

### root
The exact closed six-term target. `[H2, M1, R3]`; the immutable candidate is
known, but this phase records no accepted proof receipt.

### s-input
The complete `SnakeInput` binder and packaged hypotheses. `[H2, M1, R3]`.

### s-six
The six objects and five arrows in `composableArrows`. `[H2, M1, R3]`.

### s-transport
The checked closed-to-pointwise statement equivalence. `[H2, M1, R3]`.

### s-foundation
Pending accepted axiom, foundation, and transitive TCB policy. `[H2, M3, R4]`.

### c-kernels
Component kernel limits and exact upper column segments. `[H2, M1, R4]`.

### c-cokernels
Component cokernel colimits and exact lower column segments. `[H2, M1, R4]`.

### l-kernel
Exactness of the kernel row `L0`. `[H2, M1, R4]`.

### l-cokernel
Exactness of the cokernel row `L3`, obtained by duality. `[H2, M1, R4]`.

### c-pullback
The auxiliary pullback, factorization, short complex, and its exactness. Its
budget is 90 substantive steps and must be split if execution exceeds it.
`[H2, M1, R4]`.

### c-delta
Construction of the connecting homomorphism by descent. `[H2, M1, R4]`.

### c-zero
The two zero composites and bridge short complexes. `[H2, M1, R4]`.

### l-left
Exactness at `L0.X3` adjacent to the connecting map. `[H2, M1, R4]`.

### c-duality
Compatibility of delta with opposite categories and bridge transport.
`[H2, M1, R4]`.

### l-right
Exactness at `L3.X1`, transported from the left bridge. `[H2, M1, R4]`.

### t-assemble
Kernel-checked composition from four explicit segment premises to the exact
pointwise root. `[H2, M1, R3]`; the premises remain uncredited.

### x-upstream
Partial immutable mathlib body provenance. Transitive declaration and import
closure remain open. `[H2, M3, R4]`.

### x-source
Pending primary theorem/page/assumption/sign/errata crosswalk and independent
review. `[H2, M5, R4]`.

### x-tcb
Pending transitive axiom, artifact, replay, and supply-chain trust receipt.
`[H2, M3, R4]`.

## Freeze boundary

The frozen root cut is the four adjacent segment obligations `M0003-L-KERNEL`,
`M0003-L-LEFT`, `M0003-L-RIGHT`, and `M0003-L-COKERNEL`. `root_compose` checks
only their exact child-to-parent composition. All `closed_obligations` remain
empty because anchor availability is not accepted node evidence. This phase
supplies no audit completion or theorem completion. Registry corrections need a
new version and an append-only ID delta.
